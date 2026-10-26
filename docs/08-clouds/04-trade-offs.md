---
type: Guide
title: Cross-Cloud Trade-Offs
description: The five structural differences between AWS, Azure and Google Cloud that change a design decision rather than only a service name.
tags: [aws, azure, gcp, cloud, trade-offs, interview]
---

A service name you can look up. A structural difference you must have thought through, because it changes the design, not the vocabulary. There are five. Together they cause most of what goes wrong when a design moves from one cloud to another, and they are most of what an interviewer probes when asking you to compare clouds.

The last section is the other half of the same skill: decisions that are identical on all three clouds and only *sound* different, because each vendor gives the same trade-off its own product names.

---

## 1. The Boundary a Mistake Cannot Cross

Every cloud has one container that is a real wall: billing and quotas are counted there, and nothing inside it reaches anything outside it without an explicit grant. It is the AWS **account**, the Azure **subscription**, the Google Cloud **project**.

What differs is how expensive that wall is to build, and so how freely a design uses it.

- A project is cheap and expected to be numerous. Project-per-workload-per-environment is routine, and the landing-zone blueprints assume it.
- An account is heavy. Account-per-environment is the idiomatic answer to isolation, but it is a considered decision with vending machinery behind it.
- A subscription sits between the two. Azure then adds a second level that AWS and Google Cloud lack: the **resource group**, a mandatory folder whose contents share a lifecycle.

**What it changes.**

- A pattern that relies on "delete the resource group and everything in it goes" has no direct translation. It becomes a disposable project on Google Cloud, or tag-driven teardown on AWS.
- In the other direction, a design that assumes an account boundary per team may be over-built on Google Cloud. There a folder gives the same policy inheritance without the account-vending overhead.

**The question to ask first.** Which wall is this design relying on, and does the target cloud put a wall in the same place?

