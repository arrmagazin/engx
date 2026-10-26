---
type: Guide
title: Concepts Across the Clouds
description: Accounts, geography, control plane, compute, networking and identity across AWS, Azure and Google Cloud, and where the analogy breaks.
tags: [aws, azure, gcp, cloud, comparison]
---

The three major clouds solve the same problems and differ mainly in boundaries, names and billing units. Each section states a concept once, names it in all three clouds, then records where the analogy stops being true. That last part is the useful half: compute is compute everywhere; what varies is the boundary a permission is granted at, whether a network is regional or global, and what the billing unit is.

How to read a section:

- **A table row** — the same job, three implementations.
- **The notes under it** — what will bite you.
- **A `*(none)*` entry** — information too: that cloud usually solves the problem somewhere else, and the note says where.

---

## Accounts and Organizations

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Billing and isolation boundary** | Account · Subscription · Project |
| **Root of the estate** | Organization · Tenant · Organization |
| **Grouping node policy attaches to** | Organizational Unit · Management Group · Folder |
| **Lifecycle folder below the boundary** | *(none)* · Resource Group · *(none)* |
| **Guardrail that only removes** | Service Control Policy · Azure Policy with a `Deny` effect · Organization Policy |
| **Directory that performs sign-in** | IAM Identity Center · Entra ID · Cloud Identity |
| **Payment instrument** | payer account · Subscription's billing profile · Billing Account |
| **Countable ceiling** | Service Quota, per account and Region · Quota, per subscription · Quota, per project and region |
| **Repeatable boundary creation** | Control Tower Account Factory · subscription vending · Project Factory |

**Where the analogy breaks.**

- **Resource groups have no counterpart.** Azure puts a mandatory lifecycle folder between the subscription and the resource; deleting it deletes its contents. AWS and Google Cloud have nothing at that level, so patterns that rely on "delete the resource group" must be rebuilt as tagging or as a separate project.
- **Inheritance is the whole model on Google Cloud.** A grant on a folder reaches every project beneath it without being copied. On AWS each account is an island; inheritance must be assembled from Organizations plus SCPs.
- **Only AWS has a guardrail inside the permission system.** SCPs filter API calls by principal. Azure RBAC has no user-authored deny, and Google Cloud IAM has no ordinary explicit deny, so both push guardrails into a policy service that constrains configuration instead.
- **Projects are meant to be numerous.** Google Cloud expects many cheap projects, so project-per-workload is routine there. An AWS account is heavier to create, so account-per-environment is a considered decision.

