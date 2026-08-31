---
type: Guide
title: AWS Services Overview
description: The AWS service catalog explained from the ground up — foundations, compute, networking, storage and data, messaging, identity, monitoring.
tags: [aws, cloud, services, devops]
---

# AWS Services Overview

AWS offers more than two hundred services. Most systems use about thirty of them, and this document explains those thirty: what each one is, what problem it solves, the first thing you create when you use it, and the mistake people most often make with it. It is written so that a reader who has never opened the AWS console can follow it, and it stays useful as a reference afterwards.

The services are grouped the way a system is built. First the **foundations** every service depends on, then the six things almost every system needs: somewhere to run code (**compute**), a network to reach it (**networking**), somewhere to keep data (**storage and data**), a way for the parts to talk to each other (**messaging and events**), a way to decide who may do what (**identity**), and a way to see what is happening (**monitoring**).

```mermaid
flowchart LR
  Users --> Networking --> Compute
  Compute --> Storage[Storage and Data]
  Compute -->|send and receive| Messaging[Messaging and Events]
  Identity -. permits or denies every call .-> Compute
  Identity -. permits or denies every call .-> Storage
  Monitoring -. records what happens .-> Compute
  Monitoring -. records what happens .-> Storage
```

## How to Read This Document

Each service entry has the same shape:

- A short description in plain words: what the service is and what you would use it for.
- **Entry point** — the first object you create. Every AWS service is built around one central object, and once you know which one it is, the rest of the service's settings make sense. For a queue service it is the queue; for a virtual machine service it is the machine image plus the hardware size.
- **Use it when** — the situation where this service is the right choice, so that you can compare it with its neighbours.
- **Trap** — the mistake people most often make with the service, and why it happens. Traps are worth reading even when you skip the rest, because they are what an experienced engineer would tell you before you started.

Technical terms are explained where they first appear. Five words appear so often that it helps to know them before starting. Each has a one-line definition in [AWS Core Concepts](03-aws-core-concepts.md), which is the vocabulary companion to this document.

- **Region** — a geographic area (Frankfurt, Ireland, Virginia) where AWS runs data centres. Almost everything you create lives in exactly one Region.
- **Availability Zone (AZ)** — one or more data centres inside a Region, with their own power and network. A Region has several AZs, and spreading a system across them is how it survives a data-centre failure.
- **VPC** — Virtual Private Cloud, your own private network inside a Region. Most compute and database services are placed inside one.
- **IAM role** — a named set of permissions that a program or a person can take on for a limited time. It is how code running on AWS gets permission to call other AWS services without a stored password.
- **ARN** — Amazon Resource Name, the unique identifier of anything you create, such as `arn:aws:s3:::my-bucket`. Permissions are written against ARNs.

## Foundations

Everything in AWS rests on two ideas that are explained once here and assumed afterwards: where things live, and how you talk to them.

### Accounts, Regions and Availability Zones — Where Everything Lives

