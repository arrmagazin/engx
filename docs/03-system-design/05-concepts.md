---
type: Guide
title: System Design Glossary
description: Defines the system design vocabulary this chapter uses, grouped by the problem each set of terms addresses.
tags: [architecture, system-design, interview, glossary]
---

# System Design Glossary

Defines the vocabulary the rest of this chapter uses, grouped by the problem each set of terms addresses. Worked applications of these concepts are in [Canonical Systems](06-canonical-systems.md).

## Capacity Estimation

| Concept | Definition |
|---|---|
| **Capacity Estimation** | Sizing a system's traffic, storage, and bandwidth before designing it, so the design answers to numbers rather than intuition |
| **Back-of-envelope estimation** | An order-of-magnitude calculation from a few stated assumptions — writes per second times record size times retention |
| **Read:write ratio** | The proportion of reads to writes; decides whether a design optimizes for caching and delivery or for write throughput and consistency |
| **QPS (queries per second)** | The standard throughput unit, quoted separately for average and peak load because the two size different components |
| **Storage growth projection** | Total storage over a stated horizon, from write rate times record size times time, adjusted for the replication factor |

## Identifier Generation

| Concept | Definition |
|---|---|
| **Identifier Generation** | Producing unique keys for records across many machines without a central allocator on the request path |
| **Distributed ID generator** | A scheme yielding globally unique, roughly time-ordered 64-bit IDs from independent machines; typically timestamp bits, worker bits, and sequence bits |
| **Sequence number** | A counter incremented within one timestamp tick on one worker, disambiguating IDs generated in the same millisecond |
| **Clock skew** | A machine's clock jumping backward after a correction, risking reuse of an already-issued timestamp; detected by refusing to generate while `now < last_timestamp` |
| **Worker ID assignment** | Giving each generator instance a unique slot automatically rather than by hand, and reclaiming the slot when the instance dies |
| **Lease** | A time-bound claim on a resource, renewed by heartbeat and expiring on its own if the holder crashes |
| **Compare-and-swap (CAS)** | An atomic update applied only if the current value matches an expected one, used to claim a shared slot without a race |
| **Base62 encoding** | Representing a number in the 62 URL-safe alphanumeric characters, turning a large integer ID into a short code |

## Sharding

| Concept | Definition |
|---|---|
| **Sharding** | Splitting a dataset across database instances so no single machine holds all of it |
| **Shard key** | The field deciding which shard a record lives on; chosen to match the dominant query so common lookups reach one shard |
| **Hash-based sharding** | Placing records by a hash of the shard key — even load, at the cost of geographic and relational locality |
| **Consistent hashing** | A placement scheme that relocates only a small fraction of keys when instances are added or removed, unlike `hash % N` |
| **Region-based sharding** | Partitioning by geography rather than by hash, used where queries are inherently local |
| **Hot shard** | One shard or key taking disproportionate traffic, unbalancing a cluster that is otherwise evenly partitioned |

## Caching

| Concept | Definition |
|---|---|
| **Caching** | Keeping a copy of a result closer to its consumer than the system that produced it |
| **Cache-aside pattern** | The application reading the cache first and, on a miss, loading from the database and populating the cache |
| **Cache stampede** | Many requests missing the same key at once and all reaching the database together; mitigated by request coalescing or jittered expiry |
| **Cache invalidation** | Purging or versioning a cached copy when the data behind it changes |

## Content Delivery Network

| Concept | Definition |
|---|---|
| **Content Delivery Network (CDN)** | Geographically distributed edge servers holding static and semi-static content close to users, cutting latency and origin load |
| **301 vs. 302 redirect** | The choice between a permanent redirect browsers cache, which saves requests but hides per-click data, and a temporary one that reaches the server every time |
| **Adaptive bitrate streaming** | Video published as short segments at several quality levels, with the client switching level as network conditions change; HLS and DASH are the two standards in use |

## Consistency Models

| Concept | Definition |
|---|---|
| **Consistency Model** | The guarantee a system gives about when a write becomes visible to a subsequent read |
| **Eventual consistency** | Updates propagating asynchronously, so replicas may serve stale data briefly but converge |
| **Strong consistency** | Every read reflecting the most recent write, required wherever a stale answer is a correctness bug rather than a cosmetic one |
| **Read-your-writes consistency** | A guarantee that a user sees their own recent writes immediately, even while other users may not |
| **Last-write-wins (LWW)** | Resolving concurrent writes by keeping the most recent — adequate for counters, lossy for collaborative editing |

