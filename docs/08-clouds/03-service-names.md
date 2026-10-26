---
type: Guide
title: Service Names Across the Clouds
description: A lookup from an AWS service to its Azure and Google Cloud counterparts, with the difference that matters named in each row.
tags: [aws, azure, gcp, cloud, comparison]
---

A lookup table: useful for orientation, dangerous if taken literally.

- **Order.** Each row names AWS first, then Azure, then Google Cloud. AWS is the index because most readers arrive with its vocabulary, not because it is the reference implementation.
- **Grouping.** Rows are grouped like the concepts, not alphabetically, so neighbouring rows are the ones you compare in practice.
- **Accuracy.** Every mapping is approximate. Where two services differ in shape, the last column names the difference — usually the more useful half, and usually what an interviewer is probing.

---

## Accounts, Organizations and Governance

| AWS · Azure · Google Cloud | The difference that matters |
| --- | --- |
| Account · Subscription · Project | All three are the billing, quota and isolation boundary. Projects are cheap and expected to be numerous; accounts and subscriptions are not |
| Organizations OU · Management Group · Folder | Inheritance is one control among several on AWS, and the whole model on Google Cloud |
| *(none)* · Resource Group · *(none)* | A mandatory lifecycle folder with no counterpart; deleting it deletes its contents |
| Service Control Policy · Azure Policy with `Deny` · Organization Policy | SCPs filter API calls by principal; the other two constrain how a resource may be configured |
| Control Tower · landing-zone blueprints · Cloud Foundation Fabric | All three encode the layout large estates converge on anyway |
| Cost Explorer · Microsoft Cost Management · billing export to BigQuery | Only Google Cloud expects you to leave the console for a specific cost question |
| Trusted Advisor, Compute Optimizer · Azure Advisor · Recommender, Security Command Center | Recommender's IAM suggestions from observed usage have no AWS equivalent |
| AWS Config · Azure Policy, Resource Graph · Cloud Asset Inventory | Azure Policy is preventative and detective; Config is detective only; Asset Inventory is inventory, and the rules half lives in Security Command Center |

## Compute

| AWS · Azure · Google Cloud | The difference that matters |
| --- | --- |
| EC2 · Virtual Machines · Compute Engine | Azure subnets are regional, so the machine picks its zone. Google Cloud adds custom machine types and live migration by default |
| Auto Scaling group · Virtual Machine Scale Sets · Managed instance group | Regional MIGs spread across zones by default; Flexible scale sets keep instances individually addressable |
| Spot Instances · Spot Virtual Machines · Spot VMs | Google Cloud is simplest: no bidding, no capacity pools, a 30-second notice, and a variable price Google may change up to once a day (as of 2026) |
| ECS · *(none)* · *(none)* | Neither has a proprietary orchestrator; the answer is AKS or Container Apps, GKE or Cloud Run |
| Fargate · *(part of Container Apps)* · GKE Autopilot | Autopilot is Kubernetes billed per Pod request, not a launch type under a cluster |
| EKS · AKS · GKE | As of 2026, the AKS Free tier control plane carries no uptime SLA. GKE's Autopilot and container-native load balancing have no exact AWS equivalents |
| ECR · Azure Container Registry · Artifact Registry | The AKS *kubelet* identity needs the pull permission. Artifact Registry also holds language and OS packages |
| Lambda · Azure Functions · Cloud Run functions | One Cloud Run instance or Azure Functions host serves many requests at once; a standard Lambda instance serves one. Azure bindings are declarative input and output |
| App Runner · App Service, Container Apps · Cloud Run | Cloud Run is the default for stateless HTTP on its cloud; App Runner is peripheral on AWS |
| Step Functions, Lambda durable functions · Durable Functions, Logic Apps · Workflows | Both durable-function services replay ordinary code, which must be deterministic; Workflows is YAML priced per step |

## Networking

