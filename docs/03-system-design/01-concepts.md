---
type: Guide
title: System Design Glossary
description: Defines the system design vocabulary this chapter uses, grouped by the problem each set of terms addresses.
tags: [architecture, system-design, interview, glossary]
---

# System Design Glossary

Defines the vocabulary the rest of this chapter uses, grouped by the problem each set of terms addresses. Worked applications of these concepts are in [Canonical Systems](08-canonical-systems.md).

## Capacity Estimation

| Concept | Definition |
|---|---|
| **Capacity Estimation** | Sizing a system's traffic, storage, and bandwidth before designing it, so the design answers to numbers rather than intuition |
| **Back-of-Envelope Estimation** | An order-of-magnitude calculation from a few stated assumptions — writes per second times record size times retention |
| **Read:Write Ratio** | The proportion of reads to writes; decides whether a design optimizes for caching and delivery or for write throughput and consistency |
| **QPS (Queries per Second)** | The standard throughput unit, quoted separately for average and peak load because the two size different components |
| **Storage Growth Projection** | Total storage over a stated horizon, from write rate times record size times time, adjusted for the replication factor |

## Identifier Generation

| Concept | Definition |
|---|---|
| **Identifier Generation** | Producing unique keys for records across many machines without a central allocator on the request path |
| **Distributed ID Generator** | A scheme yielding globally unique, roughly time-ordered 64-bit IDs from independent machines; typically timestamp bits, worker bits, and sequence bits |
| **Sequence Number** | A counter incremented within one timestamp tick on one worker, disambiguating IDs generated in the same millisecond |
| **Clock Skew** | A machine's clock jumping backward after a correction, risking reuse of an already-issued timestamp; detected by refusing to generate while `now < last_timestamp` |
| **Worker ID Assignment** | Giving each generator instance a unique slot automatically rather than by hand, and reclaiming the slot when the instance dies |
| **Lease** | A time-bound claim on a resource, renewed by heartbeat and expiring on its own if the holder crashes |
| **Compare-and-Swap (CAS)** | An atomic update applied only if the current value matches an expected one, used to claim a shared slot without a race |
| **Base62 Encoding** | Representing a number in the 62 URL-safe alphanumeric characters, turning a large integer ID into a short code |

## Sharding

| Concept | Definition |
|---|---|
| **Sharding** | Splitting a dataset across database instances so no single machine holds all of it |
| **Shard Key** | The field deciding which shard a record lives on; chosen to match the dominant query so common lookups reach one shard |
| **Hash-Based Sharding** | Placing records by a hash of the shard key — even load, at the cost of geographic and relational locality |
| **Consistent Hashing** | A placement scheme that relocates only a small fraction of keys when instances are added or removed, unlike `hash % N` |
| **Region-Based Sharding** | Partitioning by geography rather than by hash, used where queries are inherently local |
| **Hot Shard** | One shard or key taking disproportionate traffic, unbalancing a cluster that is otherwise evenly partitioned |

## Load Balancing

| Concept | Definition |
|---|---|
| **Load Balancing** | Spreading incoming requests across a pool of interchangeable servers, so capacity grows by adding machines rather than by enlarging one |
| **Layer 4 Balancing** | Forwarding at the transport level on address and port without reading the request; cheap and protocol-agnostic, but blind to paths, headers, and cookies |
| **Layer 7 Balancing** | Routing on application data such as path, header, or cookie, which buys per-route pools and content-aware policy at the cost of terminating and parsing every request |
| **Balancing Algorithm** | The rule picking the next server — round robin where requests cost the same, least connections where they do not, and a hash of a chosen key where a caller must keep landing on one node |
| **Backend Pool** | The set of interchangeable servers a balancer distributes across, whose membership changes as instances are added, drained, or removed |
| **Health Check** | A periodic probe deciding whether a server stays in the pool, so a failing instance is taken out before users meet its errors |
| **Sticky Session** | Pinning a client to the server holding its state, which keeps that state reachable but unbalances the pool and loses the state outright when that server dies |
| **Cache Affinity** | Routing every request for one key to the same backend so its local copy stays warm, using consistent hashing so that adding a node moves few keys |
| **Connection Draining** | Letting in-flight requests finish on a server already removed from rotation, so a deploy or scale-in does not cut live work short |
| **Single Point of Failure** | A component whose loss takes down everything behind it — the balancer's own exposure, answered by a redundant pair sharing a failover address |
| **DNS Round Robin** | Distributing at name resolution by handing out different addresses in turn; free, but with no view of server health and with client caches that outlive a failure |

