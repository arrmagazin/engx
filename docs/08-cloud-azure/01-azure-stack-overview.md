---
type: Guide
title: Azure Services Overview
description: Azure core services, networking, storage, identity, and DevOps.
tags: [interview, azure, cloud, devops]
---

# Azure Services Overview

A catalog of the Azure platform service by service — compute, networking, storage and data, messaging, identity, and monitoring — for engineers who need to place each service and its constraints. Every entry follows the same shape: what the service is, its **entry point** (the first object you create, the one that makes the rest of the service make sense), what to **know cold**, and the **trap** the service is known for. The last section maps AWS services to their Azure counterparts.

## Foundations

### The Resource Hierarchy — The Scope Everything Else Inherits From

Every resource sits at a point in a four-level tree, and *scope* is the word that decides who can touch it, what policy applies, and who pays.

- **Entry point:** **management group** → **subscription** → **resource group** → resource. A **subscription** is the billing and **quota** boundary (the counterpart of an AWS account); a **resource group** is a lifecycle container — everything in it deletes together, and it carries a *location* of its own for metadata even when it holds resources from other regions.
- **Know cold:** RBAC assignments and Azure Policy assignments **inherit downward** and only downward. Grant Reader at the management group and it lands on every subscription beneath it; there is no way to grant at a resource and have it apply upward. Resources can be **moved** between resource groups and subscriptions, but not all of them, and the move changes the resource ID.
- **ARM is the single control plane:** portal, CLI, PowerShell, Bicep, Terraform, and Pulumi all end up calling Azure Resource Manager. Which is why "it worked in the portal but not in Terraform" is almost always a permissions or API-version story, not a tooling one.
- **Trap:** regions and **availability zones**. A zone number is *per subscription* — your zone `1` and another subscription's zone `1` may be different physical datacenters. **Region pairs** matter for geo-redundant storage and planned-maintenance ordering; not every region has zones, and that's the first thing to check when a design calls for zone redundancy.

## Compute

### Virtual Machines & VMSS — Rented Virtual Machines

Raw Linux/Windows VMs on Hyper-V, billed per second, with managed disks underneath.