An **account** is the container you sign up for. It is the boundary for billing (one bill per account), for limits (quotas are counted per account), and for isolation (nothing in one account can touch another account unless both sides explicitly allow it). Companies run many accounts — one per team, or one per environment — and manage them together with **AWS Organizations**. The [Accounts and Regions](03-aws-core-concepts.md#accounts-and-regions) section of the core concepts defines each of these terms in one line.

- **Regions** are separate geographic locations, each a group of data centres with its own copy of every regional service. When you create a resource you choose a Region, and it stays there: an S3 bucket in Frankfurt (`eu-central-1`) is not visible from the Ireland (`eu-west-1`) console, and data does not move between Regions unless you copy it. Choose the Region closest to your users, or the one your data-residency rules require.
- **Availability Zones (AZs)** are the fault-isolated data centres inside a Region, usually three, connected by fast private links. A well-built system puts a copy of each part in at least two AZs, so that one data centre failing does not stop it. Much of this document is about which services do that for you (S3, DynamoDB, Lambda) and which need you to do it yourself (EC2, subnets, RDS Multi-AZ).
- **Global services:** a few services are not regional. IAM (identity), Route 53 (DNS) and CloudFront (the content network) are the same everywhere in the account.
- **Trap:** AZ names are assigned per account. Your `eu-central-1a` and another account's `eu-central-1a` can be different physical data centres. When two accounts must agree on a physical zone, use the **AZ ID** (`euc1-az1`), which is the same for everyone.

### The Console, the CLI and the API — How You Talk to AWS

Every AWS service is a set of **APIs**: signed HTTPS calls such as `s3:PutObject` or `ec2:RunInstances`. Everything else is a way of making those calls.

```mermaid
flowchart LR
  Console --> API
  CLI --> API
  SDK --> API
  IaC[CloudFormation or CDK or Terraform] --> API
  API --> IAM{IAM allows?}
  IAM -->|yes| Resource[Resource in one Account and Region]
  IAM -->|no| Denied
  API -. every call recorded by .-> CloudTrail
```

- The **console** (the website) is the same API behind buttons. It is the right place to learn and to look, and the wrong place to build production, because what you click is not recorded anywhere you can repeat.
- The **CLI** (`aws s3 ls`) and the **SDKs** (libraries for Python, TypeScript, Java and other languages) make the same calls from a terminal or from code.
- **Infrastructure as code** — CloudFormation, the CDK, Terraform — describes the resources you want in a file, and the tool makes the API calls to create or change them. This is how production infrastructure is built, because the file can be reviewed, versioned and applied again. The [AWS interview prep guide](02-aws-interview-prep.md) compares the tools.
- **Why this matters:** because everything is an API call, every call can be permitted or denied by IAM, and every call is recorded by CloudTrail. Both are covered below, and both work the same way no matter which tool made the call.

## Compute

Compute is where your code runs. AWS gives you four ways to run it, and the difference between them is how much of the machine you see and manage. At one end, EC2 gives you a whole virtual server that you install software on and keep patched. At the other, Lambda runs one function of your code when something calls it, and you never see a machine at all. ECS and EKS sit in between: you package your code as a **container** — an application plus everything it needs to run, built with Docker — and the service decides which machines run it.

The general pattern: the less you manage, the less you can customise, and the more you pay per unit of work at steady high load — but the less you pay when the load is low or uneven, and the less operator time you spend. Most teams end up with a mix.

```mermaid
flowchart LR
  Code[Your code] --> Choice{How is it packaged?}
  Choice -->|installed on a server| EC2[EC2 instances in an Auto Scaling Group]
  Choice -->|container image| ECS[ECS service]
  Choice -->|container image with Kubernetes tooling| EKS[EKS pods]
  Choice -->|a single function| Lambda
  ECS --> Cap{Who owns the machines?}
  EKS --> Cap
  Cap -->|you| Nodes[EC2 nodes]
  Cap -->|AWS| Fargate
```

### EC2 — Rented Virtual Machines

EC2 (Elastic Compute Cloud) rents you virtual machines — AWS calls each one an **instance** — running Linux or Windows, billed per second while running. A **hypervisor** (the software that splits one physical server into many virtual ones) sits underneath, but you never see it. You see a server with an operating system, and you are responsible for everything installed on it.

- **Entry point:** an **AMI** (Amazon Machine Image — a saved copy of a disk with an operating system and any software you pre-installed) plus an **instance type** (the hardware shape: how many CPU cores, how much memory), wrapped together in a **launch template**. In production you rarely start one instance by hand. You point an **Auto Scaling Group (ASG)** at the launch template, and it creates instances, replaces the ones that fail, and adds or removes them as the load changes.
- **Use it when:** the software needs a full operating system, a specific kernel, a GPU or long-running state on the machine; or when you are moving an existing server into the cloud with as few changes as possible.
- **Instance families:** the letter at the start of an instance type says what it is good at — `m` general purpose, `c` compute-optimized (more CPU per GB of memory), `r` memory-optimized (more memory per CPU), `t` burstable (cheap, with CPU credits that run out under sustained load), and `g`/`p` GPU. A `g` at the *end* (`m7g`, `c7g`) means **Graviton**, AWS's own Arm processors, which cost less per unit of work than the Intel and AMD equivalents. **Nitro** is the hardware card and minimal hypervisor behind all current-generation instances; it is why disk encryption and near-bare-metal network performance come included.
- **Storage choice:** the root disk is usually **EBS** (a network-attached disk, covered under Storage & Data; it survives stopping and starting the instance). Some instance types also have an **instance store** — NVMe solid-state disks physically inside the host, very fast, and *erased when the instance stops*. Use them for scratch space and caches, never for anything you need to keep.
- **Placement groups:** a hint about where AWS should put your instances relative to each other — `cluster` (packed close together in one AZ for the lowest network latency), `spread` (deliberately on separate hardware, so that one failure takes out one instance), and `partition` (grouped by rack, for distributed databases such as Cassandra and HDFS that manage their own replication).
- **Trap:** stopping an instance releases its public IP address unless you attached an **Elastic IP** (a fixed address you own), and it destroys instance-store data. More broadly, long-lived servers that people log into and change by hand drift apart until nobody knows what is on them. **Immutable infrastructure** — replace servers instead of changing them — exists to prevent that, and is covered in the [AWS interview prep guide](02-aws-interview-prep.md).

### ECS — AWS's Own Container Orchestrator

A container **orchestrator** is the software that takes container images and decides which machines run them, restarts them when they crash, replaces them when you deploy a new version, and connects them to a load balancer. ECS (Elastic Container Service) is the orchestrator AWS built. It is simpler than Kubernetes and deeply wired into the rest of AWS — IAM for permissions, ALB for traffic, CloudWatch for logs. If you do not need the Kubernetes ecosystem, ECS is the cheaper answer in both money and time.

- **Entry point:** a **task definition** — the specification of what to run: the container image, how much CPU and memory, environment variables, where logs go, and which IAM roles to use. A **task** is one running copy of that definition. A **service** keeps *N* copies of the task running and registers them with a load balancer. Tasks and services live in a **cluster**, which is a name plus the machines (or the Fargate capacity) they run on.
- **Use it when:** your application is already a container, or can easily become one, and you want AWS-native tooling rather than Kubernetes.
- **Launch types — who owns the machines?** With the **EC2** launch type, you run a fleet of EC2 instances (patched and sized by you) and ECS places tasks on them; this is cheaper when the fleet is kept busy. With **Fargate**, there are no machines to manage at all — see the next section. **Capacity providers** let one cluster mix Fargate, Fargate Spot and an ASG, with weights saying how much of each to use.
- **The two roles:** a task definition names two IAM roles, and confusing them is the most common ECS permission bug. The **task role** is what *your application code* can call — for example, read from an S3 bucket. The **task execution role** is what the *ECS agent* uses on your behalf before your code starts — pull the image from ECR (the container image registry) and send logs to CloudWatch.
- **Trap:** `awsvpc` network mode gives every task its own **ENI** (Elastic Network Interface — a virtual network card) with a real IP address in your VPC. That is clean and secure, but each EC2 instance can hold only a limited number of ENIs, and each subnet has a limited number of IP addresses, so busy clusters run out of network interfaces and addresses long before they run out of CPU.

#### Fargate — The Serverless Data Plane

Fargate is not a service you set up on its own. It is a **capacity type** for ECS and EKS: instead of providing machines, you hand AWS a task definition and AWS runs the containers on its own fleet, each task inside its own small, fast-starting virtual machine (a **Firecracker** micro-VM). No machine image, no Auto Scaling Group, no patching, no server to log into — and no server sitting half empty, because you pay only for what each task asks for.

- **Entry point:** choosing `FARGATE` as the launch type (or, better, as a **capacity provider**) on an ECS service. The one sizing decision is the **task-level CPU and memory pair**, chosen from a fixed table of allowed combinations rather than any values you like. This is the first thing that surprises people arriving from EC2.
- **Use it when:** the load is uneven or low, the team is small, or nobody wants to own a fleet of servers. Operator time is usually the real cost, and Fargate removes most of it.
- **Billing and networking:** billed per vCPU-second and per GB-second, from the moment the image starts downloading until the task stops, with a one-minute minimum. `awsvpc` is the *only* network mode, so every task gets its own ENI and VPC IP address. Each task has a default amount of temporary disk with a configurable ceiling; anything that must outlive the task goes to **EFS** (a shared file system, under Storage & Data). **Arm64/Graviton** and Windows containers are both supported, and **Fargate Spot** gives a lower price in exchange for a two-minute warning (a `SIGTERM` signal) before AWS takes the capacity back.
- **What you give up:** privileged containers, access to the host machine, GPUs, **daemonsets** (Kubernetes objects that run one helper on every node), and any **sidecar** pattern (a helper container next to the main one) that assumes a shared machine. Debugging is done with **ECS Exec**, which opens a shell inside the container through Systems Manager, never with SSH.
- **In EKS:** the same engine appears as a **Fargate profile** that matches pods by namespace and labels. Same trade: one pod per micro-VM and no daemonsets, so your log and metrics agents have to become sidecars inside each pod.
- **Trap:** the cost crossover. Per vCPU-hour, Fargate costs more than EC2, so a fleet that is kept steadily busy and tightly packed is cheaper on EC2. Fargate wins on bursty, spiky or small workloads. The second trap is start-up time: Fargate keeps no local copy of your image between tasks, so every new task begins with a download. **SOCI (Seekable OCI)** lazy loading starts the container before the whole image has arrived; ECS on EC2 avoids the problem by caching images on the node.

### EKS — Managed Kubernetes

**Kubernetes** is the open-source container orchestrator most of the industry has standardised on. It has two halves: the **control plane** (the API server that receives your instructions and the `etcd` database that stores the desired state) and the **data plane** (the worker machines, called **nodes**, that run your containers, grouped into **pods**). EKS (Elastic Kubernetes Service) runs the control plane for you, spread across AZs and kept up to date. Everything else is standard upstream Kubernetes, so tools and knowledge transfer from anywhere else Kubernetes runs. The [containers guide](../03-system-design/05-containers.md) explains the Kubernetes concepts themselves.

- **Entry point:** the **cluster** (the control plane, billed hourly) plus a decision about the data plane: **managed node groups** (Auto Scaling Groups that AWS keeps in step with the cluster version), **Karpenter** (a provisioner that watches for pods with nowhere to run and launches right-sized nodes for them directly — AWS-originated, now a CNCF project, and the modern default), or **Fargate profiles** (one micro-VM per pod, no nodes).
- **Use it when:** you need the Kubernetes ecosystem — Helm charts, operators, GitOps tooling, a platform team that already knows it — or portability across clouds. If none of that applies, ECS is less work.
- **Two permission systems meet here:** IAM decides who may call the EKS API from outside; Kubernetes **RBAC** (role-based access control) decides what they may do inside the cluster. The mapping between them is now the **access entries** API, which replaced the error-prone practice of editing the `aws-auth` ConfigMap by hand.
- **Pods calling AWS APIs:** a pod that needs to read S3 should not borrow the node's permissions, because then every pod on that node has them. **IRSA** (IAM Roles for Service Accounts) fixes this: the cluster publishes an OIDC identity provider, and an IAM role trusts one specific Kubernetes service account through it. The newer **EKS Pod Identity** does the same job with an agent on the node, no per-cluster OIDC setup, and simpler trust policies.
- **Trap:** the **VPC CNI** (the network plugin) gives every pod a routable VPC IP address, so a busy cluster runs out of subnet addresses. Fixes: **prefix delegation** (hand each node a block of addresses rather than one at a time), secondary CIDR ranges on the VPC, or larger instances with more ENI slots. Plan the address space *before* the cluster exists; changing it later is a migration.

### Lambda — Functions, No Servers

Lambda runs a single function of your code — a **handler** — only when something calls it, and bills you per millisecond of run time. You never see a server. Internally, each invocation runs inside a Firecracker micro-VM that AWS creates, reuses and destroys as demand changes.

- **Entry point:** a **handler** plus an **event source** — the thing that triggers it: an HTTP request through API Gateway or an ALB, a file landing in S3, a message on an SQS queue, an EventBridge event, a record on a Kinesis shard, or a bare **Function URL**. The event source shapes everything: the shape of the event JSON your code receives, what happens on failure (retry or not, and how many times), and whether failures go to a **dead-letter queue** (a holding queue for messages that could not be processed).
- **Use it when:** work arrives as separate events, runs for seconds rather than hours, and is uneven — a thumbnail generator, a webhook receiver, a nightly report, a small connector between two services.
- **Execution model:** one execution environment handles exactly **one invocation at a time**; scaling means AWS starting more environments in parallel. An environment is reused for later invocations while it is still warm, which is why variables declared outside the handler survive between calls — useful for reusing a database connection, dangerous if you treat them as reliable state.
- **Concurrency:** **reserved** concurrency both *caps* a function (it can never run more than N copies) and *guarantees* it that capacity out of the account-wide pool. **Provisioned** concurrency keeps N environments initialised in advance to remove the **cold start** (the delay of creating a fresh environment and loading your code), and bills while they sit idle. **SnapStart** (Java, .NET and Python) takes a snapshot of an initialised environment and restores it instead.
- **Limits that shape design:** a maximum run time per invocation, a memory ceiling that also sets the CPU share (memory is the only performance dial), a bounded `/tmp` scratch directory, and a cap on the size of a synchronous request and response. The exact numbers change; read the current service quotas before designing against any of them.
- **Trap:** databases. Thousands of environments each opening their own database connection will exhaust a relational database's connection limit. **RDS Proxy** (under Storage & Data) exists to pool those connections.

### App Runner / Elastic Beanstalk / Lightsail — The "Just Run My App" Tier

These three trade control for set-up time. You give them an application and they build the surrounding infrastructure for you.

- **App Runner:** point it at a container image or a source repository and get back an HTTPS address with automatic scaling, including down to almost zero when idle. There is no VPC, load balancer or cluster for you to design.
- **Elastic Beanstalk:** the older version of the same idea — it generates a CloudFormation stack of EC2 instances, an Auto Scaling Group and a load balancer behind the scenes, and you can drop down to those resources when you outgrow it.
- **Lightsail:** a fixed-price virtual private server with predictable monthly billing, aimed at small websites and people who want a simpler console.
- **Use them when:** the workload has no VPC integration, no sidecars and no custom scheduling needs. Such a workload rarely justifies EKS, and often not even ECS.

### Choosing Between the Compute Options

| Option | You manage | AWS manages | Fits when |
| --- | --- | --- | --- |
| **EC2** | The operating system, patching, scaling rules, everything installed | The hardware and the hypervisor | You need a full machine, or are moving an existing server |
| **ECS on Fargate** | The container image and its size | Everything underneath, including the machines | You have containers and want the least operations work |
| **ECS on EC2** | The container image plus the node fleet | The scheduling | Steady high load, where a well-packed fleet is cheaper |
| **EKS** | The Kubernetes objects, the add-ons and often the nodes | The control plane | You need the Kubernetes ecosystem or portability |
| **Lambda** | The function code and its memory setting | Everything else | Event-driven, short, uneven work |
| **App Runner** | The image or the repository | Everything else | A plain web service with no special networking |

## Networking

A network in AWS is something you build, not something you get. Before an instance or container can receive traffic, someone has decided which private network it sits in, which part of that network, whether that part can be reached from the internet, which firewall rules apply, how requests are spread across copies of the application, and how a domain name finds it. This section follows that path from the outside in.

```mermaid
flowchart LR
  User --> R53[Route 53 DNS]
  R53 --> CF[CloudFront edge]
  CF --> ALB[Load balancer in a public subnet]
  ALB --> App[Application in a private subnet]
  App --> DB[Database in a private subnet]
  App --> NAT[NAT Gateway] --> Internet
  App --> VPCE[VPC Endpoint] --> S3
  OnPrem[Your data centre] -->|Direct Connect or VPN| TGW[Transit Gateway]
  TGW --> App
```

### VPC, Subnets & Routing — The Foundation Everything Else Sits In

A **VPC** (Virtual Private Cloud) is a private network you own inside one Region, defined by a **CIDR block** — a range of IP addresses written like `10.0.0.0/16`, where the number after the slash says how big the range is (a `/16` holds 65,536 addresses, a `/24` holds 256). Nothing outside can reach a VPC unless you connect it to something. The [Networking — Inside the VPC](03-aws-core-concepts.md#networking--inside-the-vpc) section of the core concepts defines every part named here.

- **Entry point:** the **CIDR block**, then **subnets** (smaller ranges cut out of it, each pinned to one Availability Zone), then **route tables** (the rules that say where traffic leaving a subnet goes). There is no "public subnet" checkbox. A subnet is public *because* its route table sends `0.0.0.0/0` — meaning "everything not matched by a more specific rule" — to an **Internet Gateway**, the VPC's door to the internet. A subnet whose route table has no such rule is private.
- **Use it when:** always — nearly every service in the Compute and Storage sections sits inside a VPC. The design question is not whether to have one but how to divide it. The usual pattern is a public subnet per AZ for load balancers, and a private subnet per AZ for everything else.
- **Private egress:** servers in a private subnet often still need to reach *out* to the internet — to download packages, or to call a third-party API. A **NAT Gateway** (network address translation) sits in a public subnet and forwards their outbound traffic while blocking anything inbound. Put one in each AZ, so that losing one AZ does not cut off the others. For IPv6 the equivalent is the **egress-only Internet Gateway**.
- **Trap:** NAT Gateway is billed per hour *and* per gigabyte processed, and it is a common source of unexpected cost — often because traffic to AWS's own services is going through it. Traffic to S3, ECR and DynamoDB should go through **VPC endpoints** instead; see PrivateLink & VPC Endpoints below.

### Security Groups vs. NACLs — The Two Firewalls

A VPC has two layers of firewall, and beginners mix them up. A **security group** is attached to the network interface of one instance, task or endpoint. A **network ACL** (access control list) is attached to a whole subnet.

| Aspect | Security Group | Network ACL |
| --- | --- | --- |
| **Attaches to** | An ENI (an instance, a task, an endpoint) | A subnet |
| **State** | **Stateful** — if a request is allowed in, its reply is allowed out automatically | **Stateless** — you must write a rule for the return traffic too |
| **Rules** | Allow only; anything not allowed is denied | Allow **and** deny, checked in number order, first match wins |
| **Default** | Deny all inbound, allow all outbound | Allow all in both directions |

- **Entry point:** the idiomatic AWS pattern is **a security group that references another security group**: `sg-database` allows port 5432 *from anything in `sg-app`*, not from an IP range. Instances come and go and their IP addresses change, but they keep their security group, so the rule keeps working as the application scales.
- **Use NACLs for:** coarse, subnet-wide blocks — for example, denying a known-bad IP range outright. Using NACLs for ordinary application access control is a sign that the design is working against the platform; security groups are the tool for that.
- **Trap:** the stateless part. A network ACL that allows inbound port 443 but forgets to allow the outbound **ephemeral ports** (the high-numbered ports a reply is sent from, 1024–65535) blocks every reply, and connections appear to hang.

### Elastic Load Balancing — ALB, NLB and GWLB

A **load balancer** is the single address that clients connect to. It spreads the incoming connections across many copies of your application and stops sending to copies that fail a health check. AWS has three, distinguished by which layer of the network stack they understand.

- **Entry point:** a **listener** (a port and protocol to accept, such as HTTPS on 443) → **rules** (which requests go where) → a **target group** (a set of instances, IP addresses or Lambda functions, with a health check). The target group, not the load balancer itself, is where health checking and **draining** (letting in-flight requests finish before a target is removed) actually happen.
- **Use it when:** there is more than one copy of anything that receives traffic — which in production is always.

| Load balancer | Layer | Use it for |
| --- | --- | --- |
| **ALB** (Application) | 7 (HTTP) — it reads each request | Routing by path or hostname, splitting traffic by weight between target groups for canary releases, authenticating users at the edge with OIDC, and WebSockets |
| **NLB** (Network) | 4 (TCP/UDP) — it forwards connections without reading them | Very high throughput, a fixed IP address per AZ, protocols other than HTTP, and keeping the client's source IP visible to the application |
| **GWLB** (Gateway) | 3 (IP, over the GENEVE tunnelling protocol) | Inserting third-party firewall or inspection appliances transparently into the traffic path |

- **Trap:** health checks that are too strict or too slow. A health check path that requires the database to be up marks every instance unhealthy during a short database outage and takes the whole service down; a long interval delays removing a broken instance. Check something cheap that proves the process is serving, and tune the interval and thresholds.

### CloudFront — The Global Edge

CloudFront is a **CDN** (content delivery network): it keeps copies of your content at hundreds of **edge locations** around the world, so users get responses from a location near them instead of from your Region. It is also the first thing a user's connection reaches, which makes it the natural place for TLS (the encryption behind `https`), the **WAF** (web application firewall) and protection against **DDoS** attacks (flooding a site with traffic) — all of it handled before anything reaches your servers.

- **Entry point:** a **distribution** with one or more **origins** — the places it fetches from: an S3 bucket (through **OAC**, Origin Access Control, so that the bucket itself stays private), an ALB, or any HTTP server — and **cache behaviours** that map URL path patterns to origins and say how long to keep each response.
- **Use it when:** users are spread out geographically, you serve static files, or you want one place to attach TLS, WAF rules and rate limits.
- **Edge compute:** two ways to run code at the edge. **CloudFront Functions** are tiny JavaScript functions that run in under a millisecond on the viewer's request or response — header rewrites and redirects. **Lambda@Edge** is a full Lambda runtime that can also run on the origin side, heavier and more capable.
- **Trap:** an ACM (AWS Certificate Manager) certificate used by CloudFront **must live in the `us-east-1` Region**, no matter where everything else is, because CloudFront is a global service managed from there.

### Route 53 — DNS and Health Checking

**DNS** turns a name (`api.example.com`) into an address. Route 53 is AWS's DNS service, and it can also decide *which* address to answer with, based on where the user is, what is healthy, or a percentage you set.

- **Entry point:** a **hosted zone** — a container for the DNS records of one domain — either **public** (answers queries from the whole internet) or **private** (answers only inside the VPCs you associate with it, for internal names like `db.internal`).
- **Use it when:** you own a domain and want its records next to the infrastructure they point to, or you need routing decisions that a plain DNS host cannot make.
- **Routing policies:** simple (one answer), **weighted** (split traffic by percentage — canary and blue-green releases), **latency** (send each user to the Region that answers fastest for them), **failover** (a primary and a standby, switched by a health check), geolocation, geoproximity, IP-based and multivalue.
- **Alias records:** a Route 53 record type that points at an AWS resource — a load balancer, a CloudFront distribution, an S3 website. Alias queries are free, and they work at the **zone apex**: the bare domain, `example.com` with nothing in front. Standard DNS forbids a CNAME at the apex, and a load balancer has no fixed IP address to put in an A record, so without alias records a bare domain could not point at an ALB.

### Transit Gateway, VPC Peering & Cloud WAN — Connecting VPCs

Companies end up with many VPCs — one per account, per team, per environment — and eventually two of them need to talk. There are three ways to connect them, from the simplest to the most capable.

- **VPC Peering:** a direct one-to-one link between two VPCs. Cheap, with no bandwidth bottleneck, but **non-transitive**: if A is peered with B and B with C, A still cannot reach C. That is fine for a handful of VPCs, but connecting every VPC to every other needs *n(n−1)/2* peerings — 45 for ten VPCs — which is why it stops scaling.
- **Transit Gateway (TGW):** a regional hub. Every VPC, VPN connection and Direct Connect link becomes an **attachment**, and **TGW route tables** decide which attachments can reach which. This is how you build hub-and-spoke networks with a central inspection point, and it is transitive. Billed per attachment-hour plus per gigabyte.
- **Cloud WAN:** a policy-driven global layer that creates and manages Transit Gateways and the links between Regions for you, for estates that genuinely span many Regions.
- **Use them when:** peering for two or three VPCs that will stay that way; Transit Gateway as soon as there is a hub, a shared-services VPC, or an on-premises connection to share.
- **Trap, for all three:** overlapping address ranges. Nothing can route between two VPCs that both use `10.0.0.0/16`, because a packet to `10.0.1.5` could mean either. Plan address space centrally with **VPC IPAM** (IP address manager) from the start; fixing an overlap later means re-addressing a whole network.

### Direct Connect & Site-to-Site VPN — Reaching On-Prem

Two ways to connect your own data centre or office to a VPC.

- **Site-to-Site VPN:** encrypted IPsec tunnels over the public internet. Live in minutes, but throughput and delay follow whatever the internet is doing that day.
- **Direct Connect (DX):** a dedicated private cable into an AWS facility, arranged through a network provider. Consistent latency and a lower per-gigabyte transfer price, with a **lead time measured in weeks** and a monthly port fee.
- **Use them when:** VPN for small or temporary needs, and as a backup; Direct Connect when a steady, large or latency-sensitive flow justifies the wait and the fee.
- **The standard pattern:** Direct Connect as the primary path, with a VPN as the automatic backup that takes over when the circuit fails.

### PrivateLink & VPC Endpoints — Reaching AWS Services Privately

S3, DynamoDB, ECR and the other AWS services have public internet endpoints. By default, a server in a private subnet reaches them through the NAT Gateway and the public internet, even though both ends are inside AWS. **VPC endpoints** give the service a private entrance inside your VPC instead, so that traffic never leaves the AWS network and never touches the NAT Gateway.

- **Gateway endpoints:** available for **S3 and DynamoDB only**. They are a single line in a route table, and they are **free**. There is no good reason for a VPC not to have both.
- **Interface endpoints:** an **ENI with a private IP address in your subnet** that represents one service — ECR, Systems Manager, Secrets Manager, KMS and many others. Billed per hour per AZ plus per gigabyte, which is still usually cheaper than sending the same traffic through the NAT Gateway.
- **PrivateLink** (endpoint services): the same mechanism in the other direction, so that *you* can publish a service. You put your service behind an NLB and expose it as an endpoint service; other VPCs and other accounts create an interface endpoint to it in their own network. No peering, no shared routes, and overlapping address ranges stop mattering. This is how software vendors deliver a service privately to customers on AWS.
- **Use them when:** whenever private subnets talk to AWS services — gateway endpoints always, interface endpoints wherever the NAT bill or a compliance rule says traffic must stay private — and PrivateLink whenever you offer a service to another account without opening a network path.

## Storage & Data

There is no single "storage" in AWS. Each service is built for one shape of data and one way of reading it, and the price and behaviour differ by orders of magnitude. So the first question is always *what does the data look like, and how will it be read?* — not *which service is best?*

```mermaid
flowchart LR
  Q{What shape is the data?}
  Q -->|files and objects read whole| S3
  Q -->|a disk for one server| EBS
  Q -->|a folder shared by many servers| EFS[EFS or FSx]
  Q -->|tables with joins and transactions| RDS[RDS or Aurora]
  Q -->|key lookups at any scale| DDB[DynamoDB]
  Q -->|hot values read in microseconds| ElastiCache
  Q -->|full-text search over logs or documents| OpenSearch
```

### S3 — Object Storage

S3 (Simple Storage Service) stores **objects** — files of any kind, from a few bytes to terabytes — and returns them whole when asked. It is not a file system: there are no directories, no editing part of a file in place, and no mounting it like a disk. It is a flat store where each object has a **key** (its full name) and lives in a **bucket** whose name is unique across all of AWS. It is also the cheapest and most durable place to put data in AWS, and nearly every other service reads from it or writes to it.

- **Entry point:** a **bucket** plus a **key** such as `invoices/2026/03/inv-001.pdf`. The slashes make keys *look* like folders in the console, but they are only characters in the name. They matter for one thing: request throughput is partitioned by **prefix** (the beginning of the key), so spreading keys across many prefixes raises the ceiling on requests per second.
- **Use it when:** data is written once and read many times as a whole — uploads, backups, logs, static websites, data-lake files, build artifacts.
- **Storage classes:** how fast and how often you need an object decides how much you pay to store it. **Standard** for frequently read data → **Standard-IA** and **One Zone-IA** ("infrequent access": cheaper per GB stored, a fee per GB retrieved, a minimum storage duration) → **Glacier Instant, Flexible and Deep Archive** (progressively cheaper, with retrieval taking minutes to hours for the deeper tiers). **Intelligent-Tiering** watches how each object is used and moves it between classes automatically for a small monthly monitoring fee; it is the low-risk default when you do not know the access pattern.
- **Durability and control:** **versioning** keeps every previous version of an object, so that an overwrite or a delete can be undone (**MFA delete** additionally requires a second authentication factor to remove versions). **Object Lock** makes objects unchangeable for a set period — WORM, "write once, read many" — for audit logs and legal retention. **Lifecycle policies** move objects between classes and delete them on a schedule, including old *versions*, which people forget until they see the bill for storing every version of everything.
- **Access:** **Block Public Access** is switched on by default at the account level and overrides every setting beneath it, so that a bucket cannot be made public by accident. Grant access with **bucket policies** and IAM. Bucket **ACLs**, an older mechanism, are disabled by default now (`Bucket owner enforced`) and should stay that way.
- **Read consistency:** reads have been **strongly consistent** since December 2020 — after a write completes, every read returns the new object. Older guidance describing "eventual consistency" and stale reads is out of date.

### EBS — Block Storage for One Instance

EBS (Elastic Block Store) provides **volumes**: virtual hard disks that you attach to an EC2 instance and format like any disk. They are in fact network storage, replicated within one AZ, which is why they survive the instance being stopped.

- **Entry point:** a **volume** in one specific AZ, attached to one instance (the high-end `io2` type allows attaching to several). Because it is AZ-bound, moving a volume to another AZ means taking a **snapshot** and creating a new volume from it there.
- **Use it when:** an operating system disk, a database's data directory, or any software that expects a local disk.
- **gp3 vs. gp2:** the general-purpose types. In `gp2`, **IOPS** (input/output operations per second — how many reads and writes the disk can do) were tied to volume size, so people bought bigger disks than they needed to get performance. **`gp3` decouples them**: every volume gets a baseline of 3,000 IOPS and 125 MB/s regardless of size, and you can raise either number independently of capacity. Changing a volume from gp2 to gp3 is a live modification with no downtime and a lower price; there is rarely a reason not to.
- **io2 / io2 Block Express:** for databases that need sustained high IOPS and higher durability than gp3 offers.
- **Snapshots** are point-in-time copies stored in S3. They are incremental (only the blocks changed since the last snapshot are stored) and *regional* rather than AZ-bound, which makes them the standard way to move a disk between AZs or Regions and to back it up.

### EFS & FSx — Shared Filesystems

Sometimes many machines need to read and write the *same* files at the same time — an uploads folder shared by a fleet of web servers, home directories, a build cache. A disk (EBS) attaches to one machine, and an object store (S3) is not a file system, so AWS offers managed network file systems for this case.

- **EFS (Elastic File System):** managed **NFS**, the standard Linux network file protocol. It spans multiple AZs, grows and shrinks automatically as you add and remove files, and can be mounted by many instances or containers at once. Use it when things genuinely need shared **POSIX** read-write — the ordinary Linux file semantics of permissions, locks and directories. Lifecycle policies move files that have not been read for a while to a cheaper infrequent-access class.
- **FSx:** managed versions of *third-party* file systems, for when the software expects a specific one — **FSx for Windows File Server** (SMB, the Windows file protocol, joined to Active Directory), **FSx for Lustre** (a high-performance file system for HPC and machine learning, which can present an S3 bucket as a file system), **FSx for NetApp ONTAP** and **FSx for OpenZFS**.
- **Use them when:** existing software insists on a shared file system, or many processes need to work on the same files.
- **Caveat:** shared file systems are often a compromise made when moving an existing system into the cloud without changing it. Applications built for the cloud usually keep files in S3 and state in a database instead, because both scale further and cost less.

### RDS & Aurora — Managed Relational Databases

A **relational database** stores data in tables with a schema, and is queried with SQL. RDS (Relational Database Service) runs one for you: it installs the database engine, takes backups, applies patches and handles failover, while your code keeps using the same Postgres or MySQL it already speaks. Aurora is AWS's own re-engineered version of Postgres and MySQL with a different storage layer underneath.

- **Entry point:** RDS gives you a **DB instance** — one server running stock Postgres, MySQL, SQL Server, Oracle or MariaDB, in a size you choose. Aurora gives you a **DB cluster**: AWS's own storage engine keeps six copies of the data across three AZs, and one or more compute nodes share that storage.
- **Use it when:** the data has relationships, needs transactions, or is queried in ways you cannot predict in advance. This is the default for most application data.
- **Availability vs. scale — two features that look alike:** **Multi-AZ** is about *availability*. It keeps a synchronised standby copy in another AZ that serves **no traffic** at all; if the primary fails, RDS switches to it automatically, typically within a minute or two. (The *Multi-AZ cluster* variant is the exception, with two standbys that can also serve reads.) **Read replicas** are about *scale*. They copy data asynchronously — so they lag slightly behind — and can serve read queries, but promoting one to primary after a failure is a manual step. The two solve different problems, and neither replaces the other.
- **Aurora specifics:** storage grows automatically without you provisioning it; read replicas share the same storage volume rather than copying it, so failover to one takes seconds rather than minutes; **Serverless v2** scales the compute up and down in **ACUs** (Aurora Capacity Units) without swapping instances; and **Global Database** replicates to other Regions for disaster recovery.
- **RDS Proxy:** a connection pool between your application and the database. It keeps a small number of real connections open and shares them among many clients, and it is the standard fix when Lambda concurrency overwhelms Postgres's connection limit.
- **Trap:** treating a read replica as a backup or as a standby. It is neither: a bad write is replicated to it within seconds, and it does not take over automatically. Backups come from automated snapshots and **point-in-time recovery**; failover comes from Multi-AZ.

### DynamoDB — Managed Key-Value at Any Scale

DynamoDB is a **NoSQL** database: it stores items (JSON-like documents) and finds them by key, and it promises the same single-digit-millisecond response whether the table holds a thousand items or a hundred billion. The price of that promise is that you must know your queries in advance — there is no SQL, no joins, and no ad-hoc queries across the whole table.

- **Entry point:** a **table** and its **partition key** (the attribute that decides which storage partition holds the item, and the only attribute you can look up by directly), optionally plus a **sort key** (which orders items within one partition key and lets you fetch a range of them). The order of work is inverted from SQL: you list every way the application will read the data *first*, then design the keys to serve those reads. There is no "add a JOIN later".
- **Use it when:** the access patterns are known and simple — look up by id, list a user's orders newest first — and the scale or the latency requirement is beyond what a relational database handles comfortably. Session stores, shopping carts, user profiles, event logs.
- **Indexes:** a **GSI** (global secondary index) is a copy of the table with a different partition key, so that you can look items up a second way. It has its own capacity, is eventually consistent (it lags a moment behind the table), and can be added or removed at any time. An **LSI** (local secondary index) keeps the same partition key with a different sort key, must be created *with the table*, and caps the items sharing one partition key at 10 GB.
- **Capacity:** **on-demand** (pay per request, absorbs spikes without planning) vs. **provisioned** (you declare reads and writes per second, optionally with autoscaling; cheaper at steady, predictable load).
- **Extras:** **DAX** (an in-memory cache in front of the table, for microsecond reads); **Streams** (a feed of every change to the table, usually consumed by Lambda — the pattern called change data capture); **TTL** (a timestamp attribute after which items expire and are deleted at no cost); and **global tables** for active-active replication across Regions.
- **Trap:** a **hot partition**. Throughput is divided across partitions by key, so a key that many items share — `status#PENDING`, today's date — sends all its traffic to one partition, which throttles while the rest of the table sits idle. Choose partition keys with many distinct values and even traffic across them.

### ElastiCache & OpenSearch — The Supporting Data Stores

Two services that sit next to the main database rather than replacing it.

- **ElastiCache:** a managed in-memory store — **Redis**, its open-source fork **Valkey**, or Memcached — for data that must be read in microseconds and can be rebuilt if lost. The entry point is a **cluster endpoint**; *cluster mode disabled* means one shard with replica copies, *enabled* means data split across many shards. **Valkey** is the cheaper default since the fork; the fork, and the 2024 relicensing that caused it, are explained in [Redis — Core Concepts and Workflow](../03-system-design/03-caching.md#redis--core-concepts-and-workflow). Used for **cache-aside** (check the cache first, then the database, then fill the cache), session storage, rate limiting and distributed locks.
- **OpenSearch:** managed full-text search and log analytics, the open-source fork of Elasticsearch. The entry point is a **domain** (a cluster you size) or a **serverless collection** (sized for you). Use it when CloudWatch Logs Insights is no longer enough — search across text fields, dashboards over logs, and retention measured in years.
- **Use them when:** ElastiCache when the same values are read far more often than they change and the database is the bottleneck; OpenSearch when users search text, or when operators need to slice logs in ways CloudWatch cannot.

## Messaging & Events

When one part of a system calls another directly, the two are tied together: if the receiver is slow or down, the caller waits or fails. Messaging services put a middle layer between them. The sender hands a message to the service and moves on; the receiver picks it up when it is ready. This is called **decoupling**, and it is how systems absorb bursts, survive partial failures and let teams deploy independently.

AWS has four messaging services because there are four different patterns: SQS **buffers** work in a queue for one consumer, SNS **fans out** one message to many subscribers, EventBridge **routes** events by looking at their content, and Kinesis and MSK keep a **replayable log** that many consumers read at their own pace.

```mermaid
flowchart LR
  P[Producer] -->|one message, one consumer| SQS
  SQS --> Worker
  P -->|one message, many subscribers| SNS
  SNS --> QA[Queue A]
  SNS --> QB[Queue B]
  P -->|deliver by content| EB[EventBridge]
  EB -->|rule matches| Target
  P -->|append to a log| Log[Kinesis or MSK]
  Log -->|reads from its own position| C1[Consumer 1]
  Log -->|reads from its own position| C2[Consumer 2]
```

### SQS — The Buffer

SQS (Simple Queue Service) is a **queue**: producers put messages in, and consumers take them out, roughly in the order they arrived. Each message is processed by one consumer and then deleted. If the consumers are slow, the queue simply grows; if they are down, messages wait, for up to 14 days.

- **Entry point:** a **queue URL**, a **visibility timeout** and a **dead-letter queue**. The visibility timeout is the period a message is hidden from other consumers after one has received it; it must be longer than your handler takes to run, or the message reappears and is processed twice. The dead-letter queue, with a `maxReceiveCount`, is where a message goes after failing that many times, so that one bad message cannot block the queue forever. Consumers **pull** messages by polling; use **long polling** (wait up to 20 seconds for a message to arrive) to cut cost and empty responses.
- **Use it when:** work can be done a little later, by a pool of workers, at whatever rate they manage — image processing, sending emails, anything triggered by a user action that the user does not need to wait for.
- **Standard vs. FIFO:** a **Standard** queue delivers each message *at least once*, in roughly but not strictly the order sent, with effectively unlimited throughput; your consumer must tolerate the occasional duplicate. A **FIFO** queue delivers in strict order *within a message group ID* and removes duplicates, giving exactly-once processing **within the 5-minute deduplication interval**. FIFO's base throughput limits are far lower than Standard's; **high-throughput mode** raises them substantially.
- **Trap:** the visibility timeout. Set it shorter than the processing time and every slow message is processed twice; set it far longer and a crashed consumer leaves the message invisible for all that time before another consumer can take it. Match it to the real processing time, and make consumers **idempotent** — safe to run twice — because Standard queues will occasionally deliver twice regardless.

### SNS — The Fan-Out

SNS (Simple Notification Service) delivers one message to every **subscriber** of a **topic** at once. Where SQS holds a message until one consumer takes it, SNS pushes a copy to each subscriber immediately and keeps nothing.

- **Entry point:** a **topic**, then **subscriptions** — SQS queues, Lambda functions, HTTPS endpoints, email addresses, SMS numbers or mobile push. **Push**-based, with millisecond delivery.
- **Use it when:** several independent things need to know about the same event — an order was placed, so billing, the warehouse and analytics each need a copy.
- **The standard pattern:** **SNS → one SQS queue per consumer.** Each consumer then has its own buffer, its own retry policy and its own dead-letter queue, and one slow consumer cannot affect the others. Subscribing Lambda functions straight to SNS gives you none of that: there is no buffer between them, and a burst of messages becomes a burst of invocations.

### EventBridge — The Router

EventBridge receives **events** — small JSON documents saying that something happened — and delivers each one to the targets whose **rules** match its content. Where SNS asks "who subscribed to this topic?", EventBridge asks "which rules match this event's fields?", so a rule can say "orders over 1,000 from the EU" without the producer having to create a topic for that case.

- **Entry point:** an **event bus**. Every account has a **default bus** that already carries events generated by AWS services themselves — "an EC2 instance entered `stopping`", "a Config rule went non-compliant", "a pipeline stage failed" — which makes EventBridge *the* way to react to things happening in your infrastructure. **Rules** match on event *content*, not only a topic name, and send matches to **targets**: Lambda functions, Step Functions, SQS queues, other buses, and many more.
- **Also included:** **Scheduler** (cron and rate schedules at any scale — the modern replacement for CloudWatch Events rules) and **Pipes** (a point-to-point connection from one source, through an optional filter and enrichment step, to one target, without writing glue code).
- **Use it when:** routing decisions depend on what is *in* the event, when you want to react to AWS's own events, when events cross account boundaries, or when you need to archive and replay events later.
- **vs. SNS:** richer routing, a schema registry, cross-account buses, archive and replay — at somewhat higher latency and lower throughput. Choose EventBridge for *routing logic*, SNS for *raw fan-out speed*.

### Kinesis Data Streams & MSK — The Log

A **log** in this sense is an ordered, append-only record of events that is kept for a period, not deleted on read. Consumers read from a position of their choosing and remember where they got to, so several of them can read the same data independently, and any of them can go back and read it again. That replay ability is the core difference from SQS, where an acknowledged message is gone.

- **Kinesis Data Streams:** an ordered, **replayable** stream of records split into **shards** (each shard is a unit of throughput and of ordering). Consumers track their own position and can rewind, retention is configurable up to 365 days, and many independent consumers can read the same stream. **Firehose** is the no-code companion that continuously delivers a stream into S3, OpenSearch or Redshift.
- **MSK (Managed Streaming for Apache Kafka):** managed **Apache Kafka**, the open-source standard for this pattern. Use it when you need the Kafka *protocol* and ecosystem — Kafka Connect connectors, Kafka Streams, existing tooling — rather than only a stream. **MSK Serverless** removes the job of sizing brokers.
- **Use them when:** clickstreams, metrics, sensor data and change feeds — anything with many events per second that several systems need to process, or that you may need to process again after fixing a bug.
- **Trap:** ordering is per shard (Kinesis) or per partition (Kafka), and so is throughput. Records with the same partition key land on the same shard, so — exactly as with DynamoDB — a key with uneven traffic creates a hot shard that throttles while the others sit idle.

## Identity

Every call to AWS — from a person, a pipeline or a running program — is checked by IAM before it does anything. The questions are always the same: *who is asking*, *what are they allowed to do*, and *how did they prove who they are* without a password stored somewhere it can be stolen. The services in this section answer those three questions for people, for CI/CD pipelines and for code running on AWS, and end with KMS, which decides who may decrypt what. The [Identity and Access](03-aws-core-concepts.md#identity-and-access) section of the core concepts defines each term.

```mermaid
flowchart LR
  Human[Person] -->|logs in| IdC[IAM Identity Center]
  Pipeline[CI/CD pipeline] -->|OIDC token| Role[IAM Role]
  Code[EC2 or ECS task or Lambda] -->|attached role| Role
  IdC -->|permission set| Role
  Role --> STS
  STS -->|short-lived credentials| Call[API call]
  Call --> Eval{IAM evaluation}
  Eval -->|an explicit deny| Denied
  Eval -->|an allow and no deny| Allowed
  Eval -->|neither| Denied
  Allowed -. if the data is encrypted .-> KMS
```

### IAM — The Policy Engine Underneath Everything

IAM (Identity and Access Management) is the rules engine that decides, for every single API call, whether it is allowed. Rules are written as **policies**: JSON documents listing an *effect* (Allow or Deny), the *actions* (`s3:GetObject`), the *resources* (which bucket, by ARN) and optional *conditions* (only from this IP range, only with MFA). Policies attach to identities and to resources, and IAM evaluates all of them together.

- **Entry point:** the **policy evaluation logic**, which is the one thing to memorise: by default everything is denied; an **explicit `Allow`** in some applicable policy permits the call; an **explicit `Deny`** anywhere overrides every Allow. For a call across accounts, *both* the caller's identity policy and the target's resource policy must allow it.
- **Use it when:** always — there is no way around IAM. The skill is writing policies that grant exactly what a program needs (**least privilege**) rather than `*` on everything because it was quicker.
- **Policy types:** **identity-based** (attached to a role, user or group: "this identity may do these things"); **resource-based** (attached to the bucket, queue or key: "these identities may touch me" — the way another account is let in); **permission boundaries** (a ceiling on what a role *can* be granted, so that a team allowed to create roles cannot create one more powerful than themselves); and **SCPs** (service control policies, applied by AWS Organizations to whole accounts, which **never grant** anything — they only remove permissions, so an SCP allowing everything grants nothing by itself).
- **A role has two policies:** the **trust policy** says *who may assume me* — which accounts, services or identity providers — and the **permissions policy** says *what I can do once assumed*. Almost every "access denied and I cannot see why" turns out to be a trust policy that does not name the caller.
- **Trap:** IAM users with long-lived **access keys**. They were the original way to give a program credentials, and keys leaked in code repositories remain the most common cause of compromised accounts. Every section below exists to replace them with short-lived credentials that expire on their own.

### IAM Roles in Practice — The Compute-to-AWS Bridge

How does code running on AWS get permission to call AWS? Not with a stored password. Each compute service can be given an **IAM role**, and AWS hands the running code temporary credentials for that role — rotated automatically, expiring within hours, never written to disk. This is AWS's version of what other clouds call a managed identity.

- **Entry point per compute type:** an **instance profile** for EC2 (the wrapper that attaches a role to an instance), the **task role** for ECS, **IRSA or Pod Identity** for EKS pods, and the **execution role** for Lambda. Your code does not need to know any of this: the AWS SDK's **credential provider chain** looks in the standard places in order — environment variables, a config file, then the compute service's own credentials endpoint — and finds the temporary credentials automatically.
- **Use it when:** any code on AWS needs to call AWS. If you find yourself pasting an access key into an environment variable on an EC2 instance, a role is what you should have used.
- **On EC2:** the credentials are served by the **instance metadata service**, a special address (`169.254.169.254`) that only the instance itself can reach. Enforce **IMDSv2**, which requires a session token obtained with a PUT request first. The original IMDSv1 answered a plain GET, which is exactly what an **SSRF** bug (server-side request forgery — tricking your web server into fetching a URL of the attacker's choosing) can produce; IMDSv1 is how such bugs turned into stolen cloud credentials.
- **Trap:** granting the role more than the code needs, to be safe. Every process on that instance or in that task now has those permissions, and so does anyone who compromises it.

### IAM Identity Center — How Humans Log In

Formerly called AWS SSO. This is how *people* should get into AWS: through one login, tied to the company directory, producing temporary credentials — instead of each person having an IAM user and an access key in every account.

- **Entry point:** connect an **identity source** — the built-in directory, or an existing one such as Microsoft Entra ID or Okta, connected through **SAML** (the enterprise single-sign-on standard) for login and **SCIM** (a provisioning standard) so that users and groups are created and removed automatically. Then define **permission sets** (reusable bundles of policies such as "read-only" or "developer") and **assign** each combination of `group × account × permission set`.
- **Use it when:** more than one person needs access to more than one account — which is every company.
- **Result:** `aws sso login` in the terminal opens a browser login and returns short-lived credentials; one web portal lists every account and role the person may use; and when HR removes the person from the directory, their access to every account disappears with them.

### OIDC Federation for CI/CD — Keyless Pipelines

A deployment pipeline (GitHub Actions, GitLab CI) needs to call AWS to deploy. The old way was to create an IAM user, generate an access key and paste it into the CI system's secrets — a long-lived credential that anyone with access to the CI settings could copy. **OIDC federation** replaces it: the CI provider signs a short-lived token that says which repository and branch is running, and AWS exchanges that token for temporary credentials.

- **Entry point:** register the CI provider once as an **identity provider** in IAM (`token.actions.githubusercontent.com` for GitHub Actions). Then create a role whose **trust policy conditions on the token's `sub` claim** — the field that identifies the repository and the branch or environment — so that only `my-org/my-repo` on `main` can assume it. The pipeline calls `AssumeRoleWithWebIdentity` with its token and receives credentials valid for the length of the job.
- **Use it when:** any pipeline deploys to AWS. There is no scenario where a stored access key in CI is the better choice.
- **Why it matters:** it removes the entire category of leaked long-lived CI keys, and the credentials that remain are scoped to one repository and one branch.

### STS — The Token Service

STS (Security Token Service) is the service that actually issues temporary credentials. Every mechanism above — roles on compute, Identity Center logins, OIDC pipelines — ends with a call to STS, which returns an access key, a secret key and a session token that expire together.

- **Entry point:** `AssumeRole` — give it a role ARN and get back credentials for that role. Its siblings are `AssumeRoleWithWebIdentity` (for OIDC tokens, used by CI pipelines and IRSA) and `AssumeRoleWithSAML` (for SAML logins).
- **Use it when:** directly, for cross-account access and for narrowing permissions for one task; indirectly, all the time, because everything else uses it.
- **Cross-account access:** the role lives in the *target* account and its trust policy names the *source* account; the caller in the source account needs `sts:AssumeRole` permission on that role's ARN. Both halves are required, and forgetting either one produces the same "access denied".
- **External ID:** when a third party — a monitoring vendor, a cost tool — needs to assume a role in your account, require an **external ID**: a shared secret the vendor must present with every assume call. It defends against the **confused deputy** problem, where an attacker with an account at the same vendor tricks the vendor's system into using its permission to assume *your* role.

### KMS — Key Management and Envelope Encryption

KMS (Key Management Service) holds encryption keys in hardware that never releases them, and performs encryption operations on request. Nearly every storage service's "encrypt at rest" checkbox is KMS underneath. The point of a managed key service is that a key is never written to a disk you control, and every use of it is logged and permission-checked. The [Encryption and Secrets](03-aws-core-concepts.md#encryption-and-secrets) section of the core concepts defines the terms.

- **Entry point:** a **customer-managed key (CMK)** and its **key policy**. Unlike most services, the *key policy is the root of trust*: an IAM policy granting `kms:Decrypt` does nothing unless the key policy also permits it, or explicitly delegates to IAM. This surprises people whose IAM permissions look complete but who still cannot decrypt.
- **Use it when:** data must be encrypted with a key *you* control, audit and can revoke — rather than an AWS-owned key you cannot see — and whenever a compliance rule says so.
- **Envelope encryption:** KMS keys never leave KMS, and one KMS call can encrypt only a few kilobytes, so nothing encrypts a terabyte disk directly with a KMS key. Instead, a service asks KMS for a **data key** (`GenerateDataKey`) and receives two copies: one in plain text and one encrypted under the KMS key. It encrypts the data locally with the plain-text key, stores the *encrypted* copy of the data key next to the data, and discards the plain-text copy. To read, it sends the encrypted data key back to KMS to be decrypted. That is how S3, EBS and RDS encrypt terabytes with a key that never leaves KMS.
- **Also:** **grants** (temporary programmatic permission to use a key, used by AWS services on your behalf); **automatic key rotation** (configurable from 90 to 2,560 days since 2024, where the period used to be fixed at 365); **multi-Region keys** for encrypting data that is replicated across Regions; and a mandatory **7–30 day waiting period** before a key is deleted — there is no immediate delete, by design, because deleting a key makes everything encrypted under it unreadable forever.
- **Trap:** deleting or disabling a key that something still uses. Snapshots, database backups and S3 objects encrypted with it become unreadable, and the waiting period is your only warning.

## Monitoring & Management

Once a system is running you need to answer three questions about it: *is it healthy right now* (metrics, logs and traces), *who changed what* (an audit log of API calls), and *what did a resource look like on a given day* (a history of configuration). A fourth group of services manages the servers themselves and tells you where money is being wasted. The [Observability and Governance](03-aws-core-concepts.md#observability-and-governance) section of the core concepts defines the terms.

```mermaid
flowchart LR
  App[Application] -->|metrics and logs| CW[CloudWatch]
  CW -->|threshold crossed| Alarm --> Notify[SNS or EventBridge]
  App -->|trace segments| XRay[X-Ray]
  Calls[Every API call] --> CT[CloudTrail]
  State[Every resource change] --> Cfg[AWS Config]
  Cfg -->|rule fails| Remediate[SSM Automation]
  Fleet[EC2 fleet] --> SSM[Systems Manager]
  Advice[Trusted Advisor and Compute Optimizer] -. recommendations .-> Fleet
```

### CloudWatch — Metrics, Logs and Alarms

CloudWatch is where numbers and log lines go. Every AWS service publishes **metrics** (numbers over time — CPU use, request count, queue depth) to it automatically, applications send their **logs** to it, and **alarms** watch a metric and act when it crosses a threshold.

- **Entry point:** a **metric**, identified by a namespace (`AWS/EC2`, or your own), a name (`CPUUtilization`) and **dimensions** (key-value pairs such as `InstanceId=i-123` that say *which* thing the number is about). Dimensions are part of the metric's identity, so a typo in a dimension creates a *new*, separate metric rather than an error — a common reason an alarm never fires.
- **Use it when:** always, for alarms on the platform metrics; and for application logs, unless you already run another log system.
- **Alarms:** watch one metric, or a **metric math** expression combining several, and trigger when `M out of N` recent data points breach the threshold, so that a single spike does not trigger the alarm. **Composite alarms** combine several alarms with AND and OR to cut noise. How an alarm treats *missing* data is an explicit setting, and the default is usually wrong for your case — decide whether "no data" means "healthy" or "the thing that reports data is dead".
- **Logs:** a **log group** (one per application or service) holds **log streams** (one per instance or task). **Retention defaults to "never expire"** — set it on the first day, because forgotten log groups are a reliably large line on the bill. Query with **Logs Insights**, a purpose-built query language over log lines.
- **EMF (Embedded Metric Format):** write a specially structured JSON log line and CloudWatch extracts custom metrics from it automatically — no separate `PutMetricData` call, and no extra latency in the request path. It is the cheapest way to get business metrics out of an application.
- **Trap:** custom metrics cost per metric per month, and each unique combination of dimension values is a separate metric. A dimension such as `UserId` with a million values creates a million metrics and a surprising bill.

### X-Ray & ADOT — Distributed Tracing

When one request passes through a load balancer, two services, a queue and a database, no single log tells you where the time went. **Distributed tracing** gives the request an id at the front and records a timed **segment** at every hop, so that the whole journey can be put back together into one picture.

- **Entry point:** a **trace** made of **segments** and subsegments, one per service or call, stitched into a **service map** that shows latency and error rates per hop. **Sampling rules** control how many requests are traced, which controls cost.
- **Use it when:** more than two services handle one request and "it is slow" cannot be answered from logs alone.
- **ADOT** (AWS Distro for OpenTelemetry) is AWS's supported build of **OpenTelemetry**, the vendor-neutral standard for instrumenting code. Instrument with OpenTelemetry and export to X-Ray, or to any third-party backend, rather than writing X-Ray-specific code that ties you to one vendor.

### CloudTrail — The Audit Log

CloudTrail records every API call made in the account — who made it, from which IP address, when, with which parameters, and what the answer was. Because everything in AWS is an API call, this is the complete answer to "who did this?"

- **Entry point:** **management events** — control-plane API calls such as creating an instance, changing a security group or assuming a role. They are recorded by default and viewable free in the console for 90 days. **Data events** — the high-volume calls inside a service, such as every S3 object read or every Lambda invocation — are **off by default** and billed by volume, so turning them on for specific buckets or functions is a real cost decision.
- **Use it when:** always, and for longer than 90 days: create a **trail** that writes events to an S3 bucket, so that they are kept as long as you need and can be searched with Athena.
- **The organization pattern:** an **organization trail** that covers every account and writes to a locked-down **log archive account**, with S3 Object Lock on the bucket, so that nobody — including an administrator of the account where something happened — can erase the record of what they did.
- **Boundary with Config:** CloudTrail records *API calls* — the actions. For "what did this security group look like last Tuesday" — the state — the answer is AWS Config, next.

### AWS Config — Configuration History and Compliance

AWS Config keeps a history of what every resource looked like and when it changed, and checks that history against rules you define.

- **Entry point:** enable the **configuration recorder** in each account and Region. It takes a snapshot of every supported resource whenever it changes, giving you a timeline you can compare — this security group had port 22 open from Tuesday 14:02 until Wednesday 09:15, changed by this principal.
- **Use it when:** compliance rules must be proven rather than promised, or when you need to know what a resource looked like at a point in the past.
- **Rules:** checks written as managed rules, or as custom ones in Lambda or the **Guard** policy language — "is every EBS volume encrypted?", "does every bucket block public access?" — grouped into **conformance packs**. A failing rule can trigger a **remediation action**, an SSM Automation runbook that fixes the violation without a person involved.
- **Aggregators** collect the results from every account and Region into one compliance view for the organization.

### Systems Manager — Fleet Management

Systems Manager (SSM) is an umbrella over a dozen tools for managing servers at scale — connecting to them, patching them, running commands on them and keeping them configured. The ones that matter most:

- **Entry point:** the **SSM Agent** (pre-installed on current Amazon Linux, Ubuntu and Windows AMIs) plus an instance profile granting the `AmazonSSMManagedInstanceCore` policy. That is the whole onboarding; the agent then registers the instance as **managed**.
- **Use it when:** you have EC2 instances at all. Session Manager alone justifies it.
- **Session Manager:** a shell on an instance from the browser or the CLI, **without SSH, without port 22 open, without a bastion host and without a key pair**. Access is controlled by IAM, every session start is in CloudTrail, and the full session can be recorded to S3. This is why modern security groups have no inbound SSH rule at all.
- **Also:** **Patch Manager** (patch baselines applied in maintenance windows), **Run Command** (run a script on a thousand instances at once), **State Manager** (**associations** that *continuously* re-apply a configuration, not a one-time run), **Automation** runbooks (multi-step operational procedures, such as the remediation actions Config uses), **Parameter Store** (a key-value store for configuration and, as `SecureString`, secrets) and **Inventory** (what software is installed where).

### Trusted Advisor, Health Dashboard & Compute Optimizer — The Advisory Layer

Three services that look at your account and tell you things, rather than doing things.

- **Trusted Advisor:** automated checks across cost, security, fault tolerance, performance and **service limits** — "this security group allows SSH from anywhere", "this instance has been idle for two weeks", "you are at 80% of your VPC quota". The full set of checks requires a Business or Enterprise support plan.
- **AWS Health Dashboard:** events affecting *your* account specifically — a scheduled hardware retirement for one of your instances, a degraded service in your Region, an end-of-life notice for a version you run. Connect it to EventBridge so that the events reach a ticket queue or a chat channel instead of waiting to be read.
- **Compute Optimizer:** right-sizing recommendations for EC2 instances, Auto Scaling Groups, EBS volumes, Lambda memory and Fargate tasks, based on your actual CloudWatch history rather than on guesses. This is where a cost review should start; the [AWS interview prep guide](02-aws-interview-prep.md) covers how that conversation is structured.
- **Use them when:** monthly, as a routine — none of them interrupts you, and all three find money and risk that nobody was looking for.

## Where to Go Next

- [AWS Core Concepts](03-aws-core-concepts.md) defines every term used above in one line, with a diagram per section — read it when a word here was unfamiliar.
- [AWS Interview Prep](02-aws-interview-prep.md) turns this catalog into the questions asked about it: the trade-offs, the diagrams to draw and the stories to tell.
- [Containers — Core Concepts and Orchestration](../03-system-design/05-containers.md) explains the ideas behind ECS and EKS — images, containers, pods, orchestration — for readers who want the concepts before the products.