## Idempotency

| Concept | Definition |
|---|---|
| **Idempotency** | The property that applying an operation more than once has the same effect as applying it once |
| **Idempotency key** | A client-generated unique value per operation, letting the server recognize a retry instead of repeating the side effect |
| **Idempotent webhook handling** | A callback handler that checks a unique event ID before acting, so a redelivered event takes effect once |
| **At-least-once delivery** | A guarantee that a message arrives one or more times but never zero, leaving duplicate handling to the receiver |
| **Client-side deduplication** | Discarding repeats by message ID on the receiving side, the standard counterpart to at-least-once delivery |

## Concurrency Control

| Concept | Definition |
|---|---|
| **Concurrency Control** | Keeping simultaneous writers from corrupting shared state |
| **Optimistic concurrency control** | Reading a version, updating only if it still matches, and retrying on conflict; higher throughput until contention concentrates on one record |
| **Pessimistic locking** | Taking a lock before modifying a record and blocking other writers until release; simple and correct, but throughput-limiting |
| **Reservation with TTL** | A short-lived hold that expires unless confirmed, separating temporarily held state from committed state |

## Distributed Transactions

| Concept | Definition |
|---|---|
| **Distributed Transaction** | A single logical operation spanning services that share no database and therefore no commit |
| **Saga pattern** | Running that operation as an ordered series of local transactions, each with an undo step for when a later one fails |
| **Compensating action** | The undo step in a saga — a refund, a released hold, a cancelled reservation |

## Fan-Out

| Concept | Definition |
|---|---|
| **Fan-Out** | The multiplication of one write into many downstream writes or reads, one per recipient |
| **Fan-out on write** | Pushing content into every recipient's feed at publish time; fast reads, expensive for accounts with many followers |
| **Fan-out on read** | Merging content from followed sources when a feed is requested; cheap writes, costly reads across shards |
| **Celebrity problem** | One account with a very large follower count making write-time fan-out prohibitive, since a single post triggers millions of writes |
| **Hybrid fan-out** | Pushing for ordinary accounts and merging at read time above a follower threshold |

## Feed Ranking

| Concept | Definition |
|---|---|
| **Feed Ranking** | Ordering candidate items for one user by predicted relevance rather than by recency alone |
| **Two-stage candidate generation** | Narrowing a large corpus cheaply and approximately, then scoring only the survivors with an expensive model |
| **Cold-start problem** | New items or users having no engagement history, so popularity-based ranking cannot yet place them |
| **Exploration vs. exploitation** | The trade-off between serving proven content and deliberately serving unproven content to learn its quality |

## Real-Time Delivery

| Concept | Definition |
|---|---|
| **Real-Time Delivery** | Pushing data to a client as it happens, rather than waiting for the client to ask |
| **Persistent connection** | A connection held open between client and server so the server can send without being polled |
| **Connection gateway** | A layer holding many open client connections, sharded so each user is pinned to one node |
| **Presence service** | The mapping from user to the gateway node currently holding their connection, rewritten on every reconnect |
| **Reconnection storm** | Every client of a failed gateway reconnecting at once, requiring backoff and jitter to avoid toppling the replacement |
| **Message ordering via sequence numbers** | A per-conversation monotonic counter that fixes order and exposes gaps, avoiding reliance on clocks that differ across servers |
| **Server-authoritative message store** | The server holding the definitive durable copy that every device syncs against, rather than each device managing its own queue |
| **Multi-device sync** | Keeping message content and read state consistent across one user's logged-in devices |
| **Backpressure** | Limiting how fast work is handed to a component that cannot keep up, through pagination, incremental sync, or queueing |

## Geospatial Indexing

| Concept | Definition |
|---|---|
| **Geospatial Indexing** | Organizing points on the earth's surface so nearby ones can be found without scanning all of them |
| **Geohashing** | Encoding latitude and longitude into a string whose shared prefixes mean physical proximity, which also makes it usable as a shard key |
| **Quadtree** | A tree that recursively subdivides two-dimensional space, subdividing further where points are dense |
| **Google S2 library** | A production library for spherical geometry and cell-based indexing, used where a rectangular grid distorts |
| **Ring search** | Querying a small area first and widening it until enough candidates are found |