| AWS · Azure · Google Cloud | The difference that matters |
| --- | --- |
| VPC · VNet · VPC network | Global, not regional, on Google Cloud: add a region without a new network or any peering |
| Internet Gateway · *(none)* · *(default internet route)* | Azure has no internet gateway; outbound needs a NAT Gateway or another explicit method |
| Security group, NACL · NSG, ASG · Firewall rules and policies | One stateful mechanism on the other two clouds. NSGs have deny rules and priorities; Google Cloud rules apply by network tag or service account |
| NAT Gateway · NAT Gateway · Cloud NAT | Cloud NAT is a feature of the router, not an instance in a subnet: no per-zone deployment, no bandwidth bottleneck |
| ALB, NLB · Application Gateway, Load Balancer · Cloud Load Balancing | The Google external Application Load Balancer is one global anycast IP, not a regional endpoint behind DNS |
| CloudFront, Global Accelerator · Front Door · Cloud CDN, Media CDN | Front Door is one service for edge, caching, WAF and global failover. Cloud CDN is a switch on a backend, not a distribution |
| Route 53 · Azure DNS, Private DNS Zones · Cloud DNS | Private DNS is the first suspect when an Azure private endpoint misbehaves |
| Route 53 routing policies · Traffic Manager · *(anycast removes the need)* | DNS-level global routing is not a thing you assemble on Google Cloud |
| WAF · WAF on Front Door or App Gateway · Cloud Armor | Comparable; the attachment point differs |
| PrivateLink · Private Link, Private Endpoint · Private Service Connect | Azure service endpoints are a coarser free middle option with no AWS equivalent. Private Service Connect also reaches Google's own APIs privately |
| Transit Gateway · Virtual WAN · Network Connectivity Center | Hand-built hub-and-spoke is still common on Azure. A global VPC removes many cases the other two exist to solve |
| Direct Connect · ExpressRoute · Cloud Interconnect | Azure private peering reaches VNets, Microsoft peering reaches public endpoints |
| Site-to-Site VPN · VPN Gateway · Cloud VPN | Deploy Azure gateways active-active across zones; the SKU sets the ceiling |
| *(none)* · *(none)* · Shared VPC | One host project lends subnets to service projects — a consequence of the global network |

## Storage and Data

| AWS · Azure · Google Cloud | The difference that matters |
| --- | --- |
| S3 · Blob Storage · Cloud Storage | The Azure *storage account*, not the container, is the limits and firewall boundary. Cloud Storage keeps one API across all classes |
| EBS · Managed Disks · Persistent Disk, Hyperdisk | Premium SSD v2 is the gp3 equivalent. Regional Persistent Disk replicates synchronously across two zones, which EBS does not do |
| EFS, FSx · Azure Files, NetApp Files · Filestore, NetApp Volumes | Azure Files speaks SMB natively and integrates with Active Directory |
| RDS · Azure SQL Database, Flexible Server · Cloud SQL | On Azure the service tier *is* the availability model |
| Aurora · Hyperscale tier · AlloyDB | AlloyDB is PostgreSQL-compatible with separated storage, and not wire-compatible with MySQL the way Aurora is |
| *(none)* · *(none)* · Spanner | Horizontally scalable relational with external consistency. The closest AWS answer is Aurora plus sharding, which is not the same thing |
| DynamoDB · Cosmos DB · Firestore, Bigtable | Two services, not one, on Google Cloud. Cosmos DB has five consistency levels and RU/s instead of separate read and write capacity |
| ElastiCache · Azure Cache for Redis · Memorystore | The Azure Premium tier is where network integration, persistence, clustering and geo-replication appear |
| Redshift · Synapse, Fabric · BigQuery | BigQuery is serverless with no cluster to size, billed by bytes scanned or reserved slots — a different mental model, not a bigger one |
| Athena · Synapse serverless SQL · BigQuery external tables | Query over object storage in all three, with very different pricing shapes |
| OpenSearch · Azure AI Search · *(no direct equivalent)* | Azure AI Search is content search only; log search belongs to Log Analytics and KQL |

