---
type: Guide
title: Concepts Across the Clouds
description: One table per concept group, naming how AWS, Azure and Google Cloud each incarnate the same idea, and where the analogy stops holding.
tags: [aws, azure, gcp, cloud, comparison]
---

The three major clouds solve the same problems and disagree mainly on boundaries, names and billing units. This chapter is organized by the problem rather than by the vendor: each section states a concept once, names its incarnation in all three clouds, then records where the analogy stops being true. That last part is the useful half — compute is compute everywhere, and what varies is the boundary a permission is granted at, whether a network is regional or global, and what the billing unit is.

Read a row as "the same job, three implementations". Read the notes under it as "and here is what will bite you". A `*(none)*` entry is information too: it usually means that cloud solves the problem somewhere else, and the note says where.

---

## Accounts and Organizations

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Billing and isolation boundary** | Account | Subscription | Project |
| **Root of the estate** | Organization | Tenant | Organization |
| **Grouping node policy attaches to** | Organizational Unit | Management Group | Folder |
| **Lifecycle folder below the boundary** | *(none)* | Resource Group | *(none)* |
| **Guardrail that only removes** | Service Control Policy | Azure Policy with a `Deny` effect | Organization Policy |
| **Directory that performs sign-in** | IAM Identity Center | Entra ID | Cloud Identity |
| **Payment instrument** | payer account | Subscription's billing profile | Billing Account |
| **Countable ceiling** | Service Quota, per account and Region | Quota, per subscription | Quota, per project and region |
| **Repeatable boundary creation** | Control Tower Account Factory | subscription vending | Project Factory |

**Where the analogy breaks.**

- **Resource groups have no counterpart.** Azure puts a mandatory lifecycle folder between the subscription and the resource; deleting it deletes its contents. AWS and Google Cloud have nothing at that level, so patterns that lean on "delete the resource group" have to be rebuilt as tagging or as a separate project.
- **Inheritance is the whole model on Google Cloud.** A grant on a folder reaches every project beneath it without being copied. On AWS each account is an island and inheritance has to be assembled from Organizations plus SCPs.
- **Only AWS has a guardrail inside the permission system.** SCPs filter API calls by principal. Azure RBAC has no user-authored deny, and Google Cloud IAM has no ordinary explicit deny, so both push guardrails into a policy service that constrains configuration instead.
- **Projects are meant to be numerous.** Google Cloud expects many cheap projects; an AWS account is heavier to create, which is why account-per-environment is a considered decision there and project-per-workload is routine here.

