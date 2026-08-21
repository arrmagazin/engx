---
type: Guide
title: AWS Services overview
description: AWS core services, networking, storage, identity, and DevOps.
tags: [interview, aws, cloud, devops]
---

# AWS Services overview

A study map organized around the five competency areas that show up in almost every AWS infrastructure job description. 

Each service below follows the same shape: **what it actually is**, the **entry point** (the first object you create — the thing that makes the rest of the service make sense), what to **know cold**, and the **trap** interviewers probe for.

## Compute

### EC2 — rented virtual machines

Raw Linux/Windows VMs billed per second, with a hypervisor you never see.

- **Entry point:** an **AMI** (the disk image) + an **instance type** (the hardware shape), wrapped in a **launch template**. In production you almost never launch an instance directly — you point an **Auto Scaling Group** at a launch template and let it create and replace instances for you.
- **Know cold:** family letters encode purpose — `m` general, `c` compute-optimised, `r` memory-optimised, `t` burstable (CPU credits), `g`/`p` GPU. A `g` *suffix* (`m7g`, `c7g`) means **Graviton** — AWS's own ARM silicon, typically ~20% cheaper for equivalent work. **Nitro** is the offload card + minimal hypervisor behind all modern instances; it's why EBS encryption and near-bare-metal network performance are free.
- **Storage choice:** EBS-backed root (network disk, survives stop/start) vs **instance store** (physically attached NVMe, extremely fast, *erased when the instance stops*).
- **Placement groups:** `cluster` (packed in one AZ for lowest latency), `spread` (deliberately separate hardware), `partition` (rack-aware, for HDFS/Cassandra-style systems).
- **Trap:** stopping an instance releases its public IP unless you attached an Elastic IP, and destroys instance-store data. "Immutable" thinking (§4) exists because mutating long-lived instances is how fleets drift.

### ECS — AWS's own container orchestrator

Simpler than Kubernetes, deeply wired into IAM, ALB and CloudWatch. If you don't need the k8s ecosystem, this is the cheaper answer.

- **Entry point:** a **task definition** — the container spec (image, CPU/memory, env, log driver, IAM roles). A **service** keeps *N* copies of that task running and registers them with a load balancer. Both live in a **cluster**, which is just a namespace plus capacity.
- **Launch types:** **EC2** (you own and patch the nodes, cheaper at steady high utilisation) vs **Fargate** (no nodes at all, billed per vCPU-second and GB-second). **Capacity providers** let one cluster mix Fargate, Fargate Spot and an ASG with weights.
- **Know cold — the two roles:** the **task role** is what *your application code* can call; the **task execution role** is what the *ECS agent* uses to pull the ECR image and ship logs. Confusing them is the single most common ECS IAM bug, and a favourite interview question.
- **Trap:** `awsvpc` network mode gives every task its own ENI with a real VPC IP — elegant, but you hit per-instance ENI limits and subnet IP exhaustion long before you hit CPU limits.

#### Fargate — the serverless data plane

Not a service you cluster, a **capacity type**. You hand AWS a task definition; it runs the containers on its own fleet of Firecracker micro-VMs. No AMI, no ASG, no patching, no node to SSH into — and no node to over-provision either.

