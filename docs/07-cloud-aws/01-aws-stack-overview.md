---
type: Guide
title: AWS Services Overview
description: The AWS service catalog — compute, networking, storage and data, messaging and events, identity, and monitoring.
tags: [aws, cloud, services, devops]
---

# AWS Services Overview

A catalog of the AWS services an infrastructure or platform engineer chooses between, grouped into foundations, compute, networking, storage and data, messaging and events, identity, and monitoring.

Each entry gives what the service actually is, its **entry point** — the first object you create, the one that makes the rest of the service make sense — and the constraint that most often catches people out.

## Compute

### EC2 — Rented Virtual Machines

Raw Linux/Windows VMs billed per second, with a hypervisor you never see.

- **Entry point:** an **AMI** (the disk image) + an **instance type** (the hardware shape), wrapped in a **launch template**. In production you rarely launch an instance directly — you point an **Auto Scaling Group** at a launch template and let it create and replace instances for you.
- **Instance families:** family letters encode purpose — `m` general, `c` compute-optimized, `r` memory-optimized, `t` burstable (CPU credits), and `g`/`p` GPU. A `g` *suffix* (`m7g`, `c7g`) means **Graviton**, AWS's own Arm silicon. **Nitro** is the offload card plus minimal hypervisor behind all current-generation instances; it is why EBS encryption and near-bare-metal network performance are included.
- **Storage choice:** EBS-backed root (network disk, survives stop/start) vs. **instance store** (physically attached NVMe, very fast, *erased when the instance stops*).
- **Placement groups:** `cluster` (packed in one AZ for lowest latency), `spread` (deliberately separate hardware), and `partition` (rack-aware, for HDFS/Cassandra-style systems).
- **Trap:** stopping an instance releases its public IP unless you attached an Elastic IP, and destroys instance-store data. Immutable infrastructure — covered in the [AWS interview prep guide](02-aws-interview-prep.md) — exists because mutating long-lived instances is how fleets drift.

### ECS — AWS's Own Container Orchestrator

Simpler than Kubernetes, deeply wired into IAM, ALB, and CloudWatch. If you do not need the Kubernetes ecosystem, this is the cheaper answer.

- **Entry point:** a **task definition** — the container spec (image, CPU/memory, env, log driver, IAM roles). A **service** keeps *N* copies of that task running and registers them with a load balancer. Both live in a **cluster**, which is a namespace plus capacity.
- **Launch types:** **EC2** (you own and patch the nodes, cheaper at steady high utilization) vs. **Fargate** (no nodes at all, billed per vCPU-second and GB-second). **Capacity providers** let one cluster mix Fargate, Fargate Spot, and an ASG with weights.
- **The two roles:** the **task role** is what *your application code* can call; the **task execution role** is what the *ECS agent* uses to pull the ECR image and ship logs. Confusing them is the most common ECS IAM bug.
- **Trap:** `awsvpc` network mode gives every task its own ENI with a real VPC IP — elegant, but you hit per-instance ENI limits and subnet IP exhaustion long before you hit CPU limits.

#### Fargate — The Serverless Data Plane

Not a service you cluster, a **capacity type**. You hand AWS a task definition; it runs the containers on its own fleet of Firecracker micro-VMs. No AMI, no ASG, no patching, and no node to SSH into — and no node to over-provision either.