## Caching

| Concept | Definition |
|---|---|
| **Caching** | Keeping a copy of a result closer to its consumer than the system that produced it |
| **Cache-Aside Pattern** | The application reading the cache first and, on a miss, loading from the database and populating the cache |
| **Cache Stampede** | Many requests missing the same key at once and all reaching the database together; mitigated by request coalescing or jittered expiry |
| **Cache Invalidation** | Purging or versioning a cached copy when the data behind it changes |

## Content Delivery Network

| Concept | Definition |
|---|---|
| **Content Delivery Network (CDN)** | Geographically distributed edge servers holding static and semi-static content close to users, cutting latency and origin load |
| **301 vs. 302 Redirect** | The choice between a permanent redirect browsers cache, which saves requests but hides per-click data, and a temporary one that reaches the server every time |
| **Adaptive Bitrate Streaming** | Video published as short segments at several quality levels, with the client switching level as network conditions change; HLS and DASH are the two standards in use |

## Consistency Models

| Concept | Definition |
|---|---|
| **Consistency Model** | The guarantee a system gives about when a write becomes visible to a subsequent read |
| **Eventual Consistency** | Updates propagating asynchronously, so replicas may serve stale data briefly but converge |
| **Strong Consistency** | Every read reflecting the most recent write, required wherever a stale answer is a correctness bug rather than a cosmetic one |
| **Read-Your-Writes Consistency** | A guarantee that a user sees their own recent writes immediately, even while other users may not |
| **Last-Write-Wins (LWW)** | Resolving concurrent writes by keeping the most recent — adequate for counters, lossy for collaborative editing |
| **CAP Theorem** | The result that a distributed system split by a network partition can either keep its replicas in agreement or keep answering requests, but not both while the split lasts; partition tolerance is not a third option a designer trades away, because partitions happen whether or not they were chosen |
| **PACELC** | An extension of the CAP theorem that also names the else-case: with no partition, the standing trade-off is between lower latency and a stronger guarantee, which is the choice a healthy system actually makes every day |

## Idempotency

| Concept | Definition |
|---|---|
| **Idempotency** | The property that applying an operation more than once has the same effect as applying it once |
| **Idempotency Key** | A client-generated unique value per operation, letting the server recognize a retry instead of repeating the side effect |
| **Idempotent Webhook Handling** | A callback handler that checks a unique event ID before acting, so a redelivered event takes effect once |
| **At-Least-Once Delivery** | A guarantee that a message arrives one or more times but never zero, leaving duplicate handling to the receiver |
| **Client-Side Deduplication** | Discarding repeats by message ID on the receiving side, the standard counterpart to at-least-once delivery |

## Concurrency Control

| Concept | Definition |
|---|---|
| **Concurrency Control** | Keeping simultaneous writers from corrupting shared state |
| **Optimistic Concurrency Control** | Reading a version, updating only if it still matches, and retrying on conflict; higher throughput until contention concentrates on one record |
| **Pessimistic Locking** | Taking a lock before modifying a record and blocking other writers until release; simple and correct, but throughput-limiting |
| **Reservation with TTL** | A short-lived hold that expires unless confirmed, separating temporarily held state from committed state |

## Service Decomposition