- **Entry point:** selecting `FARGATE` as the launch type (or, better, a **capacity provider**) on an ECS service. The sizing dial is the **task-level CPU/memory pair**, and it comes from a fixed matrix — 0.25 vCPU allows 0.5–2 GB, 1 vCPU allows 2–8 GB, and so on up to 16 vCPU / 120 GB. You cannot ask for arbitrary values, which is the first thing that surprises people migrating from EC2.
- **Know cold:** billing is per vCPU-second and GB-second, from **image pull start** to task stop, with a one-minute minimum. `awsvpc` is the *only* network mode, so every task gets its own ENI and VPC IP. Ephemeral storage is 20 GB by default, configurable to 200 GB; anything that must outlive the task goes to **EFS**. **ARM64/Graviton** and Windows containers are both supported, and **Fargate Spot** costs roughly 70% less in exchange for a two-minute SIGTERM.
- **What you give up:** privileged containers, host access, GPUs, daemonsets, and any sidecar pattern that assumes a shared node. Debugging is **ECS Exec** (SSM under the hood), never SSH.
- **In EKS:** the same engine appears as a **Fargate profile** that matches pods by namespace and labels. Same trade: one pod per micro-VM, no daemonsets — which means your log and metrics agents have to become sidecars.
- **Trap:** the cost crossover. Per vCPU-hour Fargate is meaningfully more expensive than EC2, so a steadily-loaded, well-packed fleet is cheaper on EC2 — Fargate wins on **bursty, spiky, or low-headcount** workloads where the ops time is the real cost. The second trap is scale-out latency: there is no local image cache between tasks, so a 2 GB image is pulled fresh every single time it scales.

### EKS — managed Kubernetes

AWS runs the control plane (etcd, API server) across AZs; everything else is standard upstream Kubernetes.

- **Entry point:** the **cluster** (control plane, billed hourly) plus a *data plane decision*: **managed node groups** (ASGs AWS keeps in sync), **Karpenter** (provisions right-sized nodes directly from pending pods — AWS-originated, now CNCF, and the modern default), or **Fargate profiles** (per-pod, no nodes).
- **Two auth planes meet here:** IAM says who can call the EKS API; Kubernetes RBAC says what they can do inside the cluster. The mapping is now the **access entries** API (it replaced hand-editing the `aws-auth` ConfigMap — knowing that dates you correctly).
- **Pods calling AWS APIs:** **IRSA** (cluster OIDC provider + a role whose trust policy matches a service account) or the newer **EKS Pod Identity** (an agent, no per-cluster OIDC setup, simpler trust policies). Both beat giving the whole node role broad permissions.
- **Trap:** the **VPC CNI** gives every pod a routable VPC IP, so a busy cluster exhausts subnet CIDRs. Fixes: **prefix delegation**, secondary CIDR ranges, or larger instances with more ENI slots. Plan IP space *before* the cluster exists.

### Lambda — functions, no servers

You upload a handler; AWS runs it in a micro-VM (Firecracker) only when something invokes it.