- **Entry point:** selecting `FARGATE` as the launch type (or, better, a **capacity provider**) on an ECS service. The sizing dial is the **task-level CPU/memory pair**, and it comes from a fixed matrix of supported combinations rather than arbitrary values, which is the first thing that surprises people migrating from EC2.
- **Billing and networking:** billing is per vCPU-second and GB-second, from **image pull start** to task stop, with a one-minute minimum. `awsvpc` is the *only* network mode, so every task gets its own ENI and VPC IP. Ephemeral task storage has a default size and a configurable ceiling; anything that must outlive the task goes to **EFS**. **Arm64/Graviton** and Windows containers are both supported, and **Fargate Spot** trades a two-minute SIGTERM for a lower rate.
- **What you give up:** privileged containers, host access, GPUs, daemonsets, and any sidecar pattern that assumes a shared node. Debugging is **ECS Exec** (SSM under the hood), never SSH.
- **In EKS:** the same engine appears as a **Fargate profile** that matches pods by namespace and labels. Same trade: one pod per micro-VM, no daemonsets — which means your log and metrics agents have to become sidecars.
- **Trap:** the cost crossover. Per vCPU-hour Fargate costs more than EC2, so a steadily loaded, well-packed fleet is cheaper on EC2 — Fargate wins on **bursty, spiky, or low-headcount** workloads where operator time is the real cost. The second trap is scale-out latency: Fargate keeps no local image cache between tasks, so a cold task start includes an image pull. **SOCI (Seekable OCI)** lazy loading exists to avoid pulling the whole image; ECS on EC2 caches images on the node instead.

### EKS — Managed Kubernetes

AWS runs the control plane (etcd, API server) across AZs; everything else is standard upstream Kubernetes.

- **Entry point:** the **cluster** (control plane, billed hourly) plus a *data plane decision*: **managed node groups** (ASGs AWS keeps in sync), **Karpenter** (provisions right-sized nodes directly from pending pods — AWS-originated, now CNCF, and the modern default), or **Fargate profiles** (per-pod, no nodes).
- **Two auth planes meet here:** IAM says who can call the EKS API; Kubernetes RBAC says what they can do inside the cluster. The mapping is now the **access entries** API, which replaced hand-editing the `aws-auth` ConfigMap.
- **Pods calling AWS APIs:** **IRSA** (cluster OIDC provider plus a role whose trust policy matches a service account) or the newer **EKS Pod Identity** (an agent, no per-cluster OIDC setup, simpler trust policies). Both beat giving the whole node role broad permissions.
- **Trap:** the **VPC CNI** gives every pod a routable VPC IP, so a busy cluster exhausts subnet CIDRs. Fixes: **prefix delegation**, secondary CIDR ranges, or larger instances with more ENI slots. Plan IP space *before* the cluster exists.

### Lambda — Functions, No Servers

You upload a handler; AWS runs it in a micro-VM (Firecracker) only when something invokes it.

- **Entry point:** a **handler** plus an **event source** — API Gateway or an ALB target group, an S3 notification, an SQS queue, EventBridge, a Kinesis shard, or a bare Function URL. The event source shapes everything: the event JSON, the retry semantics, and whether failures go to a DLQ.
- **Execution model:** one execution environment handles exactly **one invocation at a time**; scaling means more environments. That is why globals persist between invocations — useful for connection reuse, dangerous for state.
- **Concurrency:** **reserved** concurrency both *caps* a function and *guarantees* it capacity; **provisioned** concurrency keeps environments pre-initialized to eliminate cold starts, and bills while idle. **SnapStart** (Java, .NET, Python) restores a pre-warmed snapshot instead.
- **Limits that shape design:** a maximum runtime per invocation, a memory ceiling that also sets CPU (memory is the only performance dial), a bounded `/tmp`, and a synchronous payload cap. Read the current service quotas before designing against any of them.
- **Trap:** databases. Thousands of concurrent environments each opening a connection will exhaust RDS — that is what **RDS Proxy** exists for.

### App Runner / Elastic Beanstalk / Lightsail — The "Just Run My App" Tier

- **App Runner:** point it at a container image or a source repo and get an HTTPS URL with autoscaling and scale-to-near-zero. No VPC, ALB, or cluster to design.
- **Elastic Beanstalk:** the older version of the same idea — it generates a CloudFormation stack of EC2 + ASG + ELB behind the scenes, and you can drop to those resources when you outgrow it.
- **Lightsail:** fixed-price VPS with predictable billing, aimed at small sites.
- **When to reach for them:** they trade control for setup time. A workload with no VPC integration, no sidecars, and no custom scheduling rarely justifies EKS.

## Networking

### VPC, Subnets & Routing — The Foundation Everything Else Sits In

A software-defined network you own, defined by a CIDR block.

