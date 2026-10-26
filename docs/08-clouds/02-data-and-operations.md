---
type: Guide
title: Data and Operations Across the Clouds
description: Storage, messaging, encryption, observability, delivery and resilience across AWS, Azure and Google Cloud, and where the analogy breaks.
tags: [aws, azure, gcp, cloud, comparison]
---

The second half of the concept map, after [Concepts Across the Clouds](01-concept-map.md): data, integration and operations, read the same way — a table row per concept, then where the analogy breaks.

---

## Storage and Data

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Object storage** | S3 · Blob Storage · Cloud Storage |
| **The limits and firewall boundary** | the Bucket · the Storage Account · the Bucket |
| **Cost tier of an object** | Storage Class · Access Tier · Storage Class |
| **Automatic tiering** | Intelligent-Tiering · lifecycle policy · Autoclass |
| **Time-limited URL** | Presigned URL · User-Delegation SAS · Signed URL |
| **Block disk** | EBS · Managed Disk · Persistent Disk, Hyperdisk |
| **Fast general-purpose disk tier** | gp3 · Premium SSD v2 · Hyperdisk Balanced |
| **Managed file share** | EFS, FSx · Azure Files, NetApp Files · Filestore, NetApp Volumes |
| **Managed relational database** | RDS · Azure SQL Database, Flexible Server · Cloud SQL |
| **Cloud-native relational engine** | Aurora · Hyperscale tier · AlloyDB |
| **Horizontally scalable relational** | *(none)* · *(none)* · Spanner |
| **Key-value or document store** | DynamoDB · Cosmos DB · Firestore, Bigtable |
| **In-memory cache** | ElastiCache · Azure Cache for Redis · Memorystore |
| **Analytics warehouse** | Redshift · Synapse, Fabric · BigQuery |
| **Query over object storage** | Athena · Synapse serverless SQL · BigQuery external tables |

**Where the analogy breaks.**

- **The Azure boundary sits one level up.** The storage account, not the container, carries the limits and the firewall. So capacity planning and network rules are account-shaped, which has no S3 or Cloud Storage equivalent.
- **DynamoDB maps to two Google Cloud services, not one** — Firestore for documents and queries, Bigtable for wide-column at very large scale. Neither is a drop-in for DynamoDB's model. Cosmos DB is the nearest single service, with five consistency levels and RU/s in place of separate read and write capacity.
- **Spanner has no counterpart.** It is horizontally scalable relational with external consistency. The closest AWS answer is Aurora plus sharding, which is a different thing.
- **BigQuery is not a bigger Redshift.** It is serverless with no cluster to size, billed by bytes scanned or reserved slots — a different mental model, and the first place a cost surprise appears.
- **Cloud Storage keeps one API across classes**, so changing class does not change how an object is read. Dual-region and multi-region buckets are native, not replication you configure.
- **Regional Persistent Disk replicates synchronously across two zones.** EBS does not do this, so a Google Cloud single-instance design can survive a zone loss in a way its AWS translation cannot.