**In depth.** AWS [Concepts — Accounts and Regions](_references/aws-handbook.md#concepts--accounts-and-regions) · Azure [Concepts — Tenants and Subscriptions](_references/azure-handbook.md#concepts--tenants-and-subscriptions) · Google Cloud [Concepts — Projects and Regions](_references/gcp-handbook.md#concepts--projects-and-regions)

## Geography

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Geographic group of data centres** | Region · Region · Region |
| **Fault-isolated site inside a region** | Availability Zone · Availability Zone · Zone |
| **Stable name for a physical site** | AZ ID, `euc1-az1` · physical zone, `eastus2-az1` · the zone name itself, `us-central1-a` |
| **Automatic cross-region location** | *(none)* · Region Pair · Multi-Region, `US` / `EU` / `ASIA` |
| **Edge site outside any region** | Edge Location · *(Front Door's own edge)* · Point of Presence |
| **Default scope of a virtual network** | regional · regional · global |

**Where the analogy breaks.**

- **Zone names are per account on two of the three clouds.** AWS maps zone names to sites per account, and Azure maps zone numbers per subscription. So the same name may point to different physical sites in two accounts or subscriptions. AWS gives you the AZ ID. Azure returns each subscription's logical-to-physical mapping as `availabilityZoneMappings` from the [List Locations API](https://learn.microsoft.com/rest/api/resources/subscriptions/list-locations); check it as soon as two subscriptions must coordinate placement. Google Cloud zone letters are the same for everyone.
- **Not every Azure region has zones.** Check this first when a design calls for zone redundancy.
- **Google Cloud documents the scope of every resource type.** A network is global, a subnet regional, a virtual machine and a disk zonal. AWS and Azure leave the scope implicit per service.
- **The cross-region story differs in kind.**
  - Azure: a Region Pair is a fixed partner, and Azure says it staggers planned updates across the pair (as of 2026).
  - Google Cloud: a multi-region is a location you can buy.
  - AWS: cross-region replication is something you assemble.

**In depth.** AWS [Accounts, Regions and Availability Zones — Where Everything Lives](_references/aws-handbook.md#accounts-regions-and-availability-zones--where-everything-lives) · Azure [Concepts — Regions and Resources](_references/azure-handbook.md#concepts--regions-and-resources) · Google Cloud [Organizations, Projects, Regions and Zones — Where Everything Lives](_references/gcp-handbook.md#organizations-projects-regions-and-zones--where-everything-lives)

## The Control Plane

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **What every tool ends up calling** | the service's own API · ARM · the service's own API |
| **Unique identifier of a resource** | ARN · Resource ID · Resource Name |
| **Cost-attribution label** | Tag · Tag · Label |
| **Service must be enabled first** | no · no · yes, per project |
| **Command line** | `aws` · `az` · `gcloud` |
| **Control-plane audit trail** | CloudTrail · Activity Log · Cloud Audit Logs |

**Where the analogy breaks.**

- **Azure has one control plane; the other two do not.** Every Azure tool is a client of ARM, which removes a category of confusion: "it worked in the portal but failed in Terraform" is a permissions or API-version difference, never a tool difference. On AWS each service has its own API, error shapes and consistency behaviour.
- **Enabling the API is a real step on Google Cloud.** Calls fail with `SERVICE_NAME has not been used in project N before or it is disabled`, at apply time rather than plan time. Enable a project's APIs in the project's own Terraform, ahead of anything that depends on them.
- **Moving a resource changes its identifier on Azure.** Anything written against the old Resource ID breaks. ARNs and Resource Names also encode their container, so the same caution applies wherever a move is possible at all.
- **Audit coverage is not equivalent.** Azure's Activity Log is control plane only; data-plane auditing is enabled per service. Google Cloud has four audit streams, with data-access logs off by default for cost.

**In depth.** AWS [The Console, the CLI and the API — How You Talk to AWS](_references/aws-handbook.md#the-console-the-cli-and-the-api--how-you-talk-to-aws) · Azure [ARM — The One Control Plane](_references/azure-handbook.md#arm--the-one-control-plane) · Google Cloud [The Console, the gcloud CLI and the API — How You Talk to Google Cloud](_references/gcp-handbook.md#the-console-the-gcloud-cli-and-the-api--how-you-talk-to-google-cloud)

## Compute — Machines

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Virtual machine service** | EC2 · Virtual Machines · Compute Engine |
| **Shape of the machine** | Instance Type · VM Size · Machine Type, or Custom Machine Type |
| **Bootable disk template** | AMI · Image, via Azure Compute Gallery · Image |
| **Declaration a group creates from** | Launch Template · *(part of the scale set model)* · Instance Template |
| **Self-healing, scaling group** | Auto Scaling Group · Virtual Machine Scale Sets · Managed Instance Group |
| **Interruptible discount capacity** | Spot Instance · Spot Virtual Machines · Spot VM |
| **Disk physically attached to the host** | Instance Store · Ephemeral OS Disk · Local SSD |
| **Commitment discount** | Savings Plan · Reservation · Committed Use Discount |
| **Automatic discount for just running** | *(none)* · *(none)* · Sustained Use Discount |

**Where the analogy breaks.**

- **Custom machine types are a Google Cloud answer.** You pick vCPU and memory rather than a published size, and sustained use discounts apply without any commitment.
- **Host maintenance differs.** Google Cloud live-migrates a running instance by default. Azure uses memory-preserving maintenance, including live migration, for most VM sizes on a best-effort basis, with a reboot as the fallback. AWS announces maintenance that needs a reboot, stop or retirement as a scheduled event, and you or the group act on it.
- **Azure subnets are regional, so the machine picks its zone** — the placement decision sits on the instance, not on the subnet as it does on AWS.
- **Spot is simplest on Google Cloud:** no bidding and no capacity pools to reason about, a 30-second notice by default ([120 seconds](https://cloud.google.com/compute/docs/instances/spot) if set at creation), and a variable price Google may change up to once a day (as of 2026).
- **Google Cloud spreads across zones by default.** A regional managed instance group spreads across zones unless told otherwise; an AWS Auto Scaling group spreads only across the subnets you list.

**In depth.** AWS [Concepts — Compute Instances](_references/aws-handbook.md#concepts--compute-instances) · Azure [Concepts — Compute Instances](_references/azure-handbook.md#concepts--compute-instances) · Google Cloud [Concepts — Compute Instances](_references/gcp-handbook.md#concepts--compute-instances)

## Compute — Containers

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Managed Kubernetes** | EKS · AKS · GKE |
| **Kubernetes with nodes managed for you** | EKS Auto Mode, or EKS with Fargate · AKS Automatic · GKE Autopilot |
| **Proprietary orchestrator** | ECS · *(none)* · *(none)* |
| **Run a container without a cluster** | App Runner · Container Apps · Cloud Run |
| **Container registry** | ECR · Azure Container Registry · Artifact Registry |
| **Pod-level cloud identity** | IRSA · Entra Workload ID · Workload Identity Federation for GKE |
| **Node group** | managed node group, or Karpenter · Node Pool · Node Pool |
| **Event-driven autoscaling** | *(per-service)* · KEDA, built into Container Apps · *(Cloud Run request concurrency)* |

**Where the analogy breaks.**

- **Cloud Run is central in a way App Runner is not.** It is the default home for a stateless HTTP service on Google Cloud, and Cloud Run functions are built on top of it.
- **Autopilot is not a launch type.** It is Kubernetes billed per Pod request, not a second way to run a task as Fargate is under ECS and EKS.
- **Only AWS has a proprietary orchestrator worth learning.** On the other two clouds the answer to "not Kubernetes" is the serverless container service.
- **Registry permissions catch people out on Azure:** the AKS *kubelet* identity needs the pull permission, not the cluster identity.
- **Artifact Registry is broader than ECR** — containers, language packages and OS packages in one service.

**In depth.** AWS [Concepts — Compute Containers](_references/aws-handbook.md#concepts--compute-containers) · Azure [Concepts — Compute Containers](_references/azure-handbook.md#concepts--compute-containers) · Google Cloud [Concepts — Compute Containers](_references/gcp-handbook.md#concepts--compute-containers)

## Compute — Functions

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Function service** | Lambda · Azure Functions · Cloud Run functions |
| **What starts an invocation** | Event Source Mapping · Trigger · Trigger |
| **Declarative input and output** | *(written in code)* · Binding · *(written in code)* |
| **Stateful orchestration in code** | Lambda durable functions, or Step Functions as a state machine · Durable Functions · Workflows, as YAML |
| **Requests one instance serves at once** | one, except on Lambda Managed Instances · many, configurable per trigger · many |
| **Paying to avoid cold starts** | Provisioned Concurrency · Premium plan, always-ready instances · Minimum Instances |
| **Capping spend or protecting a database** | Reserved Concurrency · per-plan instance limits · Maximum Instances |
| **Shared code package** | Layer · *(app-level dependencies)* · *(container image)* |
| **Managed HTTP front door** | API Gateway · API Management · API Gateway |

**Where the analogy breaks.**

- **Concurrency is the headline difference.** One Cloud Run instance, like one Azure Functions host, serves many requests at once; a standard Lambda execution environment serves exactly one (Lambda Managed Instances are the exception). Cost models, connection pooling and the meaning of "per-instance memory" all follow from that single fact.
- **Durable Functions and Lambda durable functions are the code-first pair.** Both replay ordinary code from checkpoints, so orchestration code must be deterministic — a different discipline from authoring a Step Functions state machine. Logic Apps is the low-code path Azure offers alongside.
- **Step Functions and Workflows price differently** — per state transition against per step. That changes how fine-grained a workflow it is sensible to write.

**In depth.** AWS [Concepts — Compute Functions](_references/aws-handbook.md#concepts--compute-functions) · Azure [Concepts — Compute Functions](_references/azure-handbook.md#concepts--compute-functions) · Google Cloud [Concepts — Compute Functions](_references/gcp-handbook.md#concepts--compute-functions)

## Networking — Inside the Network

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **The private network** | VPC, regional · VNet, regional · VPC network, global |
| **Address range** | CIDR Block · Address Space · CIDR Range, on the subnet |
| **Regional slice of it** | Subnet, per zone · Subnet, regional · Subnet, regional |
| **Stateful instance-level filter** | Security Group · NSG plus ASG · Firewall Rule |
| **Stateless subnet-level filter** | Network ACL · *(none)* · *(none)* |
| **What a rule is attached by** | security group membership · subnet or interface · Network Tag or service account |
| **Inherited filter from above** | *(none)* · Azure Firewall in the hub · Hierarchical Firewall Policy |
| **Outbound access without a public IP** | NAT Gateway · NAT Gateway · Cloud NAT |
| **Route control** | Route Table · User-Defined Route · Route, on Cloud Router |
| **Private path to the cloud's own APIs** | VPC Endpoint · Service Endpoint or Private Endpoint · Private Google Access |
| **Private path to someone else's service** | PrivateLink · Private Link · Private Service Connect |

**Where the analogy breaks.**

- **The global VPC changes the shape of every answer.** Adding a region on Google Cloud needs no new network and no peering, so much of what Transit Gateway exists to solve does not arise.
- **There is no internet gateway on Azure.** Outbound access needs a NAT Gateway or another explicit method. An AWS subnet, by contrast, becomes public by routing to an IGW.
- **Only AWS has two filtering layers.** NACLs are stateless and subnet-wide; the other two clouds give you one stateful mechanism with priorities. Azure NSGs support deny rules and explicit priority ordering; AWS security groups do not.
- **Cloud NAT is not an instance.** It is a feature of the router, so there is no per-zone deployment and no bandwidth bottleneck to size.
- **Google Cloud firewall rules apply by tag or service account**, not by attachment. That makes identity-shaped network policy natural, and makes "which rules hit this VM" a query rather than a lookup.

**In depth.** AWS [Concepts — Inside the VPC](_references/aws-handbook.md#concepts--inside-the-vpc) · Azure [Concepts — Inside the VNet](_references/azure-handbook.md#concepts--inside-the-vnet) · Google Cloud [Concepts — Inside the VPC](_references/gcp-handbook.md#concepts--inside-the-vpc)

## Networking — Edge and Load Balancing

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Layer-7 load balancer** | Application Load Balancer · Application Gateway · Cloud Load Balancing, external Application Load Balancer |
| **Layer-4 load balancer** | Network Load Balancer · Load Balancer · internal and external passthrough load balancers |
| **Where backends are registered** | Target Group · backend pool · Backend Service plus Network Endpoint Group |
| **Global anycast entry point** | CloudFront plus Global Accelerator · Front Door · a single global anycast IP |
| **Content delivery** | CloudFront · Front Door caching · Cloud CDN, Media CDN |
| **Managed DNS** | Route 53 · Azure DNS plus Private DNS Zones · Cloud DNS |
| **DNS-level global routing** | Route 53 routing policies · Traffic Manager · *(the anycast IP removes the need)* |
| **Web application firewall** | WAF · WAF on Application Gateway or Front Door · Cloud Armor |
| **Liveness test** | target group health check · Health Probe · Health Check |

**Where the analogy breaks.**

- **Google Cloud's external load balancer is one global anycast IP**, not a regional endpoint fronted by DNS. Global routing stops being a DNS problem, which is why there is no Traffic Manager equivalent to learn.
- **Azure folds the edge into one service.** Front Door covers the anycast edge, caching, edge WAF and global failover, where AWS splits that across CloudFront, Global Accelerator and WAF.
- **Cloud CDN is a switch, not a distribution.** You enable it on a backend rather than configuring a separate object.
- **The Google Cloud forwarding-rule chain has more parts to assemble** — forwarding rule, target proxy, URL map, backend service. That means more setup and more places for a misconfiguration to hide.
- **Private DNS is the first place to look when an Azure private endpoint misbehaves.**

**In depth.** AWS [Concepts — Edge and Connections](_references/aws-handbook.md#concepts--edge-and-connections) · Azure [Concepts — Edge and Connections](_references/azure-handbook.md#concepts--edge-and-connections) · Google Cloud [Concepts — Load Balancing and the Edge](_references/gcp-handbook.md#concepts--load-balancing-and-the-edge)

## Identity and Access

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Permission system** | IAM · Azure RBAC · IAM |
| **What a permission attaches to** | identity or resource · Scope in the hierarchy · node in the hierarchy |
| **Grant** | IAM Policy · Role Assignment · Allow Policy |
| **User-authored deny** | explicit `Deny` in a policy · *(none)* · Deny Policy, evaluated first |
| **Guardrail above the grant** | Service Control Policy · Azure Policy `Deny` · Organization Policy |
| **Identity a workload runs as** | IAM Role, via Instance Profile · Managed Identity · Service Account |
| **Taking on another identity** | `sts:AssumeRole` · *(not the model)* · Service Account Impersonation |
| **Trusting an external issuer** | OIDC Federation · Federated Credential · Workload Identity Federation |
| **Pod or app identity** | IRSA · Entra Workload ID · Workload Identity Federation for GKE |
| **Just-in-time elevation** | *(via Identity Center session)* · PIM · *(via short-lived impersonation)* |
| **Ceiling on what a grant can reach** | Permissions Boundary · *(scope plus Policy)* · IAM Condition, VPC Service Controls |
| **Credential discovery in client libraries** | default credential chain · `DefaultAzureCredential` · Application Default Credentials |

**Where the analogy breaks.**

- **Two of the three clouds cannot say "no" inside the permission system.** This one difference reshapes how guardrails are designed on each cloud.
  - Azure role assignments are additive, inherit downward, and carry no user-authored deny.
  - Google Cloud allow policies are additive with no ordinary explicit deny; Deny Policies are a separate, deliberate mechanism.
  - AWS policy evaluation has an explicit `Deny` that always wins.
- **A service account is an identity object, not a role you assume.** On Google Cloud it is both a principal and a resource, so it has its own IAM policy saying who may impersonate it. The Google Cloud equivalent of AWS `sts:AssumeRole` is impersonation, not attachment.
- **Azure managed identities come in two kinds** — system-assigned and user-assigned. User-assigned avoids the deploy-time race where a resource needs a permission before it exists.
- **Entra ID is the directory itself**, not a layer on top of one as IAM Identity Center is.
- **Service account keys are the single largest own-goal on Google Cloud.** `iam.disableServiceAccountKeyCreation` is the most effective one-line control on the platform.

**In depth.** AWS [Concepts — Identity and Access](_references/aws-handbook.md#concepts--identity-and-access) · Azure [Concepts — Identity and Access](_references/azure-handbook.md#concepts--identity-and-access) · Google Cloud [Concepts — Identity and Access](_references/gcp-handbook.md#concepts--identity-and-access)

---

The concept map continues with storage, messaging, encryption, observability, delivery and resilience in [Data and Operations Across the Clouds](02-data-and-operations.md).