## Messaging and Events

| AWS · Azure · Google Cloud | The difference that matters |
| --- | --- |
| SQS · Service Bus, Storage Queues · Pub/Sub | A queue is a topic with one subscription on Google Cloud |
| SNS · Event Grid · Pub/Sub | Azure has no direct SNS equivalent; fan-out is a topic with several subscriptions on Google Cloud |
| Kinesis, MSK · Event Hubs · Pub/Sub | Event Hubs has a Kafka protocol endpoint built in. Pub/Sub makes retention and seek a subscription setting |
| EventBridge · Event Grid system topics · Eventarc | Eventarc sources from audit logs, so any administrative change is routable |
| *(SQS with a delay)* · *(scheduled message)* · Cloud Tasks | Per-task deferred dispatch is its own service on Google Cloud |

## Identity, Encryption and Secrets

| AWS · Azure · Google Cloud | The difference that matters |
| --- | --- |
| IAM policy · Azure RBAC role assignment · Allow policy | Additive and inherited downward on both of the others, with no user-authored deny |
| IAM role, assumed · *(not the model)* · Service account | An identity object rather than a role you assume; impersonation replaces `sts:AssumeRole` |
| Instance profile · Managed identity · Attached service account | Azure's system- versus user-assigned split avoids a deploy-time race. The Google default service account gets the Editor role unless `iam.automaticIamGrantsForDefaultServiceAccounts` is enforced — by default only in organizations created since May 2024. Use a dedicated one either way |
| IAM Identity Center · Microsoft Entra ID, PIM · Cloud Identity | Entra is the directory itself, not a layer on top of one |
| OIDC federation · Federated credential · Workload Identity Federation | Same purpose, same risk: pin the repository and branch in the attribute condition |
| KMS · Key Vault keys, Managed HSM · Cloud KMS, Cloud HSM | Key rings are regional and permanent on Google Cloud. Managed HSM is the single-tenant validated option on Azure |
| Secrets Manager · Key Vault · Secret Manager | Key Vault holds secrets, keys and certificates in one place. As of 2026, only Secrets Manager rotates supported databases for you |
| ACM · Key Vault certificates · Certificate Manager | Comparable |

## Observability and Delivery

| AWS · Azure · Google Cloud | The difference that matters |
| --- | --- |
| CloudWatch · Azure Monitor · Cloud Monitoring, Cloud Logging | Azure resource logs go nowhere until you create a diagnostic setting; the Activity Log is collected by default. Google Cloud splits metrics and logs into two services with one query surface |
| CloudWatch Logs Insights · KQL in Log Analytics · Log Analytics | SQL over a log bucket on Google Cloud, rather than a bespoke query language |
| X-Ray · Application Insights · Cloud Trace | All three take OpenTelemetry; instrument with it either way |
| CloudTrail · Activity Log · Cloud Audit Logs | Activity Log is control plane only. Google Cloud has four streams, with data access logs off by default for cost |
| Systems Manager · Update Manager, Automation, Run Command, Bastion · OS Config, OS Login, IAP | No single umbrella service on either of the others. OS Login ties SSH to IAM |
| CloudFormation, CDK · ARM templates, Bicep · Terraform | Bicep compiles to ARM JSON and everything ends at ARM. Google's own tool, Deployment Manager, reached end of support on 31 March 2026, so Terraform is the answer, hosted as Infrastructure Manager |
| CodeBuild, CodePipeline · Azure Pipelines · Cloud Build, Cloud Deploy | Cloud Deploy promotes one artifact through ordered targets |

---

Two habits make this table safe to use:

- **Check the boundary.** A project is not an account; a global VPC is not a regional one.
- **Check the billing unit.** That is where the migration surprises are.

[Cross-Cloud Trade-Offs](04-trade-offs.md) expands both.