**In depth.** AWS [Concepts — Data Stores](_references/aws-handbook.md#concepts--data-stores) · Azure [Concepts — Data Stores](_references/azure-handbook.md#concepts--data-stores) · Google Cloud [Concepts — Data Stores](_references/gcp-handbook.md#concepts--data-stores)

## Messaging and Events

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Point-to-point queue** | SQS · Service Bus, Storage Queues · Pub/Sub, one subscription on a topic |
| **Fan-out to many subscribers** | SNS · Event Grid · Pub/Sub, several subscriptions |
| **Replayable log stream** | Kinesis Data Streams, MSK · Event Hubs · Pub/Sub, with retention and seek |
| **Event bus over infrastructure changes** | EventBridge · Event Grid system topics · Eventarc, over audit logs |
| **Time a message is hidden after delivery** | Visibility Timeout · Peek-Lock · Ack Deadline |
| **Where poison messages go** | Dead-Letter Queue · Dead-Letter Queue · Dead-Letter Topic |
| **Ordering guarantee** | FIFO Queue · Session · Ordering Key |
| **Exactly-once help** | FIFO deduplication · Duplicate Detection · *(design for idempotency)* |
| **Scheduled invocation** | EventBridge Scheduler · Timer trigger, Logic Apps · Cloud Scheduler |
| **Deferred per-task dispatch** | *(SQS with a delay)* · *(queue with a scheduled time)* · Cloud Tasks |

**Where the analogy breaks.**

- **Pub/Sub is one service where AWS has three.** Queue, fan-out and replayable log are subscription settings, not separate products. That is simpler to learn and easier to misconfigure, because retention and replay become per-subscription choices.
- **Azure has no direct SNS equivalent.** Event Grid covers the notification case, and the queue-versus-topic split lives inside Service Bus.
- **Event Hubs speaks Kafka natively** through a protocol endpoint, which removes the MSK-versus-Kinesis decision.
- **Eventarc makes any administrative change routable** by sourcing from audit logs. EventBridge has that reach only for services that publish events.

**In depth.** AWS [Concepts — Messaging and Events](_references/aws-handbook.md#concepts--messaging-and-events) · Azure [Concepts — Messaging and Events](_references/azure-handbook.md#concepts--messaging-and-events) · Google Cloud [Concepts — Messaging and Events](_references/gcp-handbook.md#concepts--messaging-and-events)

## Encryption and Secrets

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Key management service** | KMS · Key Vault keys · Cloud KMS |
| **Key you control** | Customer Managed Key · customer-managed key in a vault · CMEK |
| **Single-tenant validated hardware** | CloudHSM · Managed HSM · Cloud HSM |
| **Key held outside the cloud** | *(external key store)* · *(BYOK import)* · Cloud EKM |
| **How bulk data is actually encrypted** | Envelope Encryption · Envelope Encryption · Envelope Encryption |
| **Who may use a key** | Key Policy plus IAM · RBAC on the vault · IAM on the key or key ring |
| **Secret store** | Secrets Manager · Key Vault · Secret Manager |
| **Config values that are not secrets** | Parameter Store · App Configuration · *(Secret Manager or config in code)* |
| **Managed TLS certificates** | ACM · Key Vault certificates · Certificate Manager |

**Where the analogy breaks.**

- **Key Vault is one service for three things** — secrets, keys and certificates. AWS splits them across Secrets Manager, KMS and ACM. Key Vault references resolve a secret at runtime without the app calling the vault.
- **Rotation is built in on only one cloud.** Secrets Manager rotates supported databases for you. Secret Manager sends a notification and expects your own function.
- **Cloud KMS key rings are regional and permanent** — a naming decision you cannot take back.
- **Deletion windows break redeploy-from-scratch pipelines.** Azure's soft delete and purge protection are the strictest form: a deleted vault or key lingers, and its name cannot be reused until it is purged. AWS has the same effect for a secret in its recovery window and for a KMS key pending deletion.

**In depth.** AWS [Concepts — Encryption and Secrets](_references/aws-handbook.md#concepts--encryption-and-secrets) · Azure [Concepts — Secrets and Keys](_references/azure-handbook.md#concepts--secrets-and-keys) · Google Cloud [Concepts — Encryption and Secrets](_references/gcp-handbook.md#concepts--encryption-and-secrets)

## Observability and Governance

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Metrics** | CloudWatch metrics · Azure Monitor metrics · Cloud Monitoring |
| **Logs** | CloudWatch Logs · Log Analytics Workspace · Cloud Logging |
| **Log query language** | Logs Insights · KQL · Log Analytics SQL |
| **Where logs must be told to go** | *(on by default per service)* · Diagnostic Setting · Log Sink |
| **Alert** | Alarm · alert rule plus Action Group · Alerting Policy |
| **Distributed tracing** | X-Ray · Application Insights · Cloud Trace |
| **Application performance monitoring** | CloudWatch Application Signals · Application Insights · Cloud Monitoring with OpenTelemetry |
| **Reliability target as an object** | Application Signals SLO · Azure Monitor SLI with a baseline target · SLO with an Error Budget |
| **Resource inventory and history** | AWS Config · Azure Resource Graph · Cloud Asset Inventory |
| **Rules with remediation** | AWS Config rules · Azure Policy · Security Command Center |
| **Recommendations across pillars** | Trusted Advisor · Azure Advisor · Recommender |
| **Shell into a machine without a bastion** | Session Manager · Azure Bastion · IAP, OS Login |

**Where the analogy breaks.**

- **Azure resource logs go nowhere until you create a diagnostic setting.** The Activity Log and platform metrics are collected by default; per-resource logs are not. This is the most common "why is there no data" cause on that cloud. The other two have no single switch like it, though some of their logs, such as flow logs, are opt-in too.
- **Azure Policy is preventative and detective; AWS Config is detective only.** Google Cloud splits it differently again: Asset Inventory holds the inventory with five weeks of history (as of 2026), and Security Command Center holds the rules.
- **SLOs and error budgets are first-class objects on all three.**
  - Google Cloud has had them longest.
  - CloudWatch Application Signals defines SLOs with error budgets.
  - Azure Monitor added SLIs with an SLO target, error budget and burn-rate alerts in 2026, scoped to a service group.
- **Systems Manager has no single counterpart.** Azure spreads it across Update Manager, Automation, Run Command and Bastion; Google Cloud across OS Config, OS Login and IAP.
- **Instrument with OpenTelemetry on any cloud.** All three trace services accept it, and it is the one choice that survives a migration.

**In depth.** AWS [Concepts — Observability and Governance](_references/aws-handbook.md#concepts--observability-and-governance) · Azure [Concepts — Governance](_references/azure-handbook.md#concepts--governance) · Google Cloud [Concepts — Observability and Governance](_references/gcp-handbook.md#concepts--observability-and-governance)

## Infrastructure as Code and Delivery

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **First-party declarative language** | CloudFormation · ARM templates, Bicep · *(Deployment Manager, end of support 31 March 2026; use Terraform)* |
| **Imperative code that emits it** | CDK · Bicep modules · Config Connector |
| **Hosted way to run Terraform** | *(Service Catalog)* · *(none)* · Infrastructure Manager |
| **Preview before applying** | Change Set · What-If · `terraform plan` |
| **Configuration drift** | Drift detection · Drift · state-versus-real diff |
| **Build service** | CodeBuild · Azure Pipelines, GitHub Actions · Cloud Build |
| **Deployment promotion service** | CodePipeline, CodeDeploy · Azure Pipelines environments · Cloud Deploy |
| **Traffic-shifting deployment** | CodeDeploy canary, blue/green · Deployment Slot swap · Revision traffic split |
| **Supply-chain gate** | Signer, ECR scanning · Defender for Cloud, ACR signing · Binary Authorization |

**Where the analogy breaks.**

- **Google Cloud's own declarative tool has reached end of support.** Deployment Manager's support ended on 31 March 2026, so Terraform is the answer on that cloud. That makes Terraform skill required, not a preference.
- **Every Azure tool compiles to the same thing.** Bicep becomes ARM JSON and everything ends at ARM, so a "Bicep problem" is usually an ARM problem.
- **Cloud Deploy is built around promoting one artifact** through ordered targets — a narrower, more opinionated model than CodePipeline's stage graph.
- **Deployment slots are an Azure idea.** A swap is a platform operation on App Service, not a load-balancer manoeuvre you assemble.

**In depth.** AWS [Concepts — Infrastructure as Code and Delivery](_references/aws-handbook.md#concepts--infrastructure-as-code-and-delivery) · Azure [Concepts — Infrastructure as Code and Delivery](_references/azure-handbook.md#concepts--infrastructure-as-code-and-delivery) · Google Cloud [Concepts — Infrastructure as Code and Delivery](_references/gcp-handbook.md#concepts--infrastructure-as-code-and-delivery)

## Resilience and Recovery

| Concept | AWS · Azure · Google Cloud |
| --- | --- |
| **Zone-tolerant by configuration** | Multi-AZ, multiple subnets · Zone-Redundant · regional resource |
| **Cross-region replication of a database** | cross-Region read replica, Global Database · Failover Group · cross-region replica |
| **Managed backup service** | AWS Backup · Azure Backup · Backup and DR Service |
| **Orchestrated region failover** | *(assembled)* · Azure Site Recovery · *(assembled)* |
| **Recovery-time target** | RTO · RTO · RTO |
| **Recovery-point target** | RPO · RPO · RPO |
| **Standby pattern ladder** | Backup and Restore, Pilot Light, Warm Standby, Active-Active · the same ladder · the same ladder |
| **Division of duties with the provider** | Shared Responsibility Model · Shared Responsibility Model · Shared Responsibility Model |

**Where the analogy breaks.**

- **Zone redundancy is a property of the resource on Azure and a deployment decision on AWS.** "Zone-redundant" is a setting you tick; Multi-AZ is a topology you build from subnets and instance placement.
- **Regional services absorb the problem on Google Cloud.** A regional managed instance group, a regional disk and a regional Cloud SQL instance each survive a zone loss without a second object to manage.
- **Azure Site Recovery fills a real gap.** The other two clouds expect you to assemble region failover from replication plus DNS plus automation.
- **The pattern ladder is the one thing identical on all three clouds.** Learn it once, in the vocabulary of RTO and RPO, and recite it cloud-neutrally.

**In depth.** AWS [Concepts — Resilience and Responsibility](_references/aws-handbook.md#concepts--resilience-and-responsibility) · Azure [Concepts — Resilience and Recovery](_references/azure-handbook.md#concepts--resilience-and-recovery) · Google Cloud [Concepts — Resilience and Recovery](_references/gcp-handbook.md#concepts--resilience-and-recovery)

---

## Reading It Without Being Caught Out

Four habits make a cross-cloud claim safe:

1. **Check the boundary.** A project is not an account; a subscription is not a project; a resource group has no counterpart. Most migration surprises are a boundary that moved.
2. **Check the scope.** Global, regional or zonal — and remember the default differs: an AWS or Azure network is regional, a Google Cloud network is global.
3. **Check the billing unit.** Per instance-hour, per Pod request, per request, per RU/s, per byte scanned, per state transition. Two services can do the same job and bill on different axes.
4. **Check who can say no.** Only AWS can deny inside the permission system. On the other two, guardrails live in a policy service that constrains configuration.

The service-name lookup is in [Service Names Across the Clouds](03-service-names.md). The differences that change a design decision, not only a name, are in [Cross-Cloud Trade-Offs](04-trade-offs.md).
