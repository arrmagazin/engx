---
type: Guide
title: Cross-Cloud Trade-Offs
description: The five structural differences between AWS, Azure and Google Cloud that change a design decision rather than only a service name.
tags: [aws, azure, gcp, cloud, trade-offs, interview]
---

A service name you can look up. A structural difference you have to have thought about, because it changes the design rather than the vocabulary. There are five of them, and between them they account for most of what goes wrong when a design is carried from one cloud to another — and most of what an interviewer is actually probing when they ask you to compare clouds.

The last section is the other half of the same skill: decisions that are identical on all three clouds and only *sound* different, because each vendor gives the same trade-off its own product names.

---

## 1. The Boundary a Mistake Cannot Cross

Every cloud has one container that is a genuine wall: billing is counted there, quotas are counted there, and nothing inside it reaches anything outside it without an explicit grant. It is the AWS **account**, the Azure **subscription**, the Google Cloud **project**.

What changes is how expensive that wall is to build, and therefore how freely a design uses it.

- A project is cheap and expected to be numerous. Project-per-workload-per-environment is routine, and the landing-zone blueprints assume it.
- An account is heavy. Account-per-environment is the idiomatic answer to isolation, but it is a considered decision with vending machinery behind it.
- A subscription sits between the two, and Azure then adds a second level AWS and Google Cloud have nothing at: the **resource group**, a mandatory folder whose contents share a lifecycle.

**What it changes.** Any pattern that leans on "delete the resource group and everything in it goes" has no direct translation — it becomes a disposable project on Google Cloud, or tag-driven teardown on AWS. In the other direction, a design that assumes an account boundary per team may be over-built on Google Cloud, where a folder gives the same policy inheritance without the account-vending overhead.

**The question to ask first.** Which wall is this design relying on, and does the target cloud put a wall in the same place?

## 2. Whether the Network Is Regional or Global

An AWS VPC and an Azure VNet are regional. A Google Cloud VPC network is **global**, with regional subnets inside it.

This is the single difference that reshapes the most diagrams.

- Adding a region on Google Cloud needs no new network, no peering and no transit hub. The subnet is new; the network is not.
- On AWS and Azure, a second region means a second network, and then a decision about how to join them: peering, Transit Gateway, Virtual WAN, or a hand-built hub and spoke.
- Google Cloud's answer to the multi-network problem is therefore **Shared VPC** — one host project lending subnets to service projects — rather than a connectivity service. Network Connectivity Center exists, arrived later, and is less central precisely because a global VPC removes many of the cases a transit gateway exists to solve.

**What it changes.** Expansion cost. On a global network, "we are adding eu-west" is a subnet and a firewall rule. On a regional one, it is a network, a route propagation decision, an address-plan review and a new failure mode in the hub.

**The question to ask first.** Is the network in this design one object or one object per region — and is the address plan written accordingly?

## 3. What Inherits, and Whether Anything Can Say No

All three clouds have a hierarchy, and all three inherit permissions downward. They differ on whether a grant can be *revoked* from above.

| | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Grants inherit downward | through Organizations | through Management Groups and Scopes | through the resource tree |
| User-authored deny inside the permission system | yes, explicit `Deny` wins | no | no, except a separate Deny Policy mechanism |
| Where guardrails live instead | Service Control Policies, which filter API calls by principal | Azure Policy with a `Deny` effect, which constrains configuration | Organization Policy, which constrains configuration |

The distinction in the bottom row is not pedantry. An SCP answers "may this principal make this call". An Azure Policy or an Organization Policy answers "may a resource exist in this shape". A guardrail written as the first cannot always be translated into the second.

**What it changes.** On AWS you can forbid an action. On the other two you mostly forbid a *configuration* — no public IP on a virtual machine, no storage account without HTTPS, resources only in these regions — and you accept that a broad grant high in the tree cannot be clawed back from below. That makes the discipline different: grant at the lowest node that works, and keep organization-level grants to a small reviewed list.

**The question to ask first.** When this control fails, is it because someone was allowed to call something, or because something was allowed to exist in the wrong shape? Then write it in the mechanism that matches.

## 4. What the Billing Unit Is

Two services can do the same job and meter on different axes. This is where migration estimates go wrong, and it is the second habit worth applying to every row of the service map.