## Rate Limiting

| Concept | Definition |
|---|---|
| **Rate Limiting** | Capping how many requests a caller may make in a period, to protect capacity and enforce quotas |
| **Fixed window counter** | Counting requests per calendar window; simple, but permits a double-rate burst across a window boundary |
| **Sliding window log** | Storing each request's timestamp and counting those inside the trailing window; exact, but memory-heavy |
| **Sliding window counter** | Approximating the log by weighting the current and previous fixed windows, at constant memory |
| **Token bucket** | Tokens accruing at a fixed rate and one being spent per request, permitting bursts up to the bucket size |
| **Atomic increment** | Checking and incrementing a counter in one indivisible step, such as Redis `INCR` inside a Lua script, so two concurrent requests cannot both pass the same limit |

## Search Indexing

| Concept | Definition |
|---|---|
| **Search Indexing** | Precomputing a structure that answers queries by term, instead of scanning every document per query |
| **Inverted index** | The mapping from each term to the documents containing it |
| **Posting list** | The document IDs recorded against one term in an inverted index, often with positions and frequencies |
| **Crawl frontier** | The queue of URLs a crawler has yet to fetch, with its prioritization and deduplication rules |
| **Politeness policy** | A per-domain rate limit that keeps a crawler from overwhelming any one site |
| **Bloom filter** | A compact probabilistic membership test that can report a false positive but never a false negative |

## Asynchronous Processing

| Concept | Definition |
|---|---|
| **Asynchronous Processing** | Moving work off the request path so a caller is not made to wait for it |
| **Async event pipeline** | Publishing events to a queue and handling them in separate consumers, keeping analytics, counters, and indexing off the hot path |
| **Stream aggregation** | Computing rolling aggregates from an event stream rather than updating one row per event |
| **Write amplification via row-lock contention** | Concurrent increments to a single row serializing behind its lock, so throughput falls as traffic on that row rises |
| **Dead-letter queue (DLQ)** | A holding queue for messages that have failed processing repeatedly, so they can be inspected instead of retried forever |

## Conflict Resolution

| Concept | Definition |
|---|---|
| **Conflict Resolution** | Reconciling concurrent edits to the same data into one agreed result |
| **Operational transformation (OT)** | Transforming concurrent operations against each other so they apply in any order and converge; the approach Google Docs uses |
| **CRDT (conflict-free replicated data type)** | A data type whose concurrent updates merge deterministically without resolution logic, typically by giving every element a unique ordered ID |
| **Tombstone** | A marker left where data was deleted, so the deletion can be ordered against concurrent operations, at the cost of storage |
| **Per-document leader** | Pinning every edit for one active document to a single server, because merge logic needs one point all edits pass through |

## Time-Series Data

| Concept | Definition |
|---|---|
| **Time-Series Data** | Measurements stamped with a time, written in time order and queried by range |
| **Time-series database** | A store partitioned by time, so writes land in the current bucket and old buckets compact or archive whole |
| **Downsampling** | Replacing fine-grained history with coarser aggregates as it ages, since old data rarely needs full resolution |
| **Retention window** | The age at which raw points are deleted or archived, leaving only downsampled versions |
| **Batched ingestion** | Grouping many points into one request before sending, cutting per-point overhead at high write volume |

## Design Practice

| Concept | Definition |
|---|---|
| **Design Practice** | The habits that apply to any system design, independent of the system being designed |
| **Requirements scoping** | Stating what the system must do, which quality attributes bound it, and what is deliberately excluded, before any design follows |
| **Deep dive** | Detailed treatment of one hard sub-problem, rather than equal shallow coverage of every component |
| **Trade-off articulation** | Naming what a choice costs and what was rejected, instead of presenting one option as the only one |
| **Failure mode** | A specific way a component breaks or degrades under stress, such as a stampede, a storm, or a hotspot |
| **Cost as a design constraint** | Treating storage, egress, and compute spend as a factor in the design itself rather than a later concern |