- **Entry point:** an **image** (Marketplace, or your own in an **Azure Compute Gallery**) + a **VM size**, wrapped in a **Virtual Machine Scale Set**. In production you rarely deploy a standalone VM — you define a scale set model and let it create, scale, and reimage instances for you.
- **Know cold:** series letters encode purpose — `D` general purpose, `F` compute-optimized, `E` memory-optimized, `B` burstable (CPU credits), `L` storage-optimized, `N` GPU (`NC` compute, `ND` deep learning, `NV` visualization). Suffixes stack: `a` = AMD, `p` = **Ampere Arm** (the cheaper-per-core option, Azure's Graviton answer), `s` = premium-storage capable, `d` = has a local temp disk.
- **VMSS orchestration:** **Flexible** (the default and the modern answer — instances are ordinary VMs you can address individually, spread across zones and fault domains) vs. **Uniform** (identical, anonymous instances; the older model, still used for large stateless fleets). **Availability sets** are the pre-zone construct: fault domains and update domains inside one datacenter. Zones beat sets whenever the region offers them.
- **Storage choice:** managed disk OS (network disk, survives deallocation) vs. **ephemeral OS disk** (lives on the host's local storage, free, much faster to reimage, *wiped on deallocate or reimage*). Ephemeral OS disks are the immutable-infrastructure-friendly choice.
- **Trap:** **deallocated** ≠ **stopped**. A VM stopped from inside the guest keeps billing compute; you must *deallocate* to stop paying, and deallocation releases any dynamic public IP and destroys ephemeral OS disk contents. Basic-SKU public IPs and Basic Load Balancer retired in September 2025 — Standard SKU (static, zone-aware) is the only answer for new work.

### AKS — Managed Kubernetes

Microsoft runs the control plane; everything else is upstream Kubernetes.

- **Entry point:** the **cluster**, plus two decisions that are painful to change later — the **node pool layout** (a `System` pool for CoreDNS and friends, `User` pools for workloads, each pool one VM size) and the **network plugin**.
- **Networking, the decision that dates you:** **Azure CNI Overlay** is the recommendation for new clusters — pods get IPs from a private overlay CIDR that never touches your VNet, so VNet address space stays small. It is a recommendation, not a universal default: which plugin you get when you don't specify one depends on the creation path. **Azure CNI (node subnet)** gives every pod a routable VNet IP, which is what you want for direct pod addressability and what exhausts your CIDR when you don't. **kubenet** is legacy, with a retirement announced.
- **Pods calling Azure APIs:** **Entra Workload ID** — the cluster gets an OIDC issuer, a Kubernetes service account is federated to a user-assigned managed identity, and the pod gets a token with no secret anywhere. It replaced AAD Pod Identity, which was retired in September 2024. The alternative — granting the *kubelet* identity broad rights — gives every pod on the node the same access.
- **Scaling:** the **cluster autoscaler** grows existing node pools within min/max and is still the default; **Node Auto Provisioning** (Karpenter, upstream) provisions right-sized nodes directly from pending pods and is the current recommendation. **KEDA** scales *pods* from queue depth, not CPU — the add-on for event-driven workloads.
- **Trap:** the two identities. The **cluster identity** manages Azure resources on the cluster's behalf (load balancers, disks, route tables); the **kubelet identity** pulls from ACR. Confusing them produces the classic `ImagePullBackOff` that no amount of RBAC fixes.

### Container Apps — Serverless Containers

Kubernetes, KEDA, Dapr, and Envoy assembled and hidden. You get revisions and scale rules; you never see a node.

- **Entry point:** a **Container Apps environment** — the boundary that holds the shared VNet integration, the Log Analytics workspace, and the internal service mesh. Apps inside one environment reach each other by name over the internal ingress; apps in different environments do not.
- **Know cold:** **revisions** are immutable snapshots of a container app, and you can run several at once with **traffic weights** — blue/green and canary come for free, no load balancer to configure. **Scale rules** are KEDA scalers (HTTP concurrency, queue length, cron, custom), and `minReplicas: 0` means genuine scale-to-zero. **Workload profiles** let one environment mix Consumption (per-second, scale to zero) with Dedicated (reserved compute, GPUs, larger sizes).
- **Also:** **jobs** (run-to-completion tasks — manual, scheduled, or event-driven) cover what you'd otherwise reach for ACI to do, and **Dapr** is an opt-in sidecar for pub/sub, state, and service invocation.
- **Trap:** scale-to-zero plus HTTP ingress means the first request after idle pays a cold start, and there is no `kubectl`. When you need daemonsets, custom CRDs, admission controllers, or a service mesh you chose yourself, you have outgrown Container Apps and you're describing AKS.

### Azure Functions — Functions, No Servers

You write a handler; the runtime invokes it when a trigger fires.

- **Entry point:** a **trigger** plus **bindings** — and bindings are the real differentiator. A function can declare "triggered by a Service Bus queue, with an *output binding* to Cosmos DB" and never write a client SDK call. One trigger per function; input and output bindings are declarative.
- **Hosting plans, in order of how often they're picked wrong:** **Consumption** (scale to zero, no VNet on the classic plan, **5-minute default timeout, 10-minute hard cap**), **Flex Consumption** (the modern default — scale to zero *and* VNet integration, per-instance concurrency control, and the 10-minute cap lifted), **Premium** (pre-warmed instances, no cold start, VNet, unbounded runtime), **Dedicated** (rides an existing App Service Plan).
- **Durable Functions:** orchestrator, activity, and entity functions for workflows — fan-out/fan-in, human approval, long-running sagas. **The orchestrator replays from an event-sourced history, so its code must be deterministic**: no `DateTime.Now`, no `Guid.NewGuid()`, no direct I/O. That constraint is the interview question.
- **Trap:** databases and sockets. Hundreds of concurrent instances each opening a connection exhausts both the backend and the plan's own outbound SNAT port allocation — reuse clients as statics, and reach for connection pooling or a Premium plan with VNet integration before blaming the database.

### App Service / Static Web Apps / ACI — The "Just Run My App" Tier

- **App Service:** managed web hosting for code or containers. The entry point is the **App Service Plan** — the VM fleet you actually pay for; apps are tenants on it, so plan sizing is a *shared* decision and noisy neighbours are real. **Deployment slots** give you staged deploys with a **swap** that warms the target first; app settings marked *deployment slot setting* stay pinned to their slot, and forgetting that is how staging config reaches production. Turn **Always On** on or the app unloads when idle.
- **Static Web Apps:** static frontend on a global CDN plus a managed Functions API, with per-PR preview environments built in.
- **Azure Container Instances:** a single **container group**, per-second billing, no orchestrator. Good for one-shot jobs and burst; largely superseded by Container Apps jobs for new work.
- **Why they're on the list:** not every workload needs AKS. App Service or Container Apps often meets the requirement with far less to operate, and reaching for them is a design decision worth stating explicitly.

## Networking

### VNets, Subnets & Routing — The Foundation Everything Else Sits In

A software-defined network you own, defined by an address space.

- **Entry point:** the **address space**, then **subnets**, then **route tables (UDRs)**. Two differences from AWS worth stating out loud: a **subnet is regional, not zonal** — it spans every zone in the region, and the *resource* picks its zone — and every subnet in a VNet can already reach every other, because system routes exist from the start. There is no internet gateway to attach.
- **Egress:** outbound internet used to be on by default. **Default outbound access retired for new deployments in September 2025**, so a new subnet needs an *explicit* method: a **NAT Gateway** (the right answer — a zonal resource with a stable outbound IP and no SNAT port exhaustion), a load balancer outbound rule, or a public IP on the instance.
- **Forcing traffic through inspection:** a UDR sending `0.0.0.0/0` to a `VirtualAppliance` next hop is how you route spokes through **Azure Firewall** or a third-party NVA. **Service endpoint policies** and **BGP route propagation** flags decide whether your override actually wins.
- **Trap:** each subnet loses **five** addresses to Azure (network, gateway, two DNS, broadcast), and several services demand a **dedicated, empty, correctly-named subnet** — `AzureFirewallSubnet`, `GatewaySubnet`, `AzureBastionSubnet`, App Gateway's own subnet. Discovering the naming requirement after the address plan is set is a rebuild.

### NSGs, ASGs & Azure Firewall — The Filtering Layers

| Aspect | Network Security Group | Azure Firewall |
|---|---|---|
| **Attaches to** | A subnet **and/or** a NIC | Its own subnet, as a next hop |
| **Layer** | 3–4 (plus service tags) | 3–7, with FQDN and TLS inspection |
| **State** | Stateful — return traffic is automatic | Stateful |
| **Rules** | Allow **and** deny, evaluated by **priority number** (lowest wins) | Rule collection groups, NAT/network/application rules |
| **Cost** | Free | A fixed hourly deployment charge **plus** a per-GB data-processing charge |

- **Entry point:** the idiomatic Azure pattern is an **Application Security Group** — `asg-db` allows 5432 *from `asg-app`*, not from a CIDR. NICs join ASGs, so the rule keeps working as the fleet scales. It's the same instinct as referencing one security group from another, and it's the answer that signals you've run this.
- **Service tags** (`Storage`, `AzureKeyVault`, `Internet`, `VirtualNetwork`) are Microsoft-maintained IP sets — use them instead of hardcoding ranges that change monthly.
- **Know cold:** when an NSG sits on both the subnet and the NIC, **inbound is evaluated subnet-first then NIC, outbound NIC-first then subnet** — both must allow. Default rules already permit VNet-to-VNet and the load balancer probe, and deny inbound internet.

### Load Balancing — Load Balancer, Application Gateway, Front Door, Traffic Manager

- **Entry point:** for **Azure Load Balancer**, a **frontend IP** → **rules** → a **backend pool** with a **health probe**. For **Application Gateway**, a **listener** → **routing rule** → **backend pool** + **HTTP settings**. As in AWS, health checking and draining live on the backend/probe, not the frontend.

| Service | Layer | Scope | Use it for |
|---|---|---|---|
| **Load Balancer** | 4 (TCP/UDP) | Regional | Extreme throughput, non-HTTP protocols, zone-redundant frontends, outbound SNAT |
| **Application Gateway** | 7 (HTTP) | Regional | Path/host routing, **WAF**, TLS termination and re-encryption, cookie affinity, autoscaling (v2) |
| **Front Door** | 7 (HTTP) | **Global** | Anycast edge, caching, WAF at the edge, global failover, split-TCP acceleration |
| **Traffic Manager** | DNS | Global | DNS-level steering (priority, weighted, performance, geographic) — including to non-Azure endpoints |

- **Know cold:** Front Door is the CDN answer for new work — **Azure CDN from Edgio** retired on 15 January 2025, and **Azure CDN Standard from Microsoft** has a separate, later announced retirement date. **Front Door Premium** can reach an origin over **Private Link**, so the backend needs no public IP at all. Traffic Manager resolves names and then steps out of the path, so it fails over at DNS TTL speed, not instantly.
- **Trap:** Application Gateway v2 needs its **own dedicated subnet** with room to scale, and WAF in *Prevention* mode will block legitimate traffic until you have tuned exclusions — run *Detection* first.

### Azure DNS & Private DNS Zones

- **Entry point:** a **zone** — **public** (authoritative on the internet) or **private** (resolvable only from VNets you attach with a **virtual network link**, optionally with **autoregistration** of VM records).
- **Know cold:** **alias records** point at Azure resources (public IP, Front Door, Traffic Manager), update automatically when the target changes, and work at the **zone apex** — which is why you can't CNAME `example.com` at an endpoint. DNS forbids CNAME at the apex; alias is Azure's answer.
- **Azure DNS Private Resolver** is what replaces hand-built DNS forwarder VMs for hybrid resolution — inbound and outbound endpoints with forwarding rulesets, and it is the current answer to "how does on-prem resolve my private endpoints".

### VNet Peering & Virtual WAN — Connecting Networks

- **VNet peering:** a 1:1 link, cheap, full bandwidth, and **non-transitive**. A↔B and B↔C does *not* give A↔C — so hub-and-spoke needs either UDRs pointing spokes at a hub firewall, or a gateway. Two flags decide whether it works: **allow forwarded traffic** (accept packets not originating in the peer) and **gateway transit** (let spokes use the hub's VPN/ExpressRoute gateway).
- **Virtual WAN:** the managed hub. A **virtual hub** absorbs VNet connections, VPN, ExpressRoute, and firewall into one Microsoft-managed object with automatic transitive routing and **hub route tables** — the Transit Gateway analogue, for estates where the hand-built hub VNet has stopped scaling.
- **Trap, for both:** overlapping address spaces. Nothing peers between two VNets that both use `10.0.0.0/16`. Plan address space centrally *before* it becomes a migration.

### ExpressRoute & VPN Gateway — Reaching On-Prem

- **VPN Gateway:** IPsec tunnels over the public internet. Live in under an hour, but bandwidth and jitter follow the internet. Deploy **active-active** across zones; the SKU sets the throughput ceiling and can only be resized within a family.
- **ExpressRoute:** a dedicated private circuit through a partner. Consistent latency, higher throughput, **lead time in weeks** — say that, it's the operational reality. **Private peering** reaches your VNets; **Microsoft peering** reaches public Microsoft 365 and PaaS endpoints.
- **The standard answer:** ExpressRoute primary, VPN as the automatic backup — with **ExpressRoute Global Reach** if two on-prem sites should talk through Microsoft's backbone.

### Private Link & Service Endpoints — Reaching PaaS Privately

- **Service endpoints:** a route-table optimization. Traffic to the service leaves over the Azure backbone and arrives *carrying your subnet identity*, so the storage firewall can allow it — but it still goes to the service's **public** endpoint, it's whole-service (not one account), and it does nothing for on-prem. They're **free**.
- **Private endpoints:** a **NIC with a private IP in your subnet**, mapped to *one specific resource* (this storage account, this SQL server, this Key Vault). The public endpoint can then be disabled entirely, and on-prem reaches it over ExpressRoute/VPN. Billed hourly plus per GB.
- **Private Link Service:** publish *your own* service behind a **Standard Load Balancer** so other VNets, subscriptions, and tenants consume it through their own private endpoint — no peering, no route sharing, and overlapping address spaces stop mattering. This is the SaaS-on-Azure connectivity pattern.
- **Trap — the one that catches most teams:** **DNS**. A private endpoint only works when `myaccount.blob.core.windows.net` resolves to the private IP, which requires the `privatelink.blob.core.windows.net` **private DNS zone** linked to the querying VNet and populated by the endpoint's DNS zone group. Get the networking perfect and the DNS wrong and every client silently keeps using the public IP.

## Storage & Data

### Storage Accounts — Blob, Files, Queues, Tables

One resource, four services. Not a filesystem: Blob is a flat key-value store of objects under a globally-unique account name.

- **Entry point:** the **storage account** — and it is a bigger unit than an S3 bucket. Redundancy, firewall, encryption, access tier default, and *throughput limits* are all set at the **account** level; **containers** and blobs sit beneath it. That is the first thing to internalise coming from AWS.
- **Redundancy:** **LRS** (three copies, one datacenter) → **ZRS** (across zones in the region) → **GRS** (LRS plus async copy to the paired region) → **GZRS**. Add **RA-** for read access to the secondary. Geo-replication is **asynchronous**, so failover has a real RPO, and customer-initiated failover converts the account to LRS afterwards.
- **Tiers & lifecycle:** Hot → Cool → Cold → **Archive** (offline; rehydration takes **hours**, and there is no way to read it faster than the rehydration priority allows). Minimum retention periods mean early deletion is charged as if the data stayed. **Lifecycle management policies** handle tiering and expiry, including old blob *versions*.
- **Access — the highest-signal Azure trap:** the control plane and data plane are separate. **Owner on the storage account grants you exactly zero blob data access**; reading data needs a *data* role like **Storage Blob Data Contributor**. Prefer Entra RBAC over keys; if you must hand out a URL, use a **user-delegation SAS** (signed with an Entra key, revocable, time-boxed) rather than an account-key SAS, and disable shared key auth entirely where you can.
- **Know cold:** **hierarchical namespace** turns the account into **ADLS Gen2** — real directories, atomic rename, POSIX ACLs. Enabling it is normally a creation-time choice, though an upgrade path now exists for accounts created without it; there is no way back once it is on. Throughput limits are per *account* and shared across Blob, Queue, and Table, which is how one chatty table service throttles unrelated blob traffic — Microsoft's published scalability target is on the order of 20,000 requests per second per account, and the current figure is worth checking before you design to it.

### Managed Disks — Block Storage for One VM

Network-attached virtual disks that behave like local ones.

- **Entry point:** a **disk** in a specific region and zone, attached to one VM (shared disks exist for clustering). Zone-bound: to move it, snapshot it — or use a **ZRS** disk, which can attach from any zone in the region.
- **Premium SSD v2 — the cost win to name:** on Premium SSD (P-tiers), IOPS and throughput are tied to the size tier, so people over-provisioned capacity to buy performance. **v2 decouples them**: pick capacity, IOPS, and throughput independently, with a 3,000 IOPS / 125 MB/s baseline included. The catch is that v2 requires a zonal deployment and supports no host caching.
- **The ladder:** Standard HDD → Standard SSD → Premium SSD (with **bursting**) → Premium SSD v2 → **Ultra Disk** for sustained sub-millisecond, high-IOPS databases.
- **Snapshots** are incremental and regional; the **Azure Compute Gallery** is where you version and replicate *images* across regions for immutable deployments.

### Azure Files & NetApp Files — Shared Filesystems

- **Azure Files:** managed SMB and NFS shares, mountable by many VMs and containers at once. **Premium (FileStorage)** is provisioned SSD, Standard is pay-as-you-go HDD. Identity-based access via on-prem AD DS or Entra Domain Services; **Azure File Sync** turns a Windows Server into a cache tier over a cloud share, which is the classic hybrid file-server modernisation.
- **Azure NetApp Files:** bare-metal NetApp for HPC, SAP, and latency-sensitive NFS, with snapshots and cross-region replication.
- **Judgement point:** shared filesystems are often a lift-and-shift crutch. Cloud-native usually means Blob plus a database.

### Azure SQL & the Flexible Servers — Managed Relational Databases

- **Entry point:** **Azure SQL Database** gives you a single database on a logical **server** (a namespace and firewall boundary, not a machine). **Managed Instance** gives you near-full SQL Server — SQL Agent, cross-database queries, CLR — injected into your VNet, for lift-and-shift. **PostgreSQL / MySQL Flexible Server** is the open-source equivalent, VNet-injectable, with configurable maintenance windows.
- **Know this cold — the service tiers *are* the HA story:** **General Purpose** separates compute from remote storage, so failover is a restart on another node (tens of seconds). **Business Critical** keeps local SSD and an Always On replica set, so failover is seconds — *and it includes a free readable replica*. **Hyperscale** decouples storage into page servers, with near-instant restore and fast replica seeding, and a maximum database size well past the other tiers — Microsoft publishes the current ceiling, 128 TB. The distinction to hold on to is that the tier is the availability model, not only a performance grade.
- **Scaling & elasticity:** **vCore** (the model to use — maps to hardware and supports Azure Hybrid Benefit) vs. the legacy **DTU** blend. **Serverless** auto-pauses when idle and bills per second. **Elastic pools** share capacity across many small databases with uncorrelated peaks.
- **Cross-region:** **failover groups** wrap geo-replication in a stable listener endpoint so the connection string survives failover. Without one, DR means editing connection strings under pressure.

### Cosmos DB — Managed NoSQL at Any Scale

Single-digit millisecond reads at any size, if and only if you model it correctly.

- **Entry point:** an **account** (the **API is fixed at creation** — NoSQL, MongoDB, Cassandra, Gremlin, or Table; NoSQL is the first-class one), then a database, then a **container** with its **partition key**. The key is **immutable**, so the order of work inverts from SQL: list your access patterns first, then choose a key that serves them.
- **The currency is RU/s:** every read, write, and query is priced in Request Units. **Provisioned** (with autoscale between 10% and max) vs. **serverless** (pay per request, low ceiling, good for dev and spiky small workloads). Throughput is set at the database or the container.
- **Five consistency levels:** Strong, Bounded Staleness, **Session** (the default, and the right one for most apps — read-your-own-writes per client), Consistent Prefix, Eventual. Each step weaker is cheaper in RUs and higher in availability. Being able to justify Session is the answer.
- **Extras:** the **change feed** → Functions for change-data-capture, TTL for expiry, **multi-region writes** with a conflict resolution policy, and an integrated cache for repeated reads.
- **Trap:** a **hot partition** — a key like `status` concentrates traffic on one physical partition and throttles (429s) while the container sits mostly idle. A **logical partition is also size-capped** — Microsoft documents the ceiling, currently 20 GB — which turns a low-cardinality key into a hard wall, not a slowdown.

### Azure Cache for Redis & AI Search — The Supporting Data Stores

- **Azure Cache for Redis:** entry point is a **cache instance** and its tier — Basic (single node, no SLA), Standard (replicated), **Premium** (VNet injection or private endpoint, persistence, clustering, geo-replication), with Enterprise tiers for Redis modules. Used for cache-aside, sessions, rate limits, and distributed locks.
- **Azure AI Search:** managed search over your own content — entry point is a **service** with **indexes**, **indexers** (pull from Blob, SQL, Cosmos), and **skillsets**. Full-text, vector, and hybrid search in one index, which is why it's now the default retrieval layer for RAG on Azure.
- **Log Analytics** covers the "search my logs" half of what OpenSearch does on AWS — see *Azure Monitor* below.

## Messaging & Events

These four are constantly confused, and picking correctly between them is a genuine signal of experience. The one-liner: **Storage Queues** for simple work handoff, **Service Bus** for enterprise messaging, **Event Grid** for reactive routing, **Event Hubs** for telemetry at scale.

### Storage Queues — The Simple Buffer

- **Entry point:** a **queue** inside a storage account. Messages up to 64 KB, a queue up to the account's capacity, dequeue with a **visibility timeout** and delete on success.
- **Use it when:** you need a cheap durable buffer and nothing else — no topics, no sessions, no transactions, no ordering guarantee. If the requirements grow past that list, you wanted Service Bus.

### Service Bus — The Enterprise Broker

- **Entry point:** a **namespace** (tier matters: Basic has queues only, **Standard adds topics**, **Premium** gives dedicated capacity, VNet/private endpoints and 100 MB messages), then a **queue**, or a **topic** with **subscriptions** carrying SQL-like **filters**.
- **Know cold:** **peek-lock** (receive, process, complete — with a **lock duration up to 5 minutes that you must renew** for longer work) vs. receive-and-delete. Dead-lettering is built in, with a reason attached. **Sessions** give strict FIFO *per session ID*; **duplicate detection** dedupes by message ID inside a time window; scheduled messages, transactions, and auto-forwarding round it out.
- **Trap:** the lock duration is the visibility-timeout mistake under another name — if processing outlives the lock and nobody renews it, the message is redelivered mid-flight and you have processed it twice.

### Event Grid — The Router

- **Entry point:** a **topic** — a **system topic** (Azure resources emitting their own events: "a blob was created", "a VM was deallocated", "a resource health event fired"), a **custom topic** for your own events, or a **domain** for multi-tenant fan-out. Then **event subscriptions** with filters, push delivery, retry with exponential backoff, and dead-lettering to Blob.
- **Why it matters:** it is *the* way to react to infrastructure changes without polling, and it is the glue that makes "blob lands → function runs" work without a timer.
- **vs. Service Bus:** Event Grid carries lightweight **notifications** that something happened, at massive fan-out and low latency, with at-least-once push. Service Bus carries **commands and business messages** you must not lose or reorder. Event Grid **namespaces** add MQTT and pull delivery when push doesn't suit the consumer.

### Event Hubs — The Log

- **Entry point:** a **namespace** → an **event hub** → **partitions**. Consumers join a **consumer group** and track their own **checkpoint** in Blob storage, so they can rewind and replay — that replay ability is the core difference from Service Bus, where a completed message is gone.
- **Know cold:** retention is 1 day on Basic, up to 7 on Standard, up to 90 on Premium/Dedicated. **Capture** writes the stream to Blob or ADLS automatically in Avro, with no code. The **Kafka protocol endpoint** (Standard and above) means existing Kafka producers and consumers connect by changing a connection string — that is usually the right answer instead of running Kafka on VMs.
- **Trap:** partition count sets your maximum consumer parallelism and, on most tiers, **cannot be changed after creation**. Under-partition and the only fix is a new hub and a migration.

## Identity

### Microsoft Entra ID — The Directory Underneath Everything

- **Entry point:** the **tenant** — the directory itself. A subscription *trusts* exactly one tenant for authentication, and moving a subscription between tenants invalidates every role assignment in it.
- **Know cold — the pair everyone garbles:** an **App Registration** is the *global definition* of an application (its identifier URI, redirect URIs, API permissions, credentials). An **Enterprise Application** is the **service principal** — the local instance of that app inside one tenant, where consent and role assignments actually live. One registration, one service principal per tenant that uses it.
- **Two role systems, and they are not the same:** **Entra roles** (Global Administrator, User Administrator, Application Administrator) govern the *directory*. **Azure RBAC roles** (Owner, Contributor, Reader) govern *resources*. A Global Admin has no resource access by default — though they can elevate themselves to User Access Administrator at root scope, which is exactly why that action is audited and alerted on.
- **Conditional Access** is where MFA, device compliance, and location policy are actually enforced — the answer to "how do you secure admin access" is a Conditional Access policy plus **PIM** (Privileged Identity Management) for just-in-time, time-boxed, approval-gated role activation.

### Azure RBAC — The Authorization Model

- **Entry point:** a **role assignment** = **principal × role definition × scope**. A role definition is a set of `Actions` / `NotActions` (control plane) and `DataActions` / `NotDataActions` (data plane) — and that split is the storage trap from earlier, generalised.
- **Evaluation:** assignments are **additive and inherited downward**; there is no user-authored `Deny`. **Deny assignments** exist but are created only by Azure itself (managed applications, deny settings on deployment stacks). The absence of an SCP-style deny is why **Azure Policy** carries the guardrail role — see below.
- **Know cold:** prefer **groups** over users at the assignment, assign at the **highest scope that is still correct**, and use **PIM** for anything privileged. Custom roles are a `NotActions` exercise most of the time — start from a built-in role and subtract.

### Managed Identities — The Compute-to-Azure Bridge

The Azure answer to "no credentials anywhere, ever".

- **Entry point:** enable identity on the resource. **System-assigned** is created with the resource and deleted with it — one identity, one resource, no lifecycle management. **User-assigned** is a standalone resource you create first, attach to many resources, and — crucially — can be granted roles *before* the workload exists, which removes the deploy-time race where an app starts before its permissions land.
- **How it works:** the SDK's `DefaultAzureCredential` fetches a token from the local identity endpoint — **IMDS at `169.254.169.254`** on VMs and VMSS, an injected `IDENTITY_ENDPOINT` on App Service, Functions, and Container Apps. No secret is stored, and the token is short-lived.
- **Where it plugs in:** Key Vault, Storage, ACR, SQL (`CREATE USER [my-identity] FROM EXTERNAL PROVIDER`), Service Bus, Cosmos. If a design still has a connection string in app settings, replacing it with a managed identity is the improvement to propose.

### Workload Identity Federation — Keyless Pipelines

- **Entry point:** add a **federated credential** to an app registration or a user-assigned managed identity, conditioned on the token's **issuer** and **subject** — `repo:org/repo:ref:refs/heads/main` for GitHub Actions, or the Azure DevOps service connection's subject. The pipeline exchanges its own OIDC token for an Azure token; no client secret exists to leak or rotate.
- **Why it matters:** it deletes the entire category of long-lived CI credentials, and it is the single highest-signal thing you can mention in a CI/CD discussion. The same mechanism is what **Entra Workload ID** uses for AKS pods.

### Key Vault — Secrets, Keys, and Certificates

- **Entry point:** a **vault**, and immediately its **permission model** — legacy **access policies** (per-vault, all-or-nothing per operation, no inheritance) vs. **Azure RBAC** (the recommended model: real roles, management-group inheritance, PIM-eligible). Migrating a vault from access policies to RBAC is a common real-world task and a good story.
- **Know cold:** **soft delete is mandatory** and cannot be turned off — a deleted vault or secret lingers for the retention period, and re-creating a vault with the same name fails until you purge it. **Purge protection** goes further and blocks purging entirely, which some services require before they will use the vault. That is the "my Terraform destroy/apply loop broke" story.
- **Also:** **certificates** with auto-renewal through integrated CAs; **Key Vault references** (`@Microsoft.KeyVault(...)`) so App Service, Functions, and Container Apps resolve secrets at runtime with their managed identity and never store them; **Managed HSM** for keys in a **FIPS 140-validated single-tenant HSM**; and per-vault **throttling limits**, which is why you cache secrets rather than fetching per request.
- **Trap:** the vault firewall. Turning on network restrictions without adding your private endpoint, the *trusted Microsoft services* exception, or the deployment agent's IP locks out the very pipeline that manages the vault.

## Monitoring & Management

### Azure Monitor — Metrics, Logs, and Alerts

One service, two different data types, and knowing which one you're in explains most confusion.

- **Entry point:** a **Log Analytics workspace** plus a **diagnostic setting** on each resource. **This is the gotcha that matters**: platform metrics are collected automatically, but a resource emits *no logs anywhere* until you create a diagnostic setting routing them to a workspace, a storage account, or an Event Hub. "Why is there no data" is nearly always a missing diagnostic setting.
- **Metrics vs. logs:** metrics are pre-aggregated time series — cheap, one-minute granularity, queried by namespace and **dimensions**. Logs are schema-on-read tables queried with **KQL**, billed **per GB ingested plus retention**, and far more expressive. Send high-cardinality detail to logs, alert thresholds off metrics.
- **Alerts:** **metric alerts** (fast, cheap, with dynamic thresholds that learn the baseline), **log search alerts** (any KQL query, slower and billed per evaluation), **activity log alerts** (someone deleted something). All fire into **action groups** (email, webhook, Logic App, ITSM), with **alert processing rules** for maintenance-window suppression.
- **Agents:** the **Azure Monitor Agent** plus **Data Collection Rules** — a DCR declares what to collect and where to send it, decoupled from the machine. It replaced the Log Analytics agent (MMA/OMS), which was retired on 31 August 2024.

### Application Insights — APM and Distributed Tracing

- **Entry point:** a **workspace-based** Application Insights resource (classic resources were retired in February 2024, so workspace-based is the only mode) and an instrumentation key or, preferably, a connection string in the app.
- **Know cold:** the **Azure Monitor OpenTelemetry distro** is the current instrumentation answer — instrument with OTel, export to App Insights *or* a third-party backend, don't lock your instrumentation to one vendor. Traces correlate across services through the W3C `traceparent` header, which is what makes the **application map** and end-to-end transaction view work.
- **Cost control is sampling:** adaptive sampling on by default, ingestion sampling as a backstop. **Live Metrics** streams unsampled data for the minute you're watching a deploy.

### Activity Log & Auditing — The "Who Did This" Layer

- **Entry point:** the **Activity Log** — every control-plane write against ARM, retained **90 days for free**, and exported past that with (again) a diagnostic setting. It answers *who created, changed, or deleted this resource, from where, and when*.
- **Boundary to state:** the Activity Log records **API calls**, not contents. Data-plane auditing is **per service** — storage diagnostics, Key Vault logs, SQL audit — each enabled individually, which is genuinely more work than flipping one global switch.
- **Separate stream:** Entra **sign-in** and **audit** logs live in the directory, not the subscription, and need their own diagnostic setting to reach the workspace. Security investigations normally need both streams joined.

### Azure Policy — Governance and the Guardrail That RBAC Can't Give You

- **Entry point:** a **policy definition** with an **effect**, assigned at a scope. The effects, in ascending order of intervention: `Audit` → `AuditIfNotExists` → `Append` / `Modify` → `DeployIfNotExists` → **`Deny`**. Group definitions into **initiatives** (policy sets), and add **exemptions** with expiry rather than removing the policy.
- **Why it's structural:** with no user-authored deny assignments in RBAC, `Deny` policies are how you enforce "no public IPs", "only these regions", "every resource must be tagged". `DeployIfNotExists` plus a remediation task and a managed identity is how you *fix* existing violations — the closest thing to a self-healing estate.
- **Compliance view:** built-in initiatives map to CIS, ISO 27001, NIST, and PCI, and roll into **Microsoft Defender for Cloud**'s secure score and regulatory compliance dashboard.

### Update Manager, Automation, Run Command & Bastion — Fleet Management

Azure has no single Systems Manager; the same job is split across a handful of services, and saying so cleanly is worth more than listing them.

- **Azure Bastion:** browser or native-client RDP/SSH **without a public IP, without port 22/3389 exposed, and without a jump box you patch yourself**. This is the concrete security-improvement story.
- **Azure Update Manager:** patch assessment and scheduled deployment across Azure and (via Arc) on-prem machines, with maintenance configurations. No agent onboarding of its own.
- **Run Command / Custom Script Extension:** ad-hoc and bootstrap execution on VMs, through the control plane rather than the network.
- **Azure Automation:** runbooks (PowerShell/Python) on a schedule or a webhook — the general-purpose ops glue — plus **Machine Configuration** (formerly Guest Configuration, the DSC successor) for *continuous* desired-state auditing and enforcement rather than one-shot runs.
- **Azure Arc:** projects the entire control plane — Policy, Monitor, Update Manager, Defender, RBAC — onto servers, Kubernetes clusters, and databases running on-prem or in another cloud. The answer to any hybrid governance question.

### Advisor, Service Health & Cost Management — The Advisory Layer

- **Azure Advisor:** automated recommendations across reliability, security, performance, **cost**, and operational excellence, including right-sizing and idle-resource detection based on your own metrics. Where a cost-reduction conversation should start (see *Cost management* in the prep guide).
- **Service Health vs. Resource Health:** Service Health covers Azure-side incidents, planned maintenance, and service retirements affecting *your* subscriptions; **Resource Health** tells you whether *this specific resource* is healthy and why it last wasn't. Wire both to alerts instead of reading dashboards.
- **Cost Management:** budgets with action groups, cost analysis grouped by tag, and the three commitment levers — **Reservations** (1/3-year, specific SKU family and region), **Savings Plans** (1/3-year, spend commitment, flexible across compute), and **Spot** (deep discount, evictable at 30 seconds' notice). **Azure Hybrid Benefit** reuses existing Windows Server and SQL Server licenses and is regularly the largest single line-item saving in a Microsoft-heavy estate.

## AWS to Azure Service Map

Mappings are approximate. Where the two services differ in shape, the third column names the difference.

| AWS | Azure | Where the analogy breaks down |
|---|---|---|
| **Account** | Subscription | The billing, quota, and isolation boundary on both sides; management groups sit above it and answer to Organizations OUs, while resource groups sit below and have no AWS equivalent |
| **EC2** | Virtual Machines | Subnets are regional in Azure; the VM picks the zone |
| **Auto Scaling group** | Virtual Machine Scale Sets | Flexible orchestration keeps instances individually addressable; Uniform is the older, anonymous-instance model |
| **ECS / Fargate** | Container Apps | Container Apps bundles KEDA, Dapr, and revision-based traffic splitting |
| **EKS** | AKS | Control plane is free on the AKS Free tier (no SLA) |
| **ECR** | Azure Container Registry | The AKS *kubelet* identity needs the pull role, not the cluster identity |
| **Lambda** | Azure Functions | Bindings are declarative I/O; Durable Functions has no Lambda equivalent |
| **Step Functions** | Durable Functions / Logic Apps | Durable orchestrators are ordinary code and must be deterministic; Logic Apps is the low-code connector path |
| **VPC / Internet Gateway** | VNet / *(none)* | No IGW; egress is NAT Gateway or another explicit outbound method |
| **Security Group** | NSG + ASG | NSGs support deny rules and priority ordering |
| **ALB / NLB** | Application Gateway / Load Balancer | Application Gateway is the regional L7 tier with WAF; Load Balancer is L4 |
| **CloudFront + Global Accelerator** | Front Door | One service covers the L7 anycast edge, caching, edge WAF, and global failover |
| **Route 53** | Azure DNS + Private DNS Zones | Private DNS is the first place to look when a private endpoint misbehaves |
| **Route 53 routing policies** | Traffic Manager | Both are DNS-level global routing; Route 53's weighted, latency, geolocation, geoproximity, failover, multivalue, and IP-based policies are the same capability |
| **PrivateLink** | Private Link / Private Endpoint | Service endpoints are a coarser, free middle option |
| **Transit Gateway** | Virtual WAN | Hand-built hub-and-spoke with UDRs is still common |
| **Direct Connect** | ExpressRoute | Private peering reaches VNets; Microsoft peering reaches public Microsoft endpoints |
| **Site-to-Site VPN** | VPN Gateway | Deploy active-active across zones; the SKU sets the throughput ceiling and resizes only within a family |
| **S3** | Blob Storage | The *storage account* — not the container — is the limits and firewall boundary |
| **EBS** | Managed Disks | Premium SSD v2 is the gp3 analogue |
| **EFS / FSx** | Azure Files / NetApp Files | Azure Files speaks SMB natively and integrates with AD |
| **RDS / Aurora** | Azure SQL Database / Flexible Server | Service tier *is* the HA model; Hyperscale is the Aurora-shaped tier |
| **DynamoDB** | Cosmos DB | Five consistency levels and RU/s instead of RCU/WCU |
| **ElastiCache** | Azure Cache for Redis | The Premium tier is where VNet injection, persistence, clustering, and geo-replication appear |
| **OpenSearch** | Azure AI Search | Content search only; log search belongs to Log Analytics and KQL |
| **SQS** | Service Bus / Storage Queues | Azure has no direct SNS equivalent |
| **Kinesis / MSK** | Event Hubs | One service, with a Kafka protocol endpoint built in |
| **EventBridge** | Event Grid | System topics cover the "react to infrastructure" case |
| **IAM** | Azure RBAC | Assignments are additive and inherit downward; there is no user-authored deny |
| **IAM roles (instance profiles, IRSA)** | Managed identities | System- vs. user-assigned; user-assigned avoids deploy-time races |
| **IAM Identity Center** | Microsoft Entra ID + PIM | Entra is the directory itself, not a layer on top |
| **SCPs** | Azure Policy (`Deny`) | RBAC has no user-authored deny, so Policy carries the guardrail |
| **KMS** | Key Vault keys / Managed HSM | Managed HSM is the FIPS 140-validated single-tenant option |
| **Secrets Manager** | Key Vault | One vault holds secrets, keys, and certificates; Key Vault references resolve them at runtime |
| **CloudFormation / CDK** | ARM templates / Bicep | Bicep compiles to ARM JSON, and every tool ends at Azure Resource Manager |
| **CloudWatch** | Azure Monitor | Nothing logs until you create a diagnostic setting |
| **CloudTrail** | Activity Log | Control plane only; data-plane auditing is per service |
| **AWS Config** | Azure Policy + Resource Graph | Policy is preventative *and* detective; Config is detective |
| **Systems Manager** | Update Manager + Automation + Run Command + Bastion | No single umbrella service |
| **Trusted Advisor / Compute Optimizer** | Azure Advisor | One service covers all five pillars |
| **Cost Explorer** | Microsoft Cost Management | Budgets, cost analysis by tag, and Advisor's cost recommendations sit in one place |