## Geography

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Geographic group of data centres** | Region | Region | Region |
| **Fault-isolated site inside a region** | Availability Zone | Availability Zone | Zone |
| **Stable name for a physical site** | AZ ID, `euc1-az1` | *(none)* | the zone name itself, `us-central1-a` |
| **Automatic cross-region location** | *(none)* | Region Pair | Multi-Region, `US` / `EU` / `ASIA` |
| **Edge site outside any region** | Edge Location | *(Front Door's own edge)* | Point of Presence |
| **Default scope of a virtual network** | regional | regional | global |

**Where the analogy breaks.**

- **Zone names lie on two of the three clouds.** AWS shuffles zone names per account and Azure shuffles zone numbers per subscription, so two of them do not agree on the same physical building. AWS gives you the AZ ID to recover the truth; Azure gives you nothing, which matters as soon as two subscriptions must coordinate placement. Google Cloud zone letters are consistent for everyone.
- **Not every Azure region has zones at all** — the first thing to check when a design calls for zone redundancy.
- **Google Cloud documents the scope of every resource type.** A network is global, a subnet regional, a virtual machine and a disk zonal. AWS and Azure leave the scope implicit per service.
- **The cross-region story differs in kind.** A Region Pair is a fixed partner Azure never patches at the same time; a Google multi-region is a location you can buy; on AWS cross-region replication is something you assemble.

## The Control Plane

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **What every tool ends up calling** | the service's own API | ARM | the service's own API |
| **Unique identifier of a resource** | ARN | Resource ID | Resource Name |
| **Cost-attribution label** | Tag | Tag | Label |
| **Service must be enabled first** | no | no | yes, per project |
| **Command line** | `aws` | `az` | `gcloud` |
| **Control-plane audit trail** | CloudTrail | Activity Log | Cloud Audit Logs |

**Where the analogy breaks.**

- **Azure has one control plane and the other two do not.** Every Azure tool is a client of ARM, which collapses a category of confusion: "it worked in the portal but failed in Terraform" is then a permissions difference or an API version difference, never a tool difference. On AWS each service has its own API, its own error shapes and its own consistency behaviour.
- **Enabling the API is a real step on Google Cloud.** Calls fail with `SERVICE_NAME has not been used in project N before or it is disabled`, at apply time rather than plan time. Enable a project's APIs in the project's own Terraform, ahead of anything that depends on them.
- **Moving a resource changes its identifier on Azure.** Anything written against the old Resource ID breaks. ARNs and Resource Names encode their container too, so the same caution applies wherever a move is possible at all.
- **Audit coverage is not equivalent.** Azure's Activity Log is control plane only and data-plane auditing is enabled per service; Google Cloud has four audit streams with data-access logs off by default for cost.

## Compute — Machines

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Virtual machine service** | EC2 | Virtual Machines | Compute Engine |
| **Shape of the machine** | Instance Type | VM Size | Machine Type, or Custom Machine Type |
| **Bootable disk template** | AMI | Image, via Azure Compute Gallery | Image |
| **Declaration a group creates from** | Launch Template | *(part of the scale set model)* | Instance Template |
| **Self-healing, scaling group** | Auto Scaling Group | Virtual Machine Scale Sets | Managed Instance Group |
| **Interruptible discount capacity** | Spot Instance | Spot Virtual Machines | Spot VM |
| **Disk physically attached to the host** | Instance Store | Ephemeral OS Disk | Local SSD |
| **Commitment discount** | Savings Plan | Reservation | Committed Use Discount |
| **Automatic discount for just running** | *(none)* | *(none)* | Sustained Use Discount |

**Where the analogy breaks.**

- **Custom machine types are a Google Cloud answer.** You pick vCPU and memory rather than a published size, and sustained use discounts apply without any commitment.
- **Host maintenance differs.** Google Cloud live-migrates a running instance; the other two stop it and expect the group to replace it.
- **Azure subnets are regional, so the machine picks its zone** — the placement decision sits on the instance, not on the subnet as it does on AWS.
- **Spot is simplest on Google Cloud:** a fixed discount and a 30-second notice, with no bidding and no capacity pools to reason about.
- **Regional by default is a Google Cloud default.** A regional managed instance group spreads across zones unless told otherwise; an AWS Auto Scaling group spreads only across the subnets you list.

## Compute — Containers

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Managed Kubernetes** | EKS | AKS | GKE |
| **Kubernetes with nodes managed for you** | EKS with Fargate | *(none)* | GKE Autopilot |
| **Proprietary orchestrator** | ECS | *(none)* | *(none)* |
| **Run a container without a cluster** | App Runner | Container Apps | Cloud Run |
| **Container registry** | ECR | Azure Container Registry | Artifact Registry |
| **Pod-level cloud identity** | IRSA | Entra Workload ID | Workload Identity Federation for GKE |
| **Node group** | managed node group, or Karpenter | Node Pool | Node Pool |
| **Event-driven autoscaling** | *(per-service)* | KEDA, built into Container Apps | *(Cloud Run request concurrency)* |

**Where the analogy breaks.**

- **Cloud Run is central in a way App Runner is not.** It is the default home for a stateless HTTP service on Google Cloud, and Cloud Run functions are built on top of it.
- **Autopilot is not a launch type.** It is Kubernetes billed per Pod request, not a second way to run a task as Fargate is under ECS and EKS.
- **Only AWS has a proprietary orchestrator worth learning.** On the other two clouds the answer to "not Kubernetes" is the serverless container service.
- **Registry permissions catch people out on Azure:** the AKS *kubelet* identity needs the pull permission, not the cluster identity.
- **Artifact Registry is broader than ECR** — containers, language packages and OS packages in one service.

## Compute — Functions

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Function service** | Lambda | Azure Functions | Cloud Run functions |
| **What starts an invocation** | Event Source Mapping | Trigger | Trigger |
| **Declarative input and output** | *(written in code)* | Binding | *(written in code)* |
| **Stateful orchestration in code** | Step Functions, as a state machine | Durable Functions | Workflows, as YAML |
| **Requests one instance serves at once** | one | one | many |
| **Paying to avoid cold starts** | Provisioned Concurrency | Premium plan, always-ready instances | Minimum Instances |
| **Capping spend or protecting a database** | Reserved Concurrency | per-plan instance limits | Maximum Instances |
| **Shared code package** | Layer | *(app-level dependencies)* | *(container image)* |
| **Managed HTTP front door** | API Gateway | API Management | API Gateway |

**Where the analogy breaks.**

- **Concurrency is the headline difference.** One Cloud Run instance serves many requests at once; a Lambda execution environment serves exactly one. Cost models, connection pooling and the meaning of "per-instance memory" all follow from that single fact.
- **Durable Functions have no Lambda counterpart.** Orchestrators are ordinary code and must be deterministic, which is a different discipline from authoring a Step Functions state machine; Logic Apps is the low-code path Azure offers alongside.
- **Step Functions and Workflows price differently** — per state transition against per step, which changes how fine-grained a workflow it is sensible to write.

## Networking — Inside the Network

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **The private network** | VPC, regional | VNet, regional | VPC network, global |
| **Address range** | CIDR Block | Address Space | CIDR Range, on the subnet |
| **Regional slice of it** | Subnet, per zone | Subnet, regional | Subnet, regional |
| **Stateful instance-level filter** | Security Group | NSG plus ASG | Firewall Rule |
| **Stateless subnet-level filter** | Network ACL | *(none)* | *(none)* |
| **What a rule is attached by** | security group membership | subnet or interface | Network Tag or service account |
| **Inherited filter from above** | *(none)* | Azure Firewall in the hub | Hierarchical Firewall Policy |
| **Outbound access without a public IP** | NAT Gateway | NAT Gateway | Cloud NAT |
| **Route control** | Route Table | User-Defined Route | Route, on Cloud Router |
| **Private path to the cloud's own APIs** | VPC Endpoint | Service Endpoint or Private Endpoint | Private Google Access |
| **Private path to someone else's service** | PrivateLink | Private Link | Private Service Connect |

**Where the analogy breaks.**

- **The global VPC changes the shape of every answer.** Adding a region on Google Cloud needs no new network and no peering. Much of what Transit Gateway exists to solve does not arise.
- **There is no internet gateway on Azure.** Outbound access needs a NAT Gateway or another explicit method, where an AWS subnet becomes public by routing to an IGW.
- **Only AWS has two filtering layers.** NACLs are stateless and subnet-wide; the other two clouds give you one stateful mechanism with priorities. Azure NSGs support deny rules and explicit priority ordering, which AWS security groups do not.
- **Cloud NAT is not an instance.** It is a feature of the router, so there is no per-zone deployment and no bandwidth bottleneck to size.
- **Google Cloud firewall rules apply by tag or service account**, not by attachment, which makes identity-shaped network policy natural and makes "which rules hit this VM" a query rather than a lookup.

## Networking — Edge and Load Balancing

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Layer-7 load balancer** | Application Load Balancer | Application Gateway | Cloud Load Balancing, external Application Load Balancer |
| **Layer-4 load balancer** | Network Load Balancer | Load Balancer | internal and external passthrough load balancers |
| **Where backends are registered** | Target Group | backend pool | Backend Service plus Network Endpoint Group |
| **Global anycast entry point** | CloudFront plus Global Accelerator | Front Door | a single global anycast IP |
| **Content delivery** | CloudFront | Front Door caching | Cloud CDN, Media CDN |
| **Managed DNS** | Route 53 | Azure DNS plus Private DNS Zones | Cloud DNS |
| **DNS-level global routing** | Route 53 routing policies | Traffic Manager | *(the anycast IP removes the need)* |
| **Web application firewall** | WAF | WAF on Application Gateway or Front Door | Cloud Armor |
| **Liveness test** | target group health check | Health Probe | Health Check |

**Where the analogy breaks.**

- **Google Cloud's external load balancer is one global anycast IP**, not a regional endpoint fronted by DNS. Global routing stops being a DNS problem, which is why there is no Traffic Manager equivalent to learn.
- **Azure folds the edge into one service.** Front Door covers the anycast edge, caching, edge WAF and global failover, where AWS splits that across CloudFront, Global Accelerator and WAF.
- **Cloud CDN is a switch, not a distribution.** You enable it on a backend rather than configuring a separate object.
- **The Google Cloud forwarding-rule chain is more parts to assemble** — forwarding rule, target proxy, URL map, backend service — which is more setup and more places a misconfiguration can hide.
- **Private DNS is the first place to look when an Azure private endpoint misbehaves.**

## Storage and Data

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Object storage** | S3 | Blob Storage | Cloud Storage |
| **The limits and firewall boundary** | the Bucket | the Storage Account | the Bucket |
| **Cost tier of an object** | Storage Class | Access Tier | Storage Class |
| **Automatic tiering** | Intelligent-Tiering | lifecycle policy | Autoclass |
| **Time-limited URL** | Presigned URL | User-Delegation SAS | Signed URL |
| **Block disk** | EBS | Managed Disk | Persistent Disk, Hyperdisk |
| **Fast general-purpose disk tier** | gp3 | Premium SSD v2 | Hyperdisk Balanced |
| **Managed file share** | EFS, FSx | Azure Files, NetApp Files | Filestore, NetApp Volumes |
| **Managed relational database** | RDS | Azure SQL Database, Flexible Server | Cloud SQL |
| **Cloud-native relational engine** | Aurora | Hyperscale tier | AlloyDB |
| **Horizontally scalable relational** | *(none)* | *(none)* | Spanner |
| **Key-value or document store** | DynamoDB | Cosmos DB | Firestore, Bigtable |
| **In-memory cache** | ElastiCache | Azure Cache for Redis | Memorystore |
| **Analytics warehouse** | Redshift | Synapse, Fabric | BigQuery |
| **Query over object storage** | Athena | Synapse serverless SQL | BigQuery external tables |

**Where the analogy breaks.**

- **The Azure boundary sits one level up.** The storage account, not the container, carries the limits and the firewall — so capacity planning and network rules are account-shaped, which has no S3 or Cloud Storage equivalent.
- **DynamoDB maps to two Google Cloud services, not one.** Firestore for documents and queries, Bigtable for wide-column at very large scale, and neither is a drop-in for DynamoDB's model. Cosmos DB is the nearest single service, with five consistency levels and RU/s in place of separate read and write capacity.
- **Spanner has no counterpart.** Horizontally scalable relational with external consistency; the closest AWS answer is Aurora plus sharding, which is a different thing.
- **BigQuery is not a bigger Redshift.** Serverless with no cluster to size, billed by bytes scanned or reserved slots — a different mental model, and the first place a cost surprise appears.
- **Cloud Storage keeps one API across classes**, so changing class does not change how an object is read, and dual-region and multi-region buckets are native rather than replication you configure.
- **Regional Persistent Disk replicates synchronously across two zones.** EBS does not do this, so a Google Cloud single-instance design can survive a zone loss in a way its AWS translation cannot.

## Messaging and Events

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Point-to-point queue** | SQS | Service Bus, Storage Queues | Pub/Sub, one subscription on a topic |
| **Fan-out to many subscribers** | SNS | Event Grid | Pub/Sub, several subscriptions |
| **Replayable log stream** | Kinesis Data Streams, MSK | Event Hubs | Pub/Sub, with retention and seek |
| **Event bus over infrastructure changes** | EventBridge | Event Grid system topics | Eventarc, over audit logs |
| **Time a message is hidden after delivery** | Visibility Timeout | Peek-Lock | Ack Deadline |
| **Where poison messages go** | Dead-Letter Queue | Dead-Letter Queue | Dead-Letter Topic |
| **Ordering guarantee** | FIFO Queue | Session | Ordering Key |
| **Exactly-once help** | FIFO deduplication | Duplicate Detection | *(design for idempotency)* |
| **Scheduled invocation** | EventBridge Scheduler | Timer trigger, Logic Apps | Cloud Scheduler |
| **Deferred per-task dispatch** | *(SQS with a delay)* | *(queue with a scheduled time)* | Cloud Tasks |

**Where the analogy breaks.**

- **Pub/Sub is one service where AWS has three.** Queue, fan-out and replayable log are subscription settings rather than separate products, which is simpler to learn and easier to misconfigure, because retention and replay are now per-subscription choices.
- **Azure has no direct SNS equivalent.** Event Grid covers the notification case, and the queue-versus-topic split lives inside Service Bus.
- **Event Hubs speaks Kafka natively** through a protocol endpoint, which removes the MSK-versus-Kinesis decision entirely.
- **Eventarc makes any administrative change routable** by sourcing from audit logs, a reach EventBridge only has for services that publish events.

## Identity and Access

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Permission system** | IAM | Azure RBAC | IAM |
| **What a permission attaches to** | identity or resource | Scope in the hierarchy | node in the hierarchy |
| **Grant** | IAM Policy | Role Assignment | Allow Policy |
| **User-authored deny** | explicit `Deny` in a policy | *(none)* | Deny Policy, evaluated first |
| **Guardrail above the grant** | Service Control Policy | Azure Policy `Deny` | Organization Policy |
| **Identity a workload runs as** | IAM Role, via Instance Profile | Managed Identity | Service Account |
| **Taking on another identity** | `sts:AssumeRole` | *(not the model)* | Service Account Impersonation |
| **Trusting an external issuer** | OIDC Federation | Federated Credential | Workload Identity Federation |
| **Pod or app identity** | IRSA | Entra Workload ID | Workload Identity Federation for GKE |
| **Just-in-time elevation** | *(via Identity Center session)* | PIM | *(via short-lived impersonation)* |
| **Ceiling on what a grant can reach** | Permissions Boundary | *(scope plus Policy)* | IAM Condition, VPC Service Controls |
| **Credential discovery in client libraries** | default credential chain | `DefaultAzureCredential` | Application Default Credentials |

**Where the analogy breaks.**

- **Two of the three clouds cannot say "no" inside the permission system.** Azure role assignments are additive, inherit downward, and carry no user-authored deny; Google Cloud allow policies are additive with no ordinary explicit deny, and Deny Policies are a separate deliberate mechanism. AWS policy evaluation has an explicit `Deny` that always wins. This one difference reshapes how guardrails are designed on each cloud.
- **A service account is an identity object, not a role you assume.** On Google Cloud it is both a principal and a resource, so it has its own IAM policy saying who may impersonate it. The AWS equivalent of `sts:AssumeRole` is impersonation, not attachment.
- **Azure managed identities come in two kinds** — system-assigned and user-assigned — and user-assigned avoids the deploy-time race where a resource needs a permission before it exists.
- **Entra ID is the directory itself**, not a layer on top of one as IAM Identity Center is.
- **Service account keys are the single largest own-goal on Google Cloud.** `iam.disableServiceAccountKeyCreation` is the most effective one-line control on the platform.

## Encryption and Secrets

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Key management service** | KMS | Key Vault keys | Cloud KMS |
| **Key you control** | Customer Managed Key | customer-managed key in a vault | CMEK |
| **Single-tenant validated hardware** | CloudHSM | Managed HSM | Cloud HSM |
| **Key held outside the cloud** | *(external key store)* | *(BYOK import)* | Cloud EKM |
| **How bulk data is actually encrypted** | Envelope Encryption | Envelope Encryption | Envelope Encryption |
| **Who may use a key** | Key Policy plus IAM | RBAC on the vault | IAM on the key or key ring |
| **Secret store** | Secrets Manager | Key Vault | Secret Manager |
| **Config values that are not secrets** | Parameter Store | App Configuration | *(Secret Manager or config in code)* |
| **Managed TLS certificates** | ACM | Key Vault certificates | Certificate Manager |

**Where the analogy breaks.**

- **Key Vault is one service for three things** — secrets, keys and certificates — where AWS splits them across Secrets Manager, KMS and ACM. Key Vault references resolve a secret at runtime without the app calling the vault.
- **Rotation is built in on only one cloud.** Secrets Manager rotates supported databases for you; Secret Manager gives you a notification and expects your own function.
- **Cloud KMS key rings are regional and permanent** — a naming decision you cannot take back.
- **Soft delete and purge protection are Azure-specific failure modes**: a deleted vault or key lingers, and a name cannot be reused until it is purged, which breaks redeploy-from-scratch pipelines.

## Observability and Governance

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Metrics** | CloudWatch metrics | Azure Monitor metrics | Cloud Monitoring |
| **Logs** | CloudWatch Logs | Log Analytics Workspace | Cloud Logging |
| **Log query language** | Logs Insights | KQL | Log Analytics SQL |
| **Where logs must be told to go** | *(on by default per service)* | Diagnostic Setting | Log Sink |
| **Alert** | Alarm | alert rule plus Action Group | Alerting Policy |
| **Distributed tracing** | X-Ray | Application Insights | Cloud Trace |
| **Application performance monitoring** | CloudWatch Application Signals | Application Insights | Cloud Monitoring with OpenTelemetry |
| **Reliability target as an object** | *(built by hand)* | *(built by hand)* | SLO with an Error Budget |
| **Resource inventory and history** | AWS Config | Azure Resource Graph | Cloud Asset Inventory |
| **Rules with remediation** | AWS Config rules | Azure Policy | Security Command Center |
| **Recommendations across pillars** | Trusted Advisor | Azure Advisor | Recommender |
| **Shell into a machine without a bastion** | Session Manager | Azure Bastion | IAP, OS Login |

**Where the analogy breaks.**

- **Nothing logs anywhere on Azure until you create a diagnostic setting.** This is the most common "why is there no data" cause on that cloud, and it has no equivalent on the other two.
- **Azure Policy is preventative and detective; AWS Config is detective only.** The Google Cloud split is different again: Asset Inventory holds the inventory with five weeks of history, and Security Command Center holds the rules.
- **SLOs and error budgets are first-class objects on Google Cloud.** Elsewhere they are a dashboard and a convention.
- **Systems Manager has no single counterpart.** Azure spreads it across Update Manager, Automation, Run Command and Bastion; Google Cloud across OS Config, OS Login and IAP.
- **Instrument with OpenTelemetry whichever cloud you are on.** All three trace services accept it, and it is the one choice that survives a migration.

## Infrastructure as Code and Delivery

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **First-party declarative language** | CloudFormation | ARM templates, Bicep | *(deprecated; use Terraform)* |
| **Imperative code that emits it** | CDK | Bicep modules | Config Connector |
| **Hosted way to run Terraform** | *(Service Catalog)* | *(none)* | Infrastructure Manager |
| **Preview before applying** | Change Set | What-If | `terraform plan` |
| **Configuration drift** | Drift detection | Drift | state-versus-real diff |
| **Build service** | CodeBuild | Azure Pipelines, GitHub Actions | Cloud Build |
| **Deployment promotion service** | CodePipeline, CodeDeploy | Azure Pipelines environments | Cloud Deploy |
| **Traffic-shifting deployment** | CodeDeploy canary, blue/green | Deployment Slot swap | Revision traffic split |
| **Supply-chain gate** | Signer, ECR scanning | Defender for Cloud, ACR signing | Binary Authorization |

**Where the analogy breaks.**

- **Google Cloud's own declarative tool is deprecated.** Terraform is the answer on that cloud, which makes Terraform skill non-optional rather than a preference.
- **Every Azure tool compiles to the same thing.** Bicep becomes ARM JSON and everything ends at ARM, so a "Bicep problem" is usually an ARM problem.
- **Cloud Deploy is built around promoting one artifact** through ordered targets, which is a narrower and more opinionated model than CodePipeline's stage graph.
- **Deployment slots are an Azure idea.** A swap is a platform operation on App Service, not a load-balancer manoeuvre you assemble.

## Resilience and Recovery

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Zone-tolerant by configuration** | Multi-AZ, multiple subnets | Zone-Redundant | regional resource |
| **Cross-region replication of a database** | cross-Region read replica, Global Database | Failover Group | cross-region replica |
| **Managed backup service** | AWS Backup | Azure Backup | Backup and DR Service |
| **Orchestrated region failover** | *(assembled)* | Azure Site Recovery | *(assembled)* |
| **Recovery-time target** | RTO | RTO | RTO |
| **Recovery-point target** | RPO | RPO | RPO |
| **Standby pattern ladder** | Backup and Restore, Pilot Light, Warm Standby, Active-Active | the same ladder | the same ladder |
| **Division of duties with the provider** | Shared Responsibility Model | Shared Responsibility Model | Shared Responsibility Model |

**Where the analogy breaks.**

- **Zone redundancy is a property of the resource on Azure and a deployment decision on AWS.** "Zone-redundant" is a setting you tick; Multi-AZ is a topology you build from subnets and instance placement.
- **Regional services absorb the problem on Google Cloud.** A regional managed instance group, a regional disk and a regional Cloud SQL instance each survive a zone loss without a second object to manage.
- **Azure Site Recovery is a genuine gap-filler.** The other two clouds expect you to assemble region failover from replication plus DNS plus automation.
- **The pattern ladder is the one thing that is identical** on all three clouds, which is why it is worth learning once, in the vocabulary of RTO and RPO, and reciting cloud-neutrally.

---

## Reading It Without Being Caught Out

Four habits make a cross-cloud claim safe to make.

1. **Check the boundary.** A project is not an account; a subscription is not a project; a resource group has no counterpart. Most migration surprises are a boundary that moved.
2. **Check the scope.** Global, regional or zonal — and remember the default differs: an AWS or Azure network is regional, a Google Cloud network is global.
3. **Check the billing unit.** Per instance-hour, per Pod request, per request, per RU/s, per byte scanned, per state transition. Two services can do the same job and bill on different axes.
4. **Check who can say no.** Only AWS can deny inside the permission system. On the other two, guardrails live in a policy service that constrains configuration.

The service-name lookup is in [Service Names Across the Clouds](02-service-names.md), and the differences that change a design decision, rather than only a name, are in [Cross-Cloud Trade-Offs](03-trade-offs.md).