**In depth.** AWS [Multi-Account Structure — The Landing Zone](_references/aws-handbook.md#multi-account-structure--the-landing-zone) · Azure [The Resource Hierarchy — Where Everything Lives](_references/azure-handbook.md#the-resource-hierarchy--where-everything-lives) · Google Cloud [Resource Hierarchy — The Landing Zone](_references/gcp-handbook.md#resource-hierarchy--the-landing-zone)

## 2. Whether the Network Is Regional or Global

An AWS VPC and an Azure VNet are regional. A Google Cloud VPC network is **global**, with regional subnets inside it.

This is the single difference that reshapes the most diagrams.

- Adding a region on Google Cloud needs no new network, no peering and no transit hub. The subnet is new; the network is not.
- On AWS and Azure, a second region means a second network, and then a decision about how to join them: peering, Transit Gateway, Virtual WAN, or a hand-built hub and spoke.
- So Google Cloud's answer to the multi-network problem is **Shared VPC** — one host project lending subnets to service projects — rather than a connectivity service. Network Connectivity Center exists but arrived later. It is less central because a global VPC removes many of the cases a transit gateway exists to solve.

**What it changes.** Expansion cost. On a global network, "we are adding eu-west" means a subnet and a firewall rule. On a regional one, it means a network, a route propagation decision, an address-plan review and a new failure mode in the hub.

**The question to ask first.** Is the network in this design one object or one object per region — and is the address plan written accordingly?

**In depth.** AWS [VPC, Subnets and Routing — The Foundation Everything Else Sits In](_references/aws-handbook.md#vpc-subnets-and-routing--the-foundation-everything-else-sits-in) · Azure [VNets, Subnets and Routing — The Foundation Everything Sits In](_references/azure-handbook.md#vnets-subnets-and-routing--the-foundation-everything-sits-in) · Google Cloud [VPC, Subnets and Routes — The Foundation Everything Else Sits In](_references/gcp-handbook.md#vpc-subnets-and-routes--the-foundation-everything-else-sits-in)

## 3. What Inherits, and Whether Anything Can Say No

All three clouds have a hierarchy, and all three inherit permissions downward. They differ on whether a grant can be *revoked* from above.

| | AWS · Azure · Google Cloud |
| --- | --- |
| Grants inherit downward | through Organizations · through Management Groups and Scopes · through the resource tree |
| User-authored deny inside the permission system | yes, explicit `Deny` wins · no · no, except a separate Deny Policy mechanism |
| Where guardrails live instead | Service Control Policies, which filter API calls by principal · Azure Policy with a `Deny` effect, which constrains configuration · Organization Policy, which constrains configuration |

The bottom row is a real distinction, not a detail:

- An SCP answers "may this principal make this call?".
- An Azure Policy or an Organization Policy answers "may a resource exist in this shape?".

A guardrail written as the first cannot always be translated into the second.

**What it changes.** On AWS you can forbid an action. On the other two you mostly forbid a *configuration* — no public IP on a virtual machine, no storage account without HTTPS, resources only in these regions. You also accept that a broad grant high in the tree cannot be taken back from below. So the discipline differs: grant at the lowest node that works, and keep organization-level grants to a small reviewed list.

**The question to ask first.** When this control fails, is it because someone was allowed to call something, or because something was allowed to exist in the wrong shape? Then write it in the mechanism that matches.

**In depth.** AWS [Concepts — Identity and Access](_references/aws-handbook.md#concepts--identity-and-access) · Azure [Azure Policy — The Guardrail RBAC Cannot Provide](_references/azure-handbook.md#azure-policy--the-guardrail-rbac-cannot-provide) · Google Cloud [Organization Policy and VPC Service Controls — The Guardrails](_references/gcp-handbook.md#organization-policy-and-vpc-service-controls--the-guardrails)

## 4. What the Billing Unit Is

Two services can do the same job and meter on different axes. This is where migration estimates go wrong, and it is the second habit to apply to every row of the service map.

| Job | AWS · Azure · Google Cloud |
| --- | --- |
| Run a container | per task, per vCPU-second · per replica, per vCPU-second · per Pod request on Autopilot, per request-second on Cloud Run |
| Run a function | per invocation and GB-second, one request per instance · per execution and GB-second · per request-second, **many requests per instance** |
| Serve a key-value read | read capacity units · request units, shared across reads and writes · document reads, or node-hours on Bigtable |
| Scan a warehouse | per cluster-hour · per cluster-hour or serverless unit · **per byte scanned**, or reserved slots |
| Keep a discount | Savings Plan or commitment · Reservation · Committed use, plus sustained use with no commitment at all |

**What it changes.**

- **The clearest case: Cloud Run concurrency.** One instance serving many requests at once changes the cost model, the connection-pool design and the meaning of per-instance memory, all together.
- **The clearest hazard: BigQuery.** A query pattern that cost nothing extra on a provisioned Redshift cluster becomes a per-byte charge, and the first month's bill is where that is discovered.

**The question to ask first.** What does this service count, and does the workload's shape make that number large?

**In depth.** AWS [Cost Management](_references/aws-handbook.md#cost-management) · Azure [Cost — The Levers in Order of Size](_references/azure-handbook.md#cost--the-levers-in-order-of-size) · Google Cloud [Cost Management](_references/gcp-handbook.md#cost-management)

## 5. Which Failures the Platform Absorbs

Every cloud offers zone tolerance. They disagree about whether you receive it as a setting or assemble it as a topology.

- **Google Cloud** leans on regional resources. A regional managed instance group, a regional Persistent Disk replicating synchronously across two zones, a regional Cloud SQL instance — each survives a zone loss with no second object to manage.
- **Azure** leans on a property. "Zone-redundant" is a tick box on the resource, and the storage redundancy acronyms (LRS, ZRS, GRS, GZRS) apply the same idea to durability. The catch: not every region has zones at all.
- **AWS** leans on topology. Multi-AZ is something you build: subnets in several zones, instances spread across them, RDS Multi-AZ enabled, and a load balancer in front.

Cross-region is the mirror image. Azure ships **Site Recovery** for orchestrated region failover, and pairs many regions with a partner whose planned updates it says it staggers (as of 2026). AWS and Google Cloud expect you to assemble failover from replication, DNS and automation.

**What it changes.** The number of objects in the design, and where review attention goes. A Google Cloud design review asks "is this resource regional?". An AWS design review asks "are all four of these things spread across zones, and does the failover actually work?".

**The question to ask first.** Is this resilience a property I can read off the resource, or a topology someone has to keep correct?

**In depth.** AWS [Resilience and Recovery](_references/aws-handbook.md#resilience-and-recovery) · Azure [Resilience and Operating at Scale](_references/azure-handbook.md#resilience-and-operating-at-scale) · Google Cloud [Resilience and Recovery](_references/gcp-handbook.md#resilience-and-recovery)

---

## The Same Decision in Three Vocabularies

Four decisions recur on every cloud. The product names differ; the reasoning is the same each time. That is what makes them worth rehearsing once rather than three times.

**First-party language, or Terraform.** CloudFormation and the CDK, ARM templates and Bicep, or Terraform everywhere.

- The first-party tool gives day-zero support for new resource types, and no state file to corrupt or back up.
- Terraform wins the moment a second provider is in play — and there usually is one: an identity provider, GitHub repositories, DNS at an external registrar, a monitoring vendor. That is multi-provider, not multi-cloud, and the first-party tool cannot reach it.
- Terraform's real cost: state becomes a production asset, with remote storage, locking, backup and an access model of its own.
- On Google Cloud the decision is already made: the first-party tool, Deployment Manager, reached end of support on 31 March 2026.

**Managed Kubernetes, or the serverless container service.** EKS against ECS on Fargate, AKS against Container Apps, GKE against Cloud Run.

- Default to the serverless service. The identity, load balancer and logging integrations are already wired together, and it scales to zero.
- Move to Kubernetes when you hit something structural — custom resources and operators, DaemonSets for a node-level agent, network policies for tenant isolation, a service mesh.
- The deciding question is organizational, not technical: **does someone own cluster upgrades?** Every managed Kubernetes offering has a version support clock you do not control, and an unowned cluster falls off it. If nobody owns upgrades, the serverless service is the right call even where Kubernetes would technically fit.

**Configuration management, or baked images.** State Manager, Machine Configuration or OS Config against Ansible.

- The first three are pull-based: they re-assert a baseline. Ansible is push-based: it orchestrates ordered steps. They do not really compete.
- The answer worth pushing for is neither. If something is configured at boot, ask why the image does not already contain it. Bake it, replace instances instead of patching them, and the drift problem stops existing.
- Keep configuration management for the cases you truly cannot bake.

**Scale the relational database up, or out.** Aurora, the Hyperscale tier or AlloyDB, against Spanner or sharding.

- Up: these engines take a single-writer workload a very long way. That is the right answer far more often than people admit.
- Out is a different commitment. Spanner is the only horizontally scalable relational option with external consistency across the three clouds. The closest AWS or Azure answer is a managed engine plus sharding you own.
- The deciding questions: will you really outgrow one machine's writes? Does the database itself need more than one region? What is the availability target worth?

**In depth.** AWS [Trade-Offs](_references/aws-handbook.md#trade-offs) · Azure [Trade-Offs — The "It Depends on X" Answers](_references/azure-handbook.md#trade-offs--the-it-depends-on-x-answers) · Google Cloud [Trade-Offs](_references/gcp-handbook.md#trade-offs)