| Concept | Definition |
|---|---|
| **Service Decomposition** | Dividing a system into independently deployable units and deciding where the lines between them fall |
| **Monolith** | One deployable unit holding the whole application, where calls between modules are in-process and a release ships every part at once |
| **Microservice** | A unit owning one capability and the data behind it, released on its own schedule, at the price of network calls and operational surface where an in-process call once served |
| **Service Boundary** | The line drawn around such a unit, placed where data and reasons to change are cohesive, since a line cutting through either turns routine work into a multi-team release |
| **Bounded Context** | The scope within which one model of a domain term holds without qualification, the usual guide for where that line belongs |
| **Distributed Monolith** | Units deployed separately yet coupled tightly enough that none can ship alone, paying the cost of the split without collecting its benefit |
| **Shared Database Coupling** | Two units reading and writing the same tables, which removes the independence the split was meant to buy because a schema change forces a coordinated release |
| **Remote Call Cost** | What a call becomes once it crosses a process boundary — slow, able to fail on its own, and able to arrive twice — which is why cross-unit operations need retries and repeat-safe handlers |

## Distributed Transactions

| Concept | Definition |
|---|---|
| **Distributed Transaction** | A single logical operation spanning services that share no database and therefore no commit |
| **Saga Pattern** | Running that operation as an ordered series of local transactions, each with an undo step for when a later one fails |
| **Compensating Action** | The undo step in a saga — a refund, a released hold, a canceled reservation |

## Fan-Out

| Concept | Definition |
|---|---|
| **Fan-Out** | The multiplication of one write into many downstream writes or reads, one per recipient |
| **Fan-Out on Write** | Pushing content into every recipient's feed at publish time; fast reads, expensive for accounts with many followers |
| **Fan-Out on Read** | Merging content from followed sources when a feed is requested; cheap writes, costly reads across shards |
| **Celebrity Problem** | One account with a very large follower count making write-time fan-out prohibitive, since a single post triggers millions of writes |
| **Hybrid Fan-Out** | Pushing for ordinary accounts and merging at read time above a follower threshold |

## Feed Ranking

| Concept | Definition |
|---|---|
| **Feed Ranking** | Ordering candidate items for one user by predicted relevance rather than by recency alone |
| **Two-Stage Candidate Generation** | Narrowing a large corpus cheaply and approximately, then scoring only the survivors with an expensive model |
| **Cold-Start Problem** | New items or users having no engagement history, so popularity-based ranking cannot yet place them |
| **Exploration vs. Exploitation** | The trade-off between serving proven content and deliberately serving unproven content to learn its quality |

## Real-Time Delivery

| Concept | Definition |
|---|---|
| **Real-Time Delivery** | Pushing data to a client as it happens, rather than waiting for the client to ask |
| **Persistent Connection** | A connection held open between client and server so the server can send without being polled |
| **Connection Gateway** | A layer holding many open client connections, sharded so each user is pinned to one node |
| **Presence Service** | The mapping from user to the gateway node currently holding their connection, rewritten on every reconnect |
| **Reconnection Storm** | Every client of a failed gateway reconnecting at once, requiring backoff and jitter to avoid toppling the replacement |
| **Message Ordering via Sequence Numbers** | A per-conversation monotonic counter that fixes order and exposes gaps, avoiding reliance on clocks that differ across servers |
| **Server-Authoritative Message Store** | The server holding the definitive durable copy that every device syncs against, rather than each device managing its own queue |
| **Multi-Device Sync** | Keeping message content and read state consistent across one user's logged-in devices |
| **Backpressure** | Limiting how fast work is handed to a component that cannot keep up, through pagination, incremental sync, or queueing |

## Geospatial Indexing

| Concept | Definition |
|---|---|
| **Geospatial Indexing** | Organizing points on the earth's surface so nearby ones can be found without scanning all of them |
| **Geohashing** | Encoding latitude and longitude into a string whose shared prefixes mean physical proximity, which also makes it usable as a shard key |
| **Quadtree** | A tree that recursively subdivides two-dimensional space, subdividing further where points are dense |
| **Google S2 Library** | A production library for spherical geometry and cell-based indexing, used where a rectangular grid distorts |
| **Ring Search** | Querying a small area first and widening it until enough candidates are found |

## Rate Limiting