| Job | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Run a container | per task, per vCPU-second | per replica, per vCPU-second | per Pod request on Autopilot, per request-second on Cloud Run |
| Run a function | per invocation and GB-second, one request per instance | per execution and GB-second | per request-second, **many requests per instance** |
| Serve a key-value read | read capacity units | request units, shared across reads and writes | document reads, or node-hours on Bigtable |
| Scan a warehouse | per cluster-hour | per cluster-hour or serverless unit | **per byte scanned**, or reserved slots |
| Keep a discount | Savings Plan or commitment | Reservation | Committed use, plus sustained use with no commitment at all |

**What it changes.** The Cloud Run concurrency line is the clearest case: one instance serving many requests at once changes the cost model, the connection-pool design and the meaning of per-instance memory, all at once. The BigQuery line is the clearest *hazard*: a query pattern that was free-at-the-margin on a provisioned Redshift cluster becomes a per-byte charge, and the first month's bill is where that is discovered.

**The question to ask first.** What does this service count, and does the workload's shape make that number large?

## 5. Which Failures the Platform Absorbs

Every cloud offers zone tolerance. They disagree about whether you receive it as a setting or assemble it as a topology.

- **Google Cloud** leans on regional resources. A regional managed instance group, a regional Persistent Disk replicating synchronously across two zones, a regional Cloud SQL instance — each survives a zone loss with no second object to manage.
- **Azure** leans on a property. "Zone-redundant" is a tick box on the resource, and the storage redundancy acronyms (LRS, ZRS, GRS, GZRS) are the same idea applied to durability. The catch is that not every region has zones at all.
- **AWS** leans on topology. Multi-AZ is something you build: subnets in several zones, instances spread across them, RDS Multi-AZ enabled, and a load balancer in front.

Cross-region is the mirror image. Azure ships **Site Recovery** for orchestrated region failover and pairs every region with a partner it never patches simultaneously; AWS and Google Cloud expect you to assemble failover from replication, DNS and automation.

**What it changes.** The number of objects in the design, and where the review attention goes. A Google Cloud design review asks "is this resource regional?". An AWS design review asks "are all four of these things spread across zones, and does the failover actually work?".

**The question to ask first.** Is this resilience a property I can read off the resource, or a topology someone has to keep correct?

---

## The Same Decision in Three Vocabularies

Four decisions recur on every cloud. The products have different names, and the reasoning is the same each time — which is what makes them worth rehearsing once rather than three times.

**First-party language, or Terraform.** CloudFormation and the CDK, ARM templates and Bicep, or Terraform everywhere. The first-party tool gives day-zero support for new resource types and no state file to corrupt or back up. Terraform wins the moment a second provider is in play — and there usually is one: an identity provider, GitHub repositories, DNS at an external registrar, a monitoring vendor. That is not multi-cloud, it is multi-provider, and the first-party tool cannot reach it. The real cost of Terraform is that state becomes a production asset, with remote storage, locking, backup and an access model of its own. On Google Cloud the decision is already made for you: the first-party tool is deprecated.

**Managed Kubernetes, or the serverless container service.** EKS against ECS on Fargate, AKS against Container Apps, GKE against Cloud Run. Default to the serverless service: the identity, load balancer and logging integrations are already wired together, and it scales to zero. Move to Kubernetes when you hit something structural — custom resources and operators, DaemonSets for a node-level agent, network policies for tenant isolation, a service mesh. The deciding question is organizational rather than technical: **does someone own cluster upgrades?** Every managed Kubernetes offering has a version support clock you do not control, and an unowned cluster falls off it. If nobody owns upgrades, the serverless service is the right call even where Kubernetes would technically fit.

**Configuration management, or baked images.** State Manager, Machine Configuration or OS Config against Ansible — pull-based enforcement that re-asserts a baseline against push-based orchestration of ordered steps. They are not really competing, and the answer worth pushing for is neither: if something is being configured at boot, ask why the image does not already contain it. Bake it, replace instances instead of patching them, and the drift problem stops existing. Configuration management is what you keep for the cases you genuinely cannot bake.

**Scale the relational database up, or out.** Aurora, the Hyperscale tier, or AlloyDB will take a single-writer workload a very long way, and that is the right answer far more often than it is admitted. Out is a different commitment: Spanner is the only one of the three clouds' options that is horizontally scalable relational with external consistency, and the closest AWS or Azure answer is a managed engine plus sharding you own. The deciding questions are whether you will genuinely outgrow one machine's writes, whether the database itself needs more than one region, and what the availability target is worth.