- **Entry point:** the **CIDR block**, then **subnets** (each pinned to one AZ), then **route tables**. There is no "public subnet" checkbox — a subnet is public *because* its route table sends `0.0.0.0/0` to an **Internet Gateway**.
- **Private egress:** a **NAT Gateway** (one per AZ for resilience) lets private subnets reach the internet outbound only. For IPv6 the equivalent is the **egress-only IGW**.
- **Trap:** NAT Gateway is billed hourly *and* per GB processed, and it is a common source of unexpected cost. Traffic to S3, ECR, and DynamoDB should go through VPC endpoints instead — see **PrivateLink & VPC Endpoints** below.

### Security Groups vs. NACLs — The Two Firewalls

| Aspect | Security Group | Network ACL |
| --- | --- | --- |
| **Attaches to** | An ENI (instance, task, endpoint) | A subnet |
| **State** | **Stateful** — return traffic is automatic | **Stateless** — you must allow the return path explicitly |
| **Rules** | Allow only | Allow **and** deny, evaluated in number order |
| **Default** | Deny all inbound, allow all outbound | Allow all both ways |

- **Entry point:** the idiomatic AWS pattern is **a security group referencing another security group** — `sg-database` allows port 5432 *from `sg-app`*, not from an IP range. It keeps working as instances scale in and out.
- **Use NACLs for:** coarse subnet-wide denials, such as blocking a CIDR outright. Reaching for NACLs to do ordinary application access control is a smell.

### Elastic Load Balancing — ALB, NLB, and GWLB

- **Entry point:** a **listener** (port + protocol) → **rules** → a **target group** (a set of instances, IPs, or Lambda functions with a health check). The target group, not the load balancer, is where health checking and draining actually happen.

| Load balancer | Layer | Use it for |
| --- | --- | --- |
| **ALB** | 7 (HTTP) | Path/host routing, weighted target groups for canaries, OIDC auth at the edge, and WebSockets |
| **NLB** | 4 (TCP/UDP) | Extreme throughput, static IPs per AZ, non-HTTP protocols, and preserving source IP |
| **GWLB** | 3 (GENEVE) | Transparently inserting third-party firewall or inspection appliances into the path |

### CloudFront — The Global Edge

A CDN that is also the front door for TLS, WAF, and DDoS protection.

- **Entry point:** a **distribution** with one or more **origins** (an S3 bucket via **OAC**, an ALB, or any HTTP server) and cache behaviors that map path patterns to origins.
- **Edge compute:** **CloudFront Functions** (sub-millisecond, JavaScript, viewer request/response only — header rewrites and redirects) vs. **Lambda@Edge** (full runtime, origin-side, heavier).
- **Trap:** an ACM certificate used by CloudFront **must live in `us-east-1`**, regardless of where everything else is.

### Route 53 — DNS and Health Checking

- **Entry point:** a **hosted zone** — **public** (authoritative on the internet) or **private** (resolvable only from the VPCs you associate it with).
- **Routing policies:** simple, **weighted** (canary and blue-green traffic splits), **latency**, **failover** (paired with health checks), geolocation, geoproximity, IP-based, and multivalue.
- **Alias records:** they point at AWS resources, are free to query, and work at the **zone apex** — which is why you cannot CNAME `example.com` to an ALB. DNS forbids CNAME at the apex; alias is AWS's answer.

### Transit Gateway, VPC Peering & Cloud WAN — Connecting VPCs

- **VPC Peering:** a 1:1 link between two VPCs. Cheap, no bandwidth bottleneck, and **non-transitive** — A↔B and B↔C does *not* give you A↔C. Fine for a handful of VPCs; a full mesh of *n* VPCs needs *n(n−1)/2* peerings, which is why it does not scale.
- **Transit Gateway:** a regional hub. Every VPC, VPN, and Direct Connect gets an **attachment**, and **TGW route tables** decide which attachments can reach which — that is how you build hub-and-spoke with centralized inspection. Billed per attachment-hour plus per GB.
- **Cloud WAN:** a policy-driven global layer that manages TGWs and inter-region peering for you, for genuinely multi-region estates.
- **Trap, for all three:** overlapping CIDRs. Nothing routes between two VPCs that both use `10.0.0.0/16`. Plan address space centrally with **VPC IPAM** before it becomes a migration.

