# System Design Interview Glossary

A reference of every concept, term, and named problem covered in prep, organized by category. Use this alongside `system-design-interview-prep.md`.

---

## Scale & Estimation

| Term | Definition |
|---|---|
| **Back-of-envelope estimation** | Rough, order-of-magnitude calculation of traffic/storage to justify design decisions (e.g., writes/sec × record size × time = storage). Interviewers expect you to defend these numbers against real-world reference points, not invent them. |
| **Read:write ratio** | The proportion of read to write operations (e.g., 100:1). Determines whether a system should be optimized around caching/CDN (read-heavy) or consistency/throughput on writes (write-heavy). |
| **QPS (queries per second)** | Standard throughput unit; distinguish average QPS from peak QPS (often 5-10x average). |
| **Storage growth projection** | Estimating total storage over a time horizon (e.g., 3 years) by multiplying write rate × record size × time, then adjusting for replication factor. |

---

## Identifiers & Sharding

| Term | Definition |
|---|---|
| **Snowflake ID / distributed ID generator** | A scheme for generating globally unique, roughly time-ordered 64-bit IDs across many machines without central coordination per-request. Typically split into timestamp bits + worker/machine ID bits + sequence bits. |
| **Sequence number (in an ID)** | A counter that increments within a single timestamp tick per worker, used to disambiguate multiple IDs generated in the same millisecond by the same machine. |
| **Clock skew / clock-moves-backward problem** | Risk that a machine's clock jumps backward (e.g., due to NTP correction), potentially causing a previously issued ID/timestamp to be reused. Mitigated by detecting `now < last_timestamp` and refusing to generate IDs until the clock catches up. |
| **Worker ID assignment** | The problem of giving each ID-generator instance a unique identifier automatically (not hardcoded), including reclaiming the ID when an instance crashes. Solved via a coordination service (etcd/ZooKeeper) with leases. |
| **Lease (in coordination services)** | A time-bound claim on a resource (e.g., a worker ID slot) that must be renewed via heartbeat; expires automatically if the holder crashes, freeing the resource. |
| **Compare-and-swap (CAS)** | An atomic operation that updates a value only if it currently matches an expected value — used to safely claim shared resources (like a worker ID slot) without race conditions. |
| **Base62 encoding** | Encoding a number using 62 characters (`0-9a-zA-Z`) to produce short, URL-safe strings — used to turn a large integer ID into a compact short code. |
| **Sharding** | Splitting data across multiple database instances so no single machine holds all of it. |
| **Shard key** | The field used to determine which shard a piece of data lives on (e.g., hash of short_code, hash of follower_id, geography). Should match the system's dominant query pattern to avoid cross-shard fan-out. |
| **Hash-based sharding** | Distributing records evenly across shards via a hash function on the shard key — good for uniform load distribution, bad when queries need geographic or relational locality. |
| **Consistent hashing** | A hashing scheme that minimizes data movement when shards are added/removed, compared to naive `hash % N`. |
| **Hot shard / hot key** | A single shard or key receiving disproportionate traffic (e.g., a viral short URL or video), causing load imbalance despite otherwise-even sharding. |

---

## Caching & Content Delivery