- **Entry point:** a **handler** plus an **event source** — API Gateway or an ALB target group, an S3 notification, an SQS queue, EventBridge, a Kinesis shard, or a bare Function URL. The event source shapes everything: the event JSON, the retry semantics, and whether failures go to a DLQ.
- **Execution model:** one execution environment handles exactly **one invocation at a time**; scaling means more environments. That's why globals persist between invocations (useful for connection reuse, dangerous for state).
- **Concurrency:** **reserved** concurrency both *caps* a function and *guarantees* it capacity; **provisioned** concurrency keeps environments pre-initialised to eliminate cold starts — and bills while idle. **SnapStart** (Java, .NET, Python) restores a pre-warmed snapshot instead.
- **Limits worth memorising:** 15-minute maximum runtime, 10 GB memory (CPU scales *with* memory — that's the only performance dial), 10 GB `/tmp`, 6 MB synchronous payload.
- **Trap:** databases. Thousands of concurrent environments each opening a connection will exhaust RDS — that's what **RDS Proxy** exists for.

### App Runner / Elastic Beanstalk / Lightsail — the "just run my app" tier

- **App Runner:** point it at a container image or a source repo, get an HTTPS URL with autoscaling and scale-to-near-zero. No VPC, ALB or cluster to design.
- **Elastic Beanstalk:** the older version of the same idea — it generates a CloudFormation stack of EC2 + ASG + ELB behind the scenes, and you can drop to those resources when you outgrow it.
- **Lightsail:** fixed-price VPS with predictable billing, aimed at small sites.
- **Why they're on the list:** naming these is how you show judgement. Not every workload deserves EKS, and "App Runner would have done this in a day" is a strong senior answer.

## Networking

### VPC, subnets & routing — the foundation everything else sits in

A software-defined network you own, defined by a CIDR block.

- **Entry point:** the **CIDR block**, then **subnets** (each pinned to one AZ), then **route tables**. There is no "public subnet" checkbox — a subnet is public *because* its route table sends `0.0.0.0/0` to an **Internet Gateway**. That one sentence answers a surprising number of interview questions.
- **Private egress:** a **NAT Gateway** (one per AZ for resilience) lets private subnets reach the internet outbound only. For IPv6 the equivalent is the **egress-only IGW**.
- **Trap:** NAT Gateway is billed hourly *and* per GB processed, and is reliably in the top three surprise line items on a bill. Traffic to S3, ECR and DynamoDB should go through VPC endpoints instead — see below.

### Security Groups vs NACLs — the classic comparison

| | Security Group | Network ACL |
|---|---|---|
| Attaches to | An ENI (instance, task, endpoint) | A subnet |
| State | **Stateful** — return traffic is automatic | **Stateless** — you must allow the return path explicitly |
| Rules | Allow only | Allow **and** deny, evaluated in number order |
| Default | Deny all inbound, allow all outbound | Allow all both ways |

- **Entry point:** the idiomatic AWS pattern is **a security group referencing another security group** — `sg-database` allows port 5432 *from `sg-app`*, not from an IP range. It keeps working as instances scale in and out, and it's the answer that signals you've actually run this.
- **Use NACLs for:** coarse subnet-wide denials (block a CIDR outright). Reaching for NACLs to do ordinary application access control is a smell.

### Elastic Load Balancing — ALB, NLB, GWLB

- **Entry point:** a **listener** (port + protocol) → **rules** → a **target group** (a set of instances, IPs, or Lambda functions with a health check). The target group, not the load balancer, is where health checking and draining actually happen.

| | Layer | Use it for |
|---|---|---|
| **ALB** | 7 (HTTP) | Path/host routing, weighted target groups for canaries, OIDC auth at the edge, WebSockets |
| **NLB** | 4 (TCP/UDP) | Extreme throughput, static IPs per AZ, non-HTTP protocols, preserving source IP |
| **GWLB** | 3 (GENEVE) | Transparently inserting third-party firewall/inspection appliances into the path |

### CloudFront — the global edge

A CDN that is also the front door for TLS, WAF and DDoS protection.

- **Entry point:** a **distribution** with one or more **origins** (an S3 bucket via **OAC**, an ALB, or any HTTP server) and cache behaviours that map path patterns to origins.
- **Edge compute:** **CloudFront Functions** (sub-millisecond, JavaScript, viewer request/response only — header rewrites, redirects) vs **Lambda@Edge** (full runtime, origin-side, heavier).
- **Trap:** an ACM certificate used by CloudFront **must live in `us-east-1`**, regardless of where everything else is. This bites everyone exactly once.

### Route 53 — DNS and health checking

- **Entry point:** a **hosted zone** — **public** (authoritative on the internet) or **private** (resolvable only from the VPCs you associate it with).
- **Routing policies:** simple, **weighted** (canary/blue-green traffic splits), **latency**, **failover** (paired with health checks), geolocation/geoproximity, multivalue.
- **Know cold:** **alias records** point at AWS resources, are free to query, and work at the **zone apex** — which is why you can't just CNAME `example.com` to an ALB. DNS forbids CNAME at the apex; alias is AWS's answer.

### Transit Gateway, VPC Peering & Cloud WAN — connecting VPCs

- **VPC Peering:** a 1:1 link between two VPCs. Cheap, no bandwidth bottleneck, and **non-transitive** — A↔B and B↔C does *not* give you A↔C. Fine for a handful of VPCs; a full mesh of *n* VPCs needs *n(n−1)/2* peerings, which is why it doesn't scale.
- **Transit Gateway:** a regional hub. Every VPC, VPN and Direct Connect gets an **attachment**, and **TGW route tables** decide which attachments can reach which — that's how you build hub-and-spoke with centralised inspection. Billed per attachment-hour plus per GB.
- **Cloud WAN:** a policy-driven global layer that manages TGWs and inter-region peering for you, for genuinely multi-region estates.
- **Trap, for all three:** overlapping CIDRs. Nothing routes between two VPCs that both use `10.0.0.0/16`. Plan address space centrally (**VPC IPAM**) before it's a migration.

### Direct Connect & Site-to-Site VPN — reaching on-prem

- **Site-to-Site VPN:** IPsec tunnels over the public internet. Live in minutes, but bandwidth and jitter follow the internet.
- **Direct Connect:** a dedicated private circuit into an AWS facility. Consistent latency and lower per-GB cost, with a **lead time measured in weeks** — mention that; it's the operational reality.
- **The standard answer:** DX for the primary path, VPN as the automatic backup.

### PrivateLink & VPC endpoints — reaching AWS services privately

- **Gateway endpoints:** **S3 and DynamoDB only**. They're a *route table entry*, and they are **free**. There is no good reason not to have them.
- **Interface endpoints:** an **ENI with a private IP in your subnet** for a specific service (ECR, SSM, Secrets Manager, KMS, …). Billed hourly per AZ plus per GB — but they keep traffic off the NAT Gateway, and the maths usually favours them.
- **PrivateLink** (endpoint services): publish *your own* service behind an NLB so other VPCs and accounts consume it through their own endpoint — no peering, no route sharing, and overlapping CIDRs stop mattering. This is the SaaS-on-AWS connectivity pattern.

## Storage & Data

### S3 — object storage

Not a filesystem. A flat key-value store of immutable objects with a global bucket namespace.

- **Entry point:** a **bucket** + a **key**. Prefixes look like directories but aren't — though they *do* partition request throughput (~3,500 writes / 5,500 reads per second per prefix).
- **Storage classes:** Standard → Standard-IA / One Zone-IA (cheaper storage, per-GB retrieval fee, minimum durations) → Glacier Instant / Flexible / Deep Archive. **Intelligent-Tiering** moves objects automatically for a small monitoring fee and is the low-risk default when access patterns are unknown.
- **Durability & control:** **versioning** (+ MFA delete) protects against overwrite and deletion; **Object Lock** gives WORM retention for audit logs; **lifecycle policies** handle transition and expiry — including expiring old *versions*, which people forget until the bill arrives.
- **Access:** **Block Public Access** is on by default at the account level and overrides everything beneath it. Prefer **bucket policies** and IAM; ACLs are disabled by default now (`Bucket owner enforced`) and should stay that way.
- **Know cold:** reads have been **strongly consistent** since 2020 — the old "eventual consistency" answer is out of date.

### EBS — block storage for one instance

Network-attached virtual disks that behave like local ones.

- **Entry point:** a **volume** in a specific AZ, attached to one instance (io2 supports multi-attach). AZ-bound: to move it, snapshot it.
- **gp3 vs gp2 — the cost win to name:** gp2's IOPS were tied to volume size, so people over-provisioned capacity to buy performance. **gp3 decouples them**: 3,000 IOPS and 125 MB/s baseline at any size, tunable independently, ~20% cheaper per GB. Migrating gp2 → gp3 is a no-downtime modification.
- **io2 / io2 Block Express** for databases needing sustained high IOPS and higher durability.
- **Snapshots** are incremental, stored in S3, and *regional* — the standard cross-AZ and cross-region recovery mechanism.

### EFS & FSx — shared filesystems

- **EFS:** managed NFS. Multi-AZ, grows and shrinks automatically, mountable by many instances/containers at once. Use it when things genuinely need shared POSIX read-write. Lifecycle policies move cold files to IA.
- **FSx:** managed *third-party* filesystems — **Windows File Server** (SMB, AD-integrated), **Lustre** (HPC, links directly to S3), **NetApp ONTAP**, **OpenZFS**.
- **Judgement point:** shared filesystems are often a lift-and-shift crutch. Cloud-native usually means S3 plus a database.

### RDS & Aurora — managed relational databases

- **Entry point:** RDS gives you a **DB instance** running stock Postgres/MySQL/SQL Server/Oracle/MariaDB. Aurora gives you a **DB cluster** — AWS's own storage engine that replicates six ways across three AZs, with compute nodes sharing it.
- **Know this cold — HA vs scale:** **Multi-AZ** is *availability*. It maintains a standby that serves **no traffic** and fails over automatically (the Multi-AZ *cluster* variant is the exception — two readable standbys). **Read replicas** are *scale*: asynchronous, laggy, promoted manually. Interviewers ask this to see if you conflate resilience with performance.
- **Aurora specifics:** storage auto-grows to 128 TiB, up to 15 replicas share the same storage (so failover is seconds, not minutes), **Serverless v2** scales capacity in ACUs without swapping instances, Global Database for cross-region replication.
- **RDS Proxy:** pools and multiplexes connections — the standard fix when Lambda concurrency overwhelms Postgres.

### DynamoDB — managed key-value at any scale

Single-digit millisecond reads regardless of table size, if and only if you model it correctly.

- **Entry point:** a **table** and its **partition key** (optionally plus a **sort key**). The order of work is inverted from SQL: you list your access patterns *first*, then design a key that serves them. There is no "add a JOIN later".
- **Indexes:** a **GSI** has a different partition key, its own capacity, and is eventually consistent — you can add one any time. An **LSI** shares the partition key, must be created *with the table*, and caps that item collection at 10 GB.
- **Capacity:** **on-demand** (pay per request, absorbs spikes, no planning) vs **provisioned** + autoscaling (cheaper at steady predictable load).
- **Extras:** **DAX** for microsecond cached reads; **Streams** → Lambda for change-data-capture; TTL for automatic expiry; global tables for multi-region active-active.
- **Trap:** a **hot partition** — a key like `status#PENDING` concentrates all traffic on one partition and throttles while the table sits mostly idle.

### ElastiCache & OpenSearch — the supporting data stores

- **ElastiCache:** managed **Redis/Valkey** (or Memcached). Entry point is a **cluster endpoint**; *cluster mode disabled* is one shard with replicas, *enabled* is sharded across many. **Valkey** is the cheaper post-fork default. Used for cache-aside, sessions, rate limits and distributed locks.
- **OpenSearch:** managed search and log analytics (the Elasticsearch fork). Entry point is a **domain** (a cluster you size) or a **serverless collection**. Reach for it when CloudWatch Logs Insights runs out of road — full-text search, dashboards, long retention.

## Messaging & Events

These four are constantly confused, and picking correctly between them is a genuine signal of experience.

### SQS — the buffer

- **Entry point:** a **queue URL**, a **visibility timeout** (must exceed your handler's runtime, or the message is redelivered mid-processing), and a **dead-letter queue** with `maxReceiveCount`. Consumers **pull**; use long polling.
- **Standard** — at-least-once, best-effort ordering, effectively unlimited throughput. **FIFO** — exactly-once processing with deduplication, strict ordering *per message group ID*, and much lower throughput limits.
- **Use it to:** decouple producers from consumers and absorb bursts. Messages disappear once acknowledged.

### SNS — the fan-out

- **Entry point:** a **topic**, then subscriptions (SQS, Lambda, HTTPS, email, SMS, mobile push). **Push**-based, millisecond delivery.
- **The idiom to name:** **SNS → multiple SQS queues.** Each consumer gets its own buffer, own retry policy, and own failure isolation. Subscribing Lambdas straight to SNS gives you none of that.

### EventBridge — the router

- **Entry point:** an **event bus**. The **default bus** already carries events from AWS services themselves — which makes it *the* way to react to infrastructure changes ("an instance entered `stopping`", "a Config rule went non-compliant"). **Rules** match on event *content*, not just topic.
- Also carries **Scheduler** (cron/rate at scale, the modern replacement for CloudWatch Events rules) and **Pipes** (point-to-point source → filter → enrich → target).
- **vs SNS:** richer routing, schema registry, cross-account buses, archive and replay — at somewhat higher latency. Choose EventBridge for *routing logic*, SNS for *raw fan-out speed*.

### Kinesis Data Streams & MSK — the log

- **Kinesis:** an ordered, **replayable** stream of records split into **shards**. Consumers track their own position and can rewind (retention up to 365 days); multiple independent consumers read the same data. That replay ability is the core difference from SQS, where an acknowledged message is gone. **Firehose** is the no-code delivery variant → S3/OpenSearch/Redshift.
- **MSK:** managed Apache Kafka, for when you need the Kafka *protocol* and ecosystem (Connect, Streams, existing tooling) rather than just a stream. **MSK Serverless** removes broker sizing.

## Identity

### IAM — the policy engine underneath everything

- **Entry point:** the **policy evaluation logic**, and you should be able to recite it: **explicit `Deny` > explicit `Allow` > implicit deny**. For cross-account access, *both* the identity policy and the resource policy must allow the call.
- **Policy types:** identity-based (attached to a role/user/group), resource-based (on the bucket, queue, key), **permission boundaries** (the ceiling on what a role *can* be granted), **SCPs** (org-level filters that **never grant**, only restrict — so an SCP allowing everything grants nothing).
- **A role has two policies:** the **trust policy** (*who may assume me*) and the **permissions policy** (*what I can do once assumed*). Almost every "access denied and I can't see why" turns out to be the trust policy.

### IAM Roles in practice — the compute-to-AWS bridge

The AWS answer to managed identity: no credentials anywhere, ever.

- **Entry point per compute type:** **instance profile** for EC2, **task role** for ECS, **IRSA / Pod Identity** for EKS pods, **execution role** for Lambda. The SDK finds temporary credentials automatically via the credential provider chain.
- **Know cold:** on EC2 those credentials come from the **instance metadata service** — enforce **IMDSv2** (session-token required), because IMDSv1's simple GET is what turns an SSRF bug into stolen cloud credentials.

### IAM Identity Center — how humans log in

Formerly AWS SSO. The modern replacement for IAM users, and you should say so plainly.

- **Entry point:** connect an **identity source** (built-in directory, or Entra ID/Okta via SAML + SCIM provisioning), define **permission sets** (reusable policy bundles), then **assign** `group × account × permission set`.
- **Result:** `aws sso login` yields short-lived credentials, one portal across every account, and access that disappears when HR deprovisions the user.
- **Say this out loud:** long-lived IAM users with access keys are a finding, not an architecture.

### OIDC federation for CI/CD — keyless pipelines

- **Entry point:** register the provider once (`token.actions.githubusercontent.com` for GitHub Actions), then create a role whose **trust policy conditions on the token's `sub` claim** — scoped to a specific repo *and* branch or environment. The pipeline exchanges its short-lived OIDC token for AWS credentials.
- **Why it matters:** it deletes the entire category of leaked long-lived CI keys. This is the single highest-signal thing you can mention in a CI/CD discussion.

### STS — the token service

- **Entry point:** `AssumeRole` — every pattern above terminates here. Also `AssumeRoleWithWebIdentity` (OIDC/IRSA) and `AssumeRoleWithSAML`.
- **Cross-account:** the role lives in the *target* account and trusts the *source* account; the source identity needs `sts:AssumeRole` permission. Both halves are required.
- **External ID:** when a third party (a monitoring SaaS) assumes a role in your account, require an external ID. It defends against the **confused deputy** problem, and naming that term scores.

### KMS — key management and envelope encryption

- **Entry point:** a **customer-managed key (CMK)** and its **key policy**. Unlike most services, the *key policy is the root of trust* — IAM permissions alone are not enough unless the key policy delegates to IAM. This is the #1 KMS gotcha.
- **Envelope encryption:** services call `GenerateDataKey`, encrypt the payload locally with the plaintext data key, store the *encrypted* data key alongside the ciphertext, and discard the plaintext. That's how S3/EBS/RDS encrypt terabytes with a key that never leaves KMS.
- **Also know:** **grants** for temporary programmatic delegation, automatic annual rotation, **multi-Region keys** for cross-region replicas, and a mandatory **7–30 day waiting period** on key deletion (there is no immediate delete — by design).

## Monitoring & Management

### CloudWatch — metrics, logs and alarms

- **Entry point:** a **metric**, identified by namespace + name + **dimensions**. Dimensions are part of the identity, so a typo creates a *new* metric rather than an error — a common source of "my alarm never fires".
- **Alarms:** threshold or **metric math**, with `M out of N` datapoints to suppress flapping; **composite alarms** combine several to cut noise. Missing-data handling is an explicit setting and usually wrong by default.
- **Logs:** log group → log stream. **Retention defaults to "never expire"** — set it on day one; forgotten log groups are a reliably large bill line. Query with **Logs Insights**.
- **EMF (Embedded Metric Format):** write a specially structured JSON log line and CloudWatch extracts custom metrics from it — no separate `PutMetricData` call, no added latency in your request path. Nice thing to know.

### X-Ray & ADOT — distributed tracing

- **Entry point:** a **trace** made of **segments** and subsegments, stitched into a **service map** that shows latency and errors per hop. **Sampling rules** control cost.
- **ADOT** is AWS's supported **OpenTelemetry** distribution. The current-day answer is: instrument with OTel, export to X-Ray *or* to your third-party backend — don't lock instrumentation to one vendor.

### CloudTrail — the audit log

The "who did this, from where, and when" service.

- **Entry point:** **management events** — control-plane API calls, recorded by default and viewable free in the console for 90 days. **Data events** (S3 object-level GETs, Lambda invocations) are high volume, **off by default**, and billed — turning them on selectively is a real decision.
- **The org pattern:** an **organization trail** writing to a locked-down **log archive account** with S3 Object Lock, so nobody — including an account admin — can erase their own tracks.
- **Boundary to state:** CloudTrail records *API calls*. For "what did this resource look like on Tuesday", that's Config.

### AWS Config — configuration history and compliance

- **Entry point:** enable the **configuration recorder** per account and region; it snapshots every supported resource on change, giving you a timeline you can diff.
- **Rules:** managed or custom (Lambda / Guard) checks — "is every EBS volume encrypted?" — bundled into **conformance packs**, with **remediation actions** wired to SSM Automation documents to fix violations automatically.
- **Aggregators** roll all accounts and regions into one compliance view.

### Systems Manager — fleet management

An umbrella over a dozen capabilities; the ones that matter here:

- **Entry point:** the **SSM Agent** (pre-installed on modern AMIs) plus an instance profile granting `AmazonSSMManagedInstanceCore`. That's the whole onboarding.
- **Session Manager:** browser or CLI shell **without SSH, without port 22, without a bastion host, without a key pair** — and every session logged to CloudTrail and optionally recorded to S3. This is a strong, concrete security-improvement story.
- **Patch Manager** (patch baselines + maintenance windows), **Run Command** (ad-hoc at fleet scale), **State Manager** (associations = *continuous* enforcement, not one-shot), **Automation** runbooks, **Parameter Store** (config and SecureStrings), **Inventory**.

### Trusted Advisor, Health Dashboard & Compute Optimizer — the advisory layer

- **Trusted Advisor:** automated checks across cost, security, fault tolerance, performance and **service limits**. The full check set requires Business or Enterprise support.
- **AWS Health Dashboard:** events affecting *your* account specifically — scheduled maintenance, degraded resources, EOL notices. Wire it to EventBridge instead of reading it manually.
- **Compute Optimizer:** ML-driven right-sizing recommendations for EC2, ASGs, EBS, Lambda memory and Fargate tasks, based on your actual CloudWatch history. Where a cost-reduction conversation should start (§5 of the prep guide).