### Direct Connect & Site-to-Site VPN — Reaching On-Prem

- **Site-to-Site VPN:** IPsec tunnels over the public internet. Live in minutes, but bandwidth and jitter follow the internet.
- **Direct Connect:** a dedicated private circuit into an AWS facility. Consistent latency and lower per-GB cost, with a **lead time measured in weeks**.
- **The standard pattern:** DX for the primary path, VPN as the automatic backup.

### PrivateLink & VPC Endpoints — Reaching AWS Services Privately

- **Gateway endpoints:** **S3 and DynamoDB only**. They are a *route table entry*, and they are **free**. There is no good reason not to have them.
- **Interface endpoints:** an **ENI with a private IP in your subnet** for a specific service (ECR, SSM, Secrets Manager, KMS, and others). Billed hourly per AZ plus per GB, but they keep traffic off the NAT Gateway, which often makes them the cheaper option.
- **PrivateLink** (endpoint services): publish *your own* service behind an NLB so other VPCs and accounts consume it through their own endpoint — no peering, no route sharing, and overlapping CIDRs stop mattering. This is the SaaS-on-AWS connectivity pattern.

## Storage & Data

### S3 — Object Storage

Not a filesystem. A flat key-value store of immutable objects with a global bucket namespace.

- **Entry point:** a **bucket** plus a **key**. Prefixes look like directories but are not — though they *do* partition request throughput, so spreading keys across prefixes raises the ceiling.
- **Storage classes:** Standard → Standard-IA / One Zone-IA (cheaper storage, per-GB retrieval fee, minimum durations) → Glacier Instant, Flexible, and Deep Archive. **Intelligent-Tiering** moves objects automatically for a small monitoring fee and is the low-risk default when access patterns are unknown.
- **Durability and control:** **versioning** (plus MFA delete) protects against overwrite and deletion; **Object Lock** gives WORM retention for audit logs; **lifecycle policies** handle transition and expiry, including expiring old *versions*, which people forget until the bill arrives.
- **Access:** **Block Public Access** is on by default at the account level and overrides everything beneath it. Prefer **bucket policies** and IAM; ACLs are disabled by default now (`Bucket owner enforced`) and should stay that way.
- **Read consistency:** reads have been **strongly consistent** since 2020. Guidance written before that describes eventual consistency and is out of date.

### EBS — Block Storage for One Instance

Network-attached virtual disks that behave like local ones.

- **Entry point:** a **volume** in a specific AZ, attached to one instance (io2 supports multi-attach). AZ-bound: to move it, snapshot it.
- **gp3 vs. gp2:** gp2's IOPS were tied to volume size, so people over-provisioned capacity to buy performance. **gp3 decouples them** — a baseline of 3,000 IOPS and 125 MB/s at any size, tunable independently of capacity. Migrating gp2 → gp3 is a no-downtime modification.
- **io2 / io2 Block Express** for databases needing sustained high IOPS and higher durability.
- **Snapshots** are incremental, stored in S3, and *regional* — the standard cross-AZ and cross-region recovery mechanism.

### EFS & FSx — Shared Filesystems

- **EFS:** managed NFS. Multi-AZ, grows and shrinks automatically, and mountable by many instances or containers at once. Use it when things genuinely need shared POSIX read-write. Lifecycle policies move cold files to IA.
- **FSx:** managed *third-party* filesystems — **Windows File Server** (SMB, AD-integrated), **Lustre** (HPC, links directly to S3), **NetApp ONTAP**, and **OpenZFS**.
- **Caveat:** shared filesystems are often a lift-and-shift compromise. Cloud-native usually means S3 plus a database.

### RDS & Aurora — Managed Relational Databases