| Term | Definition |
|---|---|
| **Cache-aside pattern** | Application checks cache first; on a miss, reads from the DB and populates the cache for next time. |
| **Cache stampede / thundering herd** | Many requests simultaneously miss the cache for the same key (e.g., a viral item's TTL expires) and all hit the database at once. Mitigated with request coalescing or jittered TTLs. |
| **CDN (Content Delivery Network)** | Geographically distributed edge servers that cache and serve static/semi-static content (images, video segments, rendered pages) close to users, reducing latency and origin load. |
| **Cache invalidation** | Explicitly purging or versioning cached content when the underlying data changes (e.g., busting a CDN-cached post page on edit). |
| **301 vs. 302 redirect** | 301 = permanent (browsers cache it, reducing server load, but you lose per-click visibility and can't change the destination). 302 = temporary (less cache-friendly, but preserves the ability to track every click and change destinations) — relevant when analytics requirements exist. |
| **Adaptive bitrate streaming (HLS/DASH)** | Video delivered in small segments at multiple quality levels; the client dynamically switches resolution based on current network conditions. |

---

## Consistency & Correctness

| Term | Definition |
|---|---|
| **Eventual consistency** | A model where updates propagate asynchronously; readers may briefly see stale data, but all replicas converge eventually. Acceptable for likes/views/follower counts where exactness isn't critical. |
| **Strong consistency** | Every read reflects the most recent write immediately. Required for payments, inventory/seat holds, and authentication — the opposite default from most read-heavy systems. |
| **Read-your-writes consistency** | A guarantee that a user always sees their own recent writes immediately, even if other users might briefly see stale data (e.g., an author sees their own just-published edit right away by reading from primary). |
| **Idempotency / idempotency key** | A mechanism (typically a client-generated unique key per operation) ensuring that retrying the same request (e.g., after a timeout) doesn't cause duplicate side effects (like double-charging a card). |
| **Idempotent webhook handling** | Designing a callback handler (e.g., from a payment processor) to safely process the same event delivered more than once, by checking a unique event ID before acting. |
| **Optimistic concurrency control** | Reading a record's version, then updating conditionally on that version matching (`WHERE version = X`), retrying on conflict. Higher throughput under low contention; degrades under hot-spot contention. |
| **Pessimistic locking** | Locking a record (`SELECT ... FOR UPDATE`) before modifying it, blocking other transactions until release. Simple and correct, but limits throughput under contention. |
| **Reservation with TTL** | Placing a short-lived hold on a resource (e.g., a seat) that expires automatically if not confirmed — separates "temporarily held" from "permanently committed" state. |
| **Saga pattern** | A way to manage a multi-step transaction across independent services (e.g., reserve seat → charge card → confirm booking) without a single distributed ACID transaction, using compensating actions (like a refund) if a later step fails. |
| **Compensating action** | The "undo" step in a saga — a corrective operation (e.g., refund, release hold) executed when a later step in a multi-step transaction fails. |
| **At-least-once delivery** | A guarantee that a message will be delivered one or more times (never zero), requiring the receiver to handle possible duplicates — the common practical alternative to the much harder "exactly-once" guarantee. |
| **Client-side deduplication** | Using a unique message/event ID on the client to discard duplicates received under an at-least-once delivery guarantee. |
| **Last-write-wins (LWW)** | A conflict resolution strategy where the most recent write overwrites earlier ones — acceptable for simple counters, but breaks collaborative editing (can silently drop concurrent edits). |

---

## Fan-Out & Feed Delivery

| Term | Definition |
|---|---|
| **Fan-out on write (push model)** | Precomputing and distributing content to all relevant recipients' feeds/queues at write time (e.g., pushing a new post into every follower's feed on publish). Fast reads, but expensive for high-fan-out writers. |
| **Fan-out on read (pull model)** | Computing a feed on demand by merging content from all followed/relevant sources at read time. Avoids write storms, but costs more at read time (fan-in across shards). |
| **Celebrity problem** | The scenario where fan-out-on-write becomes prohibitively expensive because a single account has an extremely large follower count, causing a single write to trigger millions of downstream writes. |
| **Hybrid fan-out** | Using push for most accounts and switching to pull/merge-at-read-time above a follower-count threshold — the standard senior/staff-level answer to the celebrity problem. |
| **Two-stage candidate generation + ranking** | An architecture for personalized feeds/search: cheaply narrow a massive corpus to a small candidate set (fast, approximate), then apply an expensive precise ranking model only to that small set. Used in both recommendation feeds and search result ranking. |
| **Cold-start problem** | New content (or new users) has no historical engagement data, so popularity-based ranking can't yet evaluate it — addressed via deliberate exploration traffic. |
| **Exploration vs. exploitation** | The tradeoff between showing proven, high-performing content (exploitation) versus deliberately surfacing unproven/new content to gather data on its quality (exploration). |

---

## Connection State & Real-Time Delivery

| Term | Definition |
|---|---|
| **Persistent connection (WebSocket / long-lived TCP)** | A connection kept open between client and server so the server can push data without the client polling. |
| **Connection gateway** | A server layer that holds many open persistent client connections, sharded so each user's connection is pinned to one node at a time. |
| **Presence service** | Tracks which users are currently online and which gateway node holds their live connection — a dynamic routing table (`user_id → gateway_node_id`) that changes on every reconnect. |
| **Reconnection storm** | A burst of simultaneous reconnect attempts when a gateway node crashes and all its connected clients reconnect at once — requires backoff/jitter to avoid overloading the system further. |
| **Message ordering via sequence numbers** | Assigning each message a per-conversation monotonic counter (rather than relying on wall-clock time, which suffers from clock skew across servers) to guarantee consistent ordering and enable gap detection. |
| **Server-authoritative message store** | A model where the server holds the definitive, durable copy of all messages and each device syncs against it (vs. each device independently managing its own queue) — enables clean multi-device sync and read-state propagation. |
| **Multi-device sync** | Ensuring message state (read/unread, content) is consistent across a user's multiple logged-in devices. |
| **Backpressure** | Mechanisms to prevent an overwhelmed component (e.g., a reconnecting client with a huge message backlog, or a transcoding queue during upload spikes) from being flooded all at once — typically handled via pagination, incremental sync, or autoscaling. |

---

## Geospatial Systems

| Term | Definition |
|---|---|
| **Geohashing** | Encoding latitude/longitude into a string such that geographically nearby points share string prefixes, enabling efficient proximity queries and prefix-based sharding. |
| **Quadtree** | A tree data structure that recursively subdivides 2D space (denser subdivision where point density is higher) — used for efficient spatial indexing and nearest-neighbor search. |
| **Google S2 library** | A real-world library for spherical geometry / geospatial indexing, commonly used in production geospatial systems (mentioned as an alternative to geohashing/quadtrees). |
| **Ring search / radius expansion** | A matching strategy that starts searching in a small area (e.g., a geohash cell) and expands outward until enough candidates are found. |
| **Region-based sharding** | Partitioning data by geography rather than by hash, appropriate when queries are inherently local (e.g., a rider only ever matches drivers in the same city). |

---

## Rate Limiting

| Term | Definition |
|---|---|
| **Fixed window counter** | Rate-limiting by counting requests in a fixed time window (e.g., per calendar minute); simple, but allows up to 2x burst at window boundaries. |
| **Sliding window log** | Rate-limiting by storing every request's timestamp and counting how many fall within the trailing window; accurate but memory-heavy at scale. |
| **Sliding window counter** | An approximation of the sliding window log using a weighted average of the current and previous fixed windows — fixed memory footprint, good accuracy tradeoff. |
| **Token bucket** | A rate-limiting algorithm where tokens refill at a fixed rate and each request consumes a token; naturally allows controlled bursts up to the bucket size. |
| **Atomic increment (e.g., Redis INCR + Lua script)** | Performing a check-and-increment as a single atomic operation to avoid race conditions where two concurrent requests both pass a limit check before either updates the counter. |

---

## Search & Indexing

| Term | Definition |
|---|---|
| **Crawl frontier** | The queue of URLs still to be fetched by a web crawler, along with logic for prioritization and deduplication. |
| **Bloom filter** | A space-efficient probabilistic data structure for set membership testing (e.g., "have we seen this URL before?") — allows false positives but never false negatives, trading a small error rate for large memory savings. |
| **Politeness policy (crawling)** | Rate-limiting how aggressively a crawler hits any single domain, so it doesn't overwhelm smaller sites while crawling at scale. |
| **Inverted index** | The core search data structure mapping each term to the list of documents (postings) containing it, enabling fast full-text search instead of scanning every document per query. |
| **Posting list** | The list of document IDs (and often positions/frequencies) associated with a given term in an inverted index. |

---

## Counters & Async Processing

| Term | Definition |
|---|---|
| **Write amplification via row-lock contention** | The problem of many concurrent `UPDATE count = count + 1` operations on the same row serializing and slowing down under high concurrency (e.g., a viral post's like count). |
| **Async event pipeline** | Decoupling non-critical-path work (analytics, counters, search indexing, notifications) from the main request path by publishing events to a queue (e.g., Kafka) and processing them with separate consumers. |
| **Stream aggregation** | Consuming a high-volume event stream and computing rolling aggregates (e.g., view counts per minute) rather than updating a single row per event. |
| **Dead-letter queue (DLQ)** | A holding queue for messages/jobs that have repeatedly failed processing, so they can be inspected or cleaned up rather than retried forever. |

---

## Conflict Resolution (Collaborative Systems)

| Term | Definition |
|---|---|
| **Operational Transformation (OT)** | A technique for real-time collaborative editing where concurrent operations (inserts/deletes) are mathematically transformed against each other so they can be applied in any order and still converge to the same document state. Used by Google Docs. |
| **CRDT (Conflict-free Replicated Data Type)** | A data structure designed so that concurrent updates from different replicas always merge deterministically without explicit conflict resolution logic (e.g., each character has a globally unique, ordered ID). Used in systems like Figma. |
| **Tombstone** | A marker left in place of deleted data (common in CRDTs) so that deletion can be correctly merged/ordered against concurrent operations from other replicas, at the cost of extra storage overhead. |
| **Document session server / per-document leader** | Pinning all edits for a single active document to one server instance, since conflict resolution logic requires a single point through which all concurrent edits pass — the opposite sharding instinct from hashing by user ID. |

---

## Time-Series & Monitoring

| Term | Definition |
|---|---|
| **Time-series database** | A database optimized for data naturally partitioned by time, enabling efficient writes to "current" time buckets and simplified compaction/archival of old data. |
| **Downsampling / rollups** | Aggregating high-granularity historical data into coarser granularity over time (e.g., 10-sec → 1-min → 1-hour → 1-day) to control storage costs, since old data rarely needs full precision. |
| **Retention window** | The period after which raw, high-granularity data is deleted or archived, keeping only downsampled/rolled-up versions. |
| **Batched ingestion** | Client-side batching of multiple data points into a single network call before sending to the server, reducing per-point overhead at high write volume. |

---

## Named Problems / Canonical Systems Covered

| System | Representative Company | Core Bottleneck Tested |
|---|---|---|
| URL Shortener | bit.ly | ID generation, sharding, hot key |
| Blogging Platform | Medium | Social graph fan-out, read/write split |
| Short-Video Platform | TikTok | Ranking/retrieval at scale, storage + CDN cost |
| Messaging Platform | Telegram | Connection state, delivery guarantees, ordering |
| Ride-Hailing / Nearby Search | Uber | Geospatial indexing, high-churn writes |
| Distributed Rate Limiter | (generic API infra) | Concurrency correctness, tight scope |
| Web Crawler / Search Engine | Google | Parallel crawling, inverted index, freshness |
| Payment / Booking System | Ticketmaster / Stripe-like | Strong consistency, idempotency, sagas |
| Notification System | (generic, multi-channel) | Multi-channel fan-out, dedup, retries |
| Collaborative Editing | Google Docs / Figma | Conflict resolution (OT/CRDT) |
| Metrics / Monitoring Infrastructure | Datadog-style | Time-series write volume, rollups |

---

## Cross-Cutting Meta-Concepts

| Term | Definition |
|---|---|
| **Requirements scoping (functional / non-functional / out-of-scope)** | The opening phase of any system design answer: explicitly stating what the system must do, its quality attributes (latency, availability, consistency), and what's deliberately excluded from discussion. |
| **Deep dive** | A focused, detailed exploration of one specific hard sub-problem within a larger design (as opposed to giving equal shallow coverage to every component) — a key differentiator of strong answers. |
| **Tradeoff articulation** | Explicitly naming the pros/cons of a design choice and why it was selected over alternatives, rather than presenting only one option as if it were the only possibility. |
| **Failure mode** | A specific way a system component can break or degrade under stress (e.g., cache stampede, reconnection storm, shard hotspot) — naming these unprompted is expected at senior/staff level. |
| **Cost as a design constraint** | Treating infrastructure cost (storage, CDN egress, compute) as a first-class factor in design decisions, not just an afterthought — especially relevant in storage-heavy systems like video platforms. |