| Concept | Definition |
|---|---|
| **Rate Limiting** | Capping how many requests a caller may make in a period, to protect capacity and enforce quotas |
| **Fixed Window Counter** | Counting requests per calendar window; simple, but permits a double-rate burst across a window boundary |
| **Sliding Window Log** | Storing each request's timestamp and counting those inside the trailing window; exact, but memory-heavy |
| **Sliding Window Counter** | Approximating the log by weighting the current and previous fixed windows, at constant memory |
| **Token Bucket** | Tokens accruing at a fixed rate and one being spent per request, permitting bursts up to the bucket size |
| **Atomic Increment** | Checking and incrementing a counter in one indivisible step, such as Redis `INCR` inside a Lua script, so two concurrent requests cannot both pass the same limit |

## Search Indexing

| Concept | Definition |
|---|---|
| **Search Indexing** | Precomputing a structure that answers queries by term, instead of scanning every document per query |
| **Inverted Index** | The mapping from each term to the documents containing it |
| **Posting List** | The document IDs recorded against one term in an inverted index, often with positions and frequencies |
| **Crawl Frontier** | The queue of URLs a crawler has yet to fetch, with its prioritization and deduplication rules |
| **Politeness Policy** | A per-domain rate limit that keeps a crawler from overwhelming any one site |
| **Bloom Filter** | A compact probabilistic membership test that can report a false positive but never a false negative |

## Asynchronous Processing

| Concept | Definition |
|---|---|
| **Asynchronous Processing** | Moving work off the request path so a caller is not made to wait for it |
| **Async Event Pipeline** | Publishing events to a queue and handling them in separate consumers, keeping analytics, counters, and indexing off the hot path |
| **Stream Aggregation** | Computing rolling aggregates from an event stream rather than updating one row per event |
| **Write Amplification via Row-Lock Contention** | Concurrent increments to a single row serializing behind its lock, so throughput falls as traffic on that row rises |
| **Dead-Letter Queue (DLQ)** | A holding queue for messages that have failed processing repeatedly, so they can be inspected instead of retried forever |

## Conflict Resolution

| Concept | Definition |
|---|---|
| **Conflict Resolution** | Reconciling concurrent edits to the same data into one agreed result |
| **Operational Transformation (OT)** | Transforming concurrent operations against each other so they apply in any order and converge; the approach Google Docs uses |
| **CRDT (Conflict-Free Replicated Data Type)** | A data type whose concurrent updates merge deterministically without resolution logic, typically by giving every element a unique ordered ID |
| **Tombstone** | A marker left where data was deleted, so the deletion can be ordered against concurrent operations, at the cost of storage |
| **Per-Document Leader** | Pinning every edit for one active document to a single server, because merge logic needs one point all edits pass through |

## Time-Series Data

| Concept | Definition |
|---|---|
| **Time-Series Data** | Measurements stamped with a time, written in time order and queried by range |
| **Time-Series Database** | A store partitioned by time, so writes land in the current bucket and old buckets compact or archive whole |
| **Downsampling** | Replacing fine-grained history with coarser aggregates as it ages, since old data rarely needs full resolution |
| **Retention Window** | The age at which raw points are deleted or archived, leaving only downsampled versions |
| **Batched Ingestion** | Grouping many points into one request before sending, cutting per-point overhead at high write volume |

## Design Practice

| Concept | Definition |
|---|---|
| **Design Practice** | The habits that apply to any system design, independent of the system being designed |
| **Requirements Scoping** | Stating what the system must do, which quality attributes bound it, and what is deliberately excluded, before any design follows |
| **Deep Dive** | Detailed treatment of one hard sub-problem, rather than equal shallow coverage of every component |
| **Trade-Off Articulation** | Naming what a choice costs and what was rejected, instead of presenting one option as the only one |
| **Failure Mode** | A specific way a component breaks or degrades under stress, such as a stampede, a storm, or a hotspot |
| **Cost as a Design Constraint** | Treating storage, egress, and compute spend as a factor in the design itself rather than a later concern |