- **Entry point:** RDS gives you a **DB instance** running stock Postgres, MySQL, SQL Server, Oracle, or MariaDB. Aurora gives you a **DB cluster** — AWS's own storage engine that replicates six ways across three AZs, with compute nodes sharing it.
- **HA vs. scale:** **Multi-AZ** is *availability*. It maintains a standby that serves **no traffic** and fails over automatically; the Multi-AZ *cluster* variant is the exception, with two readable standbys. **Read replicas** are *scale*: asynchronous, laggy, and promoted manually. The two solve different problems and are not substitutes.
- **Aurora specifics:** storage auto-grows without provisioning, multiple read replicas share the same storage volume (so failover takes seconds rather than minutes), **Serverless v2** scales capacity in ACUs without swapping instances, and **Global Database** handles cross-region replication.
- **RDS Proxy:** pools and multiplexes connections — the standard fix when Lambda concurrency overwhelms Postgres.

### DynamoDB — Managed Key-Value at Any Scale

Single-digit millisecond reads regardless of table size, if and only if you model it correctly.

- **Entry point:** a **table** and its **partition key**, optionally plus a **sort key**. The order of work is inverted from SQL: you list your access patterns *first*, then design a key that serves them. There is no "add a JOIN later".
- **Indexes:** a **GSI** has a different partition key, its own capacity, and eventual consistency — you can add one at any time. An **LSI** shares the partition key, must be created *with the table*, and caps that item collection at 10 GB.
- **Capacity:** **on-demand** (pay per request, absorbs spikes, no planning) vs. **provisioned** plus autoscaling (cheaper at steady predictable load).
- **Extras:** **DAX** for microsecond cached reads; **Streams** → Lambda for change-data-capture; TTL for automatic expiry; and global tables for multi-region active-active.
- **Trap:** a **hot partition** — a key like `status#PENDING` concentrates all traffic on one partition and throttles while the table sits mostly idle.

### ElastiCache & OpenSearch — The Supporting Data Stores

- **ElastiCache:** managed **Redis/Valkey** or Memcached. Entry point is a **cluster endpoint**; *cluster mode disabled* is one shard with replicas, *enabled* is sharded across many. **Valkey** is the cheaper post-fork default — the fork, and the 2024 relicensing that caused it, are explained in [Redis — Core Concepts and Workflow](../03-system-design/03-caching.md#redis--core-concepts-and-workflow). Used for cache-aside, sessions, rate limits, and distributed locks.
- **OpenSearch:** managed search and log analytics, the Elasticsearch fork. Entry point is a **domain** (a cluster you size) or a **serverless collection**. Reach for it when CloudWatch Logs Insights is no longer enough — full-text search, dashboards, and long retention.

## Messaging & Events

SQS buffers work, SNS fans one message out to many subscribers, EventBridge routes on event content, and Kinesis and MSK keep a replayable log.

### SQS — The Buffer

- **Entry point:** a **queue URL**, a **visibility timeout** (it must exceed your handler's runtime, or the message is redelivered mid-processing), and a **dead-letter queue** with `maxReceiveCount`. Consumers **pull**; use long polling.
- **Standard** — at-least-once, best-effort ordering, and effectively unlimited throughput. **FIFO** — strict ordering *per message group ID*, plus deduplication that yields exactly-once processing **within the 5-minute deduplication interval**. FIFO's base throughput limits are far below Standard's, though **high-throughput mode** raises them substantially.
- **Use it to:** decouple producers from consumers and absorb bursts. Messages disappear once acknowledged.

### SNS — The Fan-Out

- **Entry point:** a **topic**, then subscriptions (SQS, Lambda, HTTPS, email, SMS, or mobile push). **Push**-based, millisecond delivery.
- **The standard pattern:** **SNS → multiple SQS queues.** Each consumer gets its own buffer, its own retry policy, and its own failure isolation. Subscribing Lambdas straight to SNS gives you none of that.

### EventBridge — The Router

- **Entry point:** an **event bus**. The **default bus** already carries events from AWS services themselves, which makes it *the* way to react to infrastructure changes ("an instance entered `stopping`", "a Config rule went non-compliant"). **Rules** match on event *content*, not just topic.
- Also carries **Scheduler** (cron and rate schedules at scale, the modern replacement for CloudWatch Events rules) and **Pipes** (point-to-point source → filter → enrich → target).
- **vs. SNS:** richer routing, a schema registry, cross-account buses, and archive and replay — at somewhat higher latency. Choose EventBridge for *routing logic*, SNS for *raw fan-out speed*.

### Kinesis Data Streams & MSK — The Log

- **Kinesis:** an ordered, **replayable** stream of records split into **shards**. Consumers track their own position and can rewind, with retention configurable up to 365 days, and multiple independent consumers read the same data. That replay ability is the core difference from SQS, where an acknowledged message is gone. **Firehose** is the no-code delivery variant into S3, OpenSearch, or Redshift.
- **MSK:** managed Apache Kafka, for when you need the Kafka *protocol* and ecosystem (Connect, Streams, existing tooling) rather than just a stream. **MSK Serverless** removes broker sizing.

## Identity

### IAM — The Policy Engine Underneath Everything

- **Entry point:** the **policy evaluation logic** — **explicit `Deny` > explicit `Allow` > implicit deny**. For cross-account access, *both* the identity policy and the resource policy must allow the call.
- **Policy types:** identity-based (attached to a role, user, or group), resource-based (on the bucket, queue, or key), **permission boundaries** (the ceiling on what a role *can* be granted), and **SCPs** (organization-level filters that **never grant**, only restrict — so an SCP allowing everything grants nothing).
- **A role has two policies:** the **trust policy** (*who may assume me*) and the **permissions policy** (*what I can do once assumed*). Almost every "access denied and I cannot see why" turns out to be the trust policy.

### IAM Roles in Practice — The Compute-to-AWS Bridge

The AWS answer to managed identity: no long-lived credentials anywhere.

- **Entry point per compute type:** **instance profile** for EC2, **task role** for ECS, **IRSA / Pod Identity** for EKS pods, and **execution role** for Lambda. The SDK finds temporary credentials automatically via the credential provider chain.
- **On EC2:** those credentials come from the **instance metadata service** — enforce **IMDSv2** (session-token required), because IMDSv1's simple GET is what turns an SSRF bug into stolen cloud credentials.

### IAM Identity Center — How Humans Log In

Formerly AWS SSO. The replacement for long-lived IAM users with access keys.

- **Entry point:** connect an **identity source** (the built-in directory, or Entra ID or Okta via SAML plus SCIM provisioning), define **permission sets** (reusable policy bundles), then **assign** `group × account × permission set`.
- **Result:** `aws sso login` yields short-lived credentials, one portal across every account, and access that disappears when HR deprovisions the user.

### OIDC Federation for CI/CD — Keyless Pipelines

- **Entry point:** register the provider once (`token.actions.githubusercontent.com` for GitHub Actions), then create a role whose **trust policy conditions on the token's `sub` claim**, scoped to a specific repo *and* branch or environment. The pipeline exchanges its short-lived OIDC token for AWS credentials.
- **Why it matters:** it removes the entire category of leaked long-lived CI keys.

### STS — The Token Service

- **Entry point:** `AssumeRole` — every pattern above terminates here. Also `AssumeRoleWithWebIdentity` (OIDC and IRSA) and `AssumeRoleWithSAML`.
- **Cross-account:** the role lives in the *target* account and trusts the *source* account; the source identity needs `sts:AssumeRole` permission. Both halves are required.
- **External ID:** when a third party such as a monitoring SaaS assumes a role in your account, require an external ID. It defends against the **confused deputy** problem.

### KMS — Key Management and Envelope Encryption

- **Entry point:** a **customer-managed key (CMK)** and its **key policy**. Unlike most services, the *key policy is the root of trust* — IAM permissions alone are not enough unless the key policy delegates to IAM.
- **Envelope encryption:** services call `GenerateDataKey`, encrypt the payload locally with the plaintext data key, store the *encrypted* data key alongside the ciphertext, and discard the plaintext. That is how S3, EBS, and RDS encrypt terabytes with a key that never leaves KMS.
- **Also:** **grants** for temporary programmatic delegation, **automatic key rotation** (a configurable 90 to 2,560 days since 2024, where the period used to be fixed at the 365-day default), **multi-Region keys** for cross-region replicas, and a mandatory **7–30 day waiting period** on key deletion — there is no immediate delete, by design.

## Monitoring & Management

### CloudWatch — Metrics, Logs, and Alarms

- **Entry point:** a **metric**, identified by namespace, name, and **dimensions**. Dimensions are part of the identity, so a typo creates a *new* metric rather than an error — a common source of "my alarm never fires".
- **Alarms:** threshold or **metric math**, with `M out of N` datapoints to suppress flapping; **composite alarms** combine several to cut noise. Missing-data handling is an explicit setting and usually wrong by default.
- **Logs:** log group → log stream. **Retention defaults to "never expire"** — set it on day one; forgotten log groups are a reliably large bill line. Query with **Logs Insights**.
- **EMF (Embedded Metric Format):** write a specially structured JSON log line and CloudWatch extracts custom metrics from it — no separate `PutMetricData` call, and no added latency in your request path.

### X-Ray & ADOT — Distributed Tracing

- **Entry point:** a **trace** made of **segments** and subsegments, stitched into a **service map** that shows latency and errors per hop. **Sampling rules** control cost.
- **ADOT** is AWS's supported **OpenTelemetry** distribution. Instrument with OpenTelemetry and export to X-Ray or to a third-party backend, rather than locking instrumentation to one vendor.

### CloudTrail — The Audit Log

The "who did this, from where, and when" service.

- **Entry point:** **management events** — control-plane API calls, recorded by default and viewable free in the console for 90 days. **Data events** (S3 object-level GETs, Lambda invocations) are high volume, **off by default**, and billed, so turning them on selectively is a real decision.
- **The organization pattern:** an **organization trail** writing to a locked-down **log archive account** with S3 Object Lock, so nobody — including an account admin — can erase their own tracks.
- **Boundary to state:** CloudTrail records *API calls*. For "what did this resource look like on Tuesday", that is Config.

### AWS Config — Configuration History and Compliance

- **Entry point:** enable the **configuration recorder** per account and region; it snapshots every supported resource on change, giving you a timeline you can diff.
- **Rules:** managed or custom checks (Lambda or Guard) — "is every EBS volume encrypted?" — bundled into **conformance packs**, with **remediation actions** wired to SSM Automation documents to fix violations automatically.
- **Aggregators** roll all accounts and regions into one compliance view.

### Systems Manager — Fleet Management

An umbrella over a dozen capabilities; the ones that matter here:

- **Entry point:** the **SSM Agent** (pre-installed on current AMIs) plus an instance profile granting `AmazonSSMManagedInstanceCore`. That is the whole onboarding.
- **Session Manager:** a browser or CLI shell **without SSH, without port 22, without a bastion host, and without a key pair** — with every session logged to CloudTrail and optionally recorded to S3.
- **Also:** **Patch Manager** (patch baselines plus maintenance windows), **Run Command** (ad-hoc at fleet scale), **State Manager** (associations are *continuous* enforcement, not one-shot), **Automation** runbooks, **Parameter Store** (config and SecureStrings), and **Inventory**.

### Trusted Advisor, Health Dashboard & Compute Optimizer — The Advisory Layer

- **Trusted Advisor:** automated checks across cost, security, fault tolerance, performance, and **service limits**. The full check set requires Business or Enterprise support.
- **AWS Health Dashboard:** events affecting *your* account specifically — scheduled maintenance, degraded resources, and EOL notices. Wire it to EventBridge instead of reading it manually.
- **Compute Optimizer:** machine-learning right-sizing recommendations for EC2, ASGs, EBS, Lambda memory, and Fargate tasks, based on your actual CloudWatch history. This is where a cost-reduction review should start; see the [AWS interview prep guide](02-aws-interview-prep.md) for how that conversation is structured.
