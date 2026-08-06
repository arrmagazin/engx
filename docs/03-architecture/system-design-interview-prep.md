# System Design Interview Prep (Senior / Staff)

A comprehensive reference covering 10 canonical system design problems, organized by the *core bottleneck* each one tests. Built for a senior/staff-level interview loop.

---

## How to Use This Document

At senior/staff level, interviewers care less about "do you know the buzzwords" and more about:

1. **Justified assumptions** — every number (scale, storage, ratios) should be defensible, not pulled from thin air.
2. **Generating options before picking one** — for any key decision, name 2-3 alternatives and explain the tradeoff, don't just state your first idea.
3. **Recognizing the *actual* hard problem** — different systems have fundamentally different bottlenecks (write-heavy vs. read-heavy, strong vs. eventual consistency, connection-state vs. stateless). Reflexively reapplying the same pattern to every problem is a mid-level tell.
4. **Naming failure modes and cross-cutting concerns unprompted** — cache stampedes, hot shards, clock skew, idempotency, moderation, cost.

### The Standard Framework (apply to any problem)

1. **Requirements** — functional + non-functional, explicitly state what's out of scope.
2. **Scale estimates** — traffic (reads/writes per sec), storage growth, and what ratio (read:write) dominates. Sanity-check against real-world reference points.
3. **High-level architecture** — draw the boxes: clients, load balancer, services, cache, DB, async pipeline.
4. **Data model & sharding** — what's the shard key, and why does it match the dominant query pattern?
5. **Deep dives** — 2-4 of the *actually hard* parts (not everything deserves equal depth).
6. **Cross-cutting concerns** — failure modes, caching, consistency tradeoffs, cost — named without being asked.

### Summary Table — 10 Systems, 10 Bottleneck Shapes

| System | Core Bottleneck |
|---|---|
| URL Shortener | ID generation, sharding, hot key |
| Blogging Platform | Social graph fan-out, read/write split |
| Short-Video Platform (TikTok) | Ranking/retrieval at scale, storage+CDN cost |
| Messaging (Telegram) | Connection state, delivery guarantees, ordering |
| Ride-hailing (Uber) | Geospatial indexing, high-churn writes |
| Rate Limiter | Concurrency correctness, tight scope |
| Web Crawler / Search | Parallel crawl, inverted index, freshness |
| Payments / Ticketing | Strong consistency, idempotency, sagas |
| Notification System | Multi-channel fan-out, dedup, retries |
| Collaborative Editing (Docs/Figma) | Conflict resolution (OT/CRDT) |
| Metrics / Monitoring | Time-series write volume, rollups |

---

## 1. URL Shortener (bit.ly)

### Requirements
- Optional auth: anonymous users can shorten URLs; authenticated users can manage (view/edit/delete) their links.
- Click analytics (total clicks, timestamps).
- Short URLs are **immutable** once created (no editing destination) — avoids a whole class of caching/consistency headaches.
- Custom aliases supported.

### Scale (defend, don't guess)
- Assume a *popular, successful* service — not the biggest site on the internet.
- **~1,000 writes/sec** (a few hundred million new URLs/day is already huge).
- **~10,000-100,000 reads/sec** (redirects are typically 10-100x more frequent than creates).
- Per-record size: short_code + long_url (use a realistic average, ~50-100 bytes, not the 1024-byte max) + user_id + timestamps ≈ ~200-300 bytes realistic, or ~1.1KB if using max-length assumptions.
- Over 3 years at 1,000 writes/sec ≈ 94.6B records → tens to ~100TB raw (×3 for replication).
- **Conclusion: needs sharding.**

### ID Generation — Snowflake-style distributed ID generator
- **Bit layout**: 42 bits timestamp (ms, ~139 years range) + 8 bits worker ID (256 workers) + 14 bits sequence (16,384 IDs/worker/ms). Massive headroom at 1,000 writes/sec.
- **Clock-moves-backward problem**: if `current_time < last_timestamp` (NTP correction), refuse to generate IDs until clock catches up — never silently reuse a timestamp.
- **Worker ID assignment**: don't hardcode in config (doesn't scale, error-prone, breaks on restart). Use **etcd/ZooKeeper**: each worker acquires a lease on a free slot via atomic compare-and-swap, heartbeats to keep it alive; crash → lease expires → slot reclaimed. Tradeoff: adds a startup-time dependency; if etcd is briefly down, new workers can't start (existing ones keep running).
- **Encoding**: Base62 encode the 64-bit ID (`[0-9a-zA-Z]`). ~6-7 chars covers tens of billions to trillions of combinations. XOR/shuffle bits so codes don't look sequential (prevents scraping/enumeration, hides volume from competitors).
- **Custom aliases**: separate path — user-supplied string, uniqueness checked via DB (Bloom filter in front to fail fast on "already taken").

### Sharding
- **Shard key: hash of `short_code`** (not user_id) — redirects are the dominant query and already have the short_code in hand. Even distribution, O(1) routing, no fan-out.
- Downside: "all links by user X" needs a secondary index/lookup table (acceptable — rarer, lower-QPS query).

### Read Path (hot path)
1. LB → stateless routing service.
2. Cache first (Redis, keyed by short_code) — popular links follow a power law, high hit rate expected.
3. Miss → hash(short_code) → correct shard → DB → populate cache → redirect.
4. **301 vs 302**: 301 (permanent) is more cache-friendly but loses per-click analytics and can't update destination. **302 is correct here** given the analytics requirement — explicit tradeoff to state.

### Write Path
1. App server calls ID generator (or validates custom alias).
2. Write to shard by hash(short_code).
3. Async event to analytics pipeline.

### Analytics
- Never write click events synchronously to primary DB (would make the hot read path also a hot write path).
- Async: publish lightweight event (short_code, timestamp, rough geo/UA) to Kafka → consumer aggregates into a time-series store.

### Failure Modes
- **Cache stampede** on a viral link — mitigate with request coalescing or jittered TTL.
- **Shard hotspot** on a viral short_code — cache absorbs most of this.
- **etcd/coordination outage** — existing workers unaffected, but can't scale up during outage.

---

## 2. Blogging Platform (Medium)

### Requirements
- Authors write/edit/publish/delete posts; readers browse/read/search/comment/clap.
- Follow authors; personalized (simple reverse-chronological) feed.
- Out of scope: paywall, real-time collaborative editing, ML ranking.

### Scale
- 50M registered users, 5M DAU.
- 1M posts published/day ≈ **12 writes/sec** average.
- 100M reads/day ≈ **~1,150 reads/sec** average, 5,000-10,000/sec peak.
- **Read:write ≈ 100:1** — read-optimized system, heavy caching/CDN justified.
- Storage: text is trivial (~3.65TB/year); **images dominate** (~220TB/year) — bottleneck is blob storage/CDN egress, not the relational data.

### Architecture
```
Client → CDN (static assets, cached public post pages)
       → API Gateway/LB
           → Post Service / User-Auth Service / Feed Service / Comment Service / Search Service
               → Cache (Redis)
               → Primary DB(s) (sharded)
       → Async pipeline (Kafka) → Feed fan-out workers, Search indexer (Elasticsearch), Clap aggregator
Blob storage (S3) → post images, served via CDN
```

### Data Model
- `posts(post_id PK, author_id, title, body-or-blob-pointer, status, created_at, updated_at, tags[])`
- `users`, `follows(follower_id, followee_id)`, `comments`, `claps`
- Shard `posts` by `post_id`; shard `follows` by `follower_id` (matches "who does X follow" feed-generation query).

### Deep Dive: Post Content Storage & Editing
- Split **metadata row** (small, frequently queried) from **body content** (blob storage) — keeps list/feed queries fast.
- Storing each edit as a new blob + pointer gives edit history nearly for free.
- **Read-your-writes**: author's own subsequent reads route to primary (or always read post content from primary, cache only for other readers).

### Deep Dive: Feed Fan-Out (the classic tradeoff)
- **Fan-out on write (push)**: precompute each follower's feed on publish. Great read latency; breaks down for authors with huge follower counts ("celebrity problem" — millions of writes for one post).
- **Fan-out on read (pull)**: compute feed on demand by merging followed authors' recent posts. No celebrity-write-storm, but higher read latency (fan-in across shards).
- **Optimal: hybrid** — push for normal accounts, pull/merge-at-read-time for accounts above a follower threshold (e.g., 100K+). This is the expected senior/staff answer.

### Deep Dive: Claps/Likes Counter
- Naive `UPDATE ... claps = claps + 1` causes row-lock contention on popular posts.
- Use an in-memory counting service with periodic batched flushes, or route increments through Kafka + aggregate consumer. Eventual consistency on exact count is acceptable — trade strict consistency for throughput.

### Deep Dive: Search
- Don't search the primary DB. Publish create/update events → Kafka → index into Elasticsearch. Queries hit ES.

### Caching & CDN
- CDN for images + fully-rendered public post pages (biggest lever given 100:1 read ratio).
- Redis for session/feed caches, hot metadata, clap counts.
- Cache invalidation: bust CDN cache on publish/update (versioned URLs or explicit purge).

### Cross-Cutting
- Celebrity fan-out storm (addressed above).
- Hot/viral post — cache absorbs spikes; rate-limit abusive comment/clap traffic.
- Multi-region: reads from local replicas/edge; writes go to a home region per user — cross-region write consistency explicitly punted unless pushed further.
- Async moderation pipeline for spam/abuse, doesn't block the write path.

---

## 3. Short-Video Platform (TikTok)

### Requirements
- Upload short videos (record/upload, caption/hashtags/music).
- Personalized, algorithmically-ranked infinite feed ("For You" page) — the defining feature.
- Like/comment/share/follow; instant playback on scroll across variable network conditions.
- Out of scope: the ML ranking model itself (treated as black-box), live-streaming, DMs.

### Scale
- 100M DAU, ~30 videos/session, ~2 sessions/day → 6B views/day ≈ **~70,000 views/sec average**, 300-500K/sec peak.
- Uploads: 1% of DAU/day → 1M uploads/day ≈ **~12 writes/sec average** — view:upload ratio can reach millions:1.
- Each upload needs multiple resolutions/bitrates (5-6 renditions) for adaptive streaming.
- Storage: ~150TB/day → **~55PB/year**. Bottleneck is storage + transcoding + CDN egress, not metadata DB.

### Architecture
```
Upload: Client → Upload API → Object storage (raw video)
                              → Transcoding pipeline (async, queue-driven)
                                  → Multi-resolution renditions → CDN origin
                                  → Metadata DB + Search/Tag index
                                  → Feed/ranking candidate pool

Watch: Client → CDN (video segments, cache-fill on miss)
              → Feed Service → Ranking Service (ML) → candidate video IDs
              → Metadata cache (Redis)
```

### Deep Dive: Upload & Transcoding Pipeline
1. Upload service writes raw file to object storage, creates `pending` metadata row, returns immediately.
2. Event to Kafka → transcoding workers: multi-resolution transcode (HLS/DASH segments), thumbnails, audio fingerprint, content moderation (automated + human-review flagging).
3. On completion: metadata → `published`, push to CDN origin, enter ranking candidate pool.
- **Tradeoff**: transcoding is slow/CPU-heavy → async with a "processing" state. Creator sees their own video immediately (read-your-writes for creator via direct/primary read); invisible to others until transcoding + moderation complete.

### Deep Dive: Watch/Feed Path (the hard problem here)
- Fundamentally different from social fan-out — content is algorithmically selected from the entire corpus, not from followed accounts.
- **Two-stage architecture**:
  1. **Candidate generation**: cheaply narrow billions of videos to hundreds/thousands of plausible candidates (collaborative filtering, embedding-similarity, recent-popular-in-category). Fast and approximate.
  2. **Ranking**: heavier ML model scores only the pre-filtered candidates precisely. Never rank the entire corpus per request.
- **Prefetching, not on-scroll computation**: client requests a batch (10-20 videos) ahead of time and prefetches actual video data — the single most important decision for instant first-frame playback.
- **Freshness vs. cost**: fully real-time ranking per-scroll is expensive; compute candidate pool/ranking periodically or per-session, blend in real-time signals cheaply. Explicit tradeoff of personalization freshness vs. cost.

### Deep Dive: Video Delivery (CDN)
- Every rendition lives in CDN-fronted storage; first regional request fills cache, subsequent ones hit edge.
- Adaptive bitrate streaming (HLS/DASH): client fetches small segments at resolution matched to network conditions.
- **Long-tail**: viral videos cache extremely well; **cold-start problem** for brand-new videos with no history — deliberately route some traffic to unproven content (exploration vs. exploitation).

### Deep Dive: Counters at Extreme Scale
- Never synchronous DB increments per view. Publish view/like events to Kafka, aggregate in a stream processor, flush deltas periodically.
- View counts shown to users can be eventually consistent/approximate — stale-by-seconds is fine, buys enormous throughput headroom.

### Cross-Cutting
- Content moderation must complete before public candidate-pool entry.
- Multi-region storage placement — cache/pre-warm near where content is popular, informed by early ranking signals.
- **Cost is a first-class constraint** — storage + transcoding + CDN egress dominate cost; decisions like downsampling/evicting cold long-tail high-res renditions over time are legitimate discussion points.
- Backpressure on transcoding queue during upload spikes — autoscale workers, prioritize by account tier if needed.

**Key contrast to name explicitly**: the blog's hard problem was social-graph fan-out; this system's hard problem is ranking+retrieval from an undifferentiated corpus plus the physical cost of storing/serving video.

---

## 4. Messaging Platform (Telegram)

### Requirements
- 1:1 and group messaging (text/media/files); near-real-time delivery when online, queued when offline.
- Delivery/read receipts, typing indicators, presence.
- Multi-device sync; large broadcast channels (millions of subscribers, one-way).
- Out of scope: E2E key-exchange details, voice/video calls, bot API.

### Scale
- 500M MAU, ~50M concurrently connected at peak — **concurrent connections matter more here than daily totals.**
- 100M DAU × 20 msgs/day ≈ **~23,000 messages/sec average**, higher at peak.
- Small text messages (~200 bytes); media split into separate blob storage (same pattern as video platform).
- **This is a latency/connection-management problem, not a storage problem** — the key framing difference from the content platforms above.

### Architecture
```
Client (persistent WS/TCP) → Connection Gateway (sharded by user)
                            → Presence Service (user_id → gateway_node mapping)
                            → Message Service → Message Store (durable, per-conversation)
                                              → Delivery/Routing (push to recipient's gateway, or queue if offline)
                                              → Push Notification Service (APNs/FCM) for offline delivery
Media storage (blob + CDN) — same pattern as video platform
```

### Deep Dive: Connection Management (the defining problem)
- Persistent connections (WebSocket/custom TCP) so server can push without polling.
- **Presence/routing table** (Redis): `user_id → gateway_node_id` — dynamic, changes on every reconnect (harder than the URL shortener's static shard routing).
- Capacity: ~50-100K connections/gateway node → 50M concurrent / 100K ≈ ~500 gateway nodes.
- **Reconnection storm**: gateway crash → all its clients reconnect simultaneously — needs backoff/jitter on client reconnect logic.

### Deep Dive: Message Delivery & Ordering
1. Sender's client → connected gateway → Message Service.
2. **Persist durably first** (write-ahead), before attempting delivery — durability must not depend on recipient being online.
3. **Online** recipient → route directly to their gateway, push. **Offline** → durable per-user queue + push notification (APNs/FCM) to wake the app; full message delivered on reconnect/sync.
4. Sender's ack = "persisted," not "delivered" — decouple these; layer delivery/read receipts as separate state transitions.
- **Ordering**: per-conversation monotonic sequence number (not wall-clock — clock skew across servers is unreliable). Enables gap detection and idempotent resumption ("give me everything after sequence #4521").

### Deep Dive: Multi-Device Sync
- **Server-authoritative message store** (Telegram's actual model): messages live durably on the server indefinitely; each device is a view syncing via sequence numbers. Read state is server-side → propagates to all devices trivially.
- Alternative (early WhatsApp-style): each device independently fetches/deletes from a queue — simpler but read-state sync across devices is awkward, history is lost without separate backup.
- Given multi-device history requirement, **server-authoritative is the right call** — contrast with the video platform, which has no "device sync" concept.

### Deep Dive: Group Chats & Channels (fan-out again, different shape)
- **Small groups**: fan-out-on-write is fine — push to every online member's gateway, enqueue for offline.
- **Large broadcast channels**: fan-out-on-write to millions of queues per post is the same celebrity problem as the blog feed — instead, store the channel post once; subscribers pull/sync new posts on connect/poll rather than the server pushing individually. Same push-vs-pull tradeoff as the blog feed, applied to chat — worth explicitly drawing the parallel.

### Cross-Cutting
- **At-least-once delivery + client-side dedup** (via message IDs) rather than trying to guarantee exactly-once end-to-end (much harder, rarely worth it).
- **Typing indicators/presence**: high-frequency, low-value, loss-tolerant — best-effort path, not durably persisted. Contrast with actual messages, which must be durable — explicitly separating "must be durable" vs. "best-effort ok" data is a strong signal.
- **Backpressure for offline users with huge backlogs**: paginate/sync incrementally by sequence number, don't push a giant blob on reconnect.
- Security: message content encrypted in transit and ideally at rest (full E2E design out of scope but worth a one-line mention).

**Key contrast to name explicitly**: the blog/video platforms were dominated by read-scale and content-distribution problems (cache/CDN everything). This one is dominated by connection state and delivery guarantees — knowing *where* a user's live connection is, and guaranteeing exactly-once-in-order delivery across crashes/reconnects.

---

## 5. Ride-Hailing / Geospatial (Uber, Nearby Search)

### Requirements
- Riders request rides; matched to nearby available drivers.
- Drivers continuously broadcast location (every few seconds) while online.
- Dynamic/surge pricing based on local supply/demand.

### Scale
- 5M concurrent drivers broadcasting every ~4 sec → **~1.25M location writes/sec** — the defining number. Write-heavy, high-churn, unlike prior content-centric systems.
- Ride requests comparatively rare (thousands/sec).

### New Bottleneck: Proximity Queries at Scale
- Naive `WHERE distance(lat,lng) < 5km` row-scans don't work — need spatial indexing.
- **Geohashing**: encode lat/lng so prefix similarity implies proximity; shard/index by geohash prefix, query neighboring cells.
- Alternatives: **quadtree** (recursive spatial subdivision, denser where driver density is higher), or **Google S2 library** (common in real systems).
- Driver locations live in an **in-memory store** (Redis geospatial commands or custom in-memory quadtree service) — too high-churn/low-value-per-write to persist durably at full fidelity; losing a few seconds on crash is fine.

### Deep Dive: Matching
- On ride request: compute rider's geohash cell, expand outward (ring search) until enough candidates found, rank by ETA (road network, not straight-line distance), send to top candidate, timeout-and-retry to next on decline.
- **Write vs. read tradeoff**: update spatial index on every ping (fresh but expensive) vs. batch every N seconds (cheaper, staler) — a few seconds of staleness is typically tolerable, worth stating explicitly.

### Cross-Cutting
- **Region-based sharding** (not hash-based) — a Tokyo driver never matches a Chicago rider, so partition by geography. Sharding strategy should follow the query pattern, and here the pattern is inherently local.

---

## 6. Distributed Rate Limiter

### Requirements
- Limit requests per user/API-key to N per time window (e.g., 100/min), correctly across many stateless API servers.

### New Bottleneck: Correctness Under Concurrency, Not Scale
Intentionally a smaller, tighter problem used to test precise reasoning.

### Algorithms (name 3, defend one)
- **Fixed window counter**: simplest, but allows up to 2x burst at window boundaries.
- **Sliding window log**: store every request timestamp, count trailing window — accurate but memory-heavy at scale.
- **Sliding window counter** (weighted average of current + previous fixed window): good approximation with fixed memory — usually the pragmatic default choice.
- **Token bucket**: tokens refill at a fixed rate, request consumes one — naturally allows controlled bursts, popular in practice (e.g., AWS API limits).

### Deep Dive: Distributed State
- Shared counters across API servers → **centralized Redis** (atomic `INCR`+`EXPIRE`, or Lua script for atomicity across check-and-increment).
- **Race condition to flag**: naive "read count, check limit, increment" across two simultaneous requests on different servers can both pass the check before either increments — fix with an atomic single round-trip operation (Lua script or `INCR` returning new value), not separate GET+SET.
- Redis becomes a bottleneck/SPOF at extreme scale — mitigate with Redis Cluster (sharded by key), or accept slightly relaxed accuracy via local in-memory counters synced periodically (accurate global limiting vs. eventually-consistent but more scalable — a real tradeoff).

---

## 7. Web Crawler / Search Engine

### Requirements
- Crawl the web, discover new pages via links, avoid excessive re-crawling of unchanged pages.
- Build a searchable index; serve ranked results in <200ms.

### New Bottleneck: Massive Parallel Crawling + Freshness/Completeness Tradeoff

### Crawler Architecture
- **Frontier (URL queue)**: seed → fetch → extract links → dedupe (Bloom filter — false positives ok, false negatives not, memory-efficient at billions of URLs) → new URLs back to frontier.
- **Politeness**: partition frontier by domain, enforce per-domain rate limits/crawl-delay so one large/slow site doesn't starve the crawl of others.
- **Priority**: assign re-crawl frequency based on historical change frequency + page importance (rough PageRank-like signal) — not all pages deserve equal attention.
- Distributed crawl workers coordinated via the frontier queue (Kafka-like), each fetches/parses/extracts outlinks, pushes new URLs and content downstream.

### Deep Dive: Indexing
- Parsed content → **inverted index** (term → doc IDs containing it), sharded by term or doc range depending on query pattern.
- Typically built/updated in large batches, not real-time per page — "how quickly must a new page become searchable" is a legitimate scoping question.

### Deep Dive: Query Serving
- Query → tokenize → look up posting lists (sharded, fan-out + merge) → rank candidates (same two-stage "narrow then rank" pattern as the TikTok feed) → return top-K.

---

## 8. Payment / Booking System (Ticketmaster-style)

### Requirements
- Book a seat/ticket or make a payment; never oversell the same seat or double-charge.
- Integrate reliably with external payment processors (Stripe-like).

### The Big Mindset Shift
Every prior system leaned on "eventual consistency is fine, cache aggressively, approximate counts ok." **Here that's mostly wrong** — correctness (no double-booking, no double-charge, no lost money) matters more than latency or throughput. State this contrast explicitly in the interview — it signals you're not pattern-matching a template.

### Deep Dive: Preventing Overselling
- **Pessimistic locking** (`SELECT ... FOR UPDATE`): simple and correct, but limits throughput under contention (many buyers, one popular seat).
- **Optimistic concurrency**: read version, `UPDATE ... WHERE version = X`, retry on conflict — better throughput at low contention, degrades under hot-spot scenarios (e.g., everyone wants front-row seats).
- **Reservation with TTL**: "add to cart" places a short-lived hold (e.g., 10 min; status=reserved, expires_at set); finalize to "sold" only on successful payment; background job releases expired holds. This is the realistic answer — explicitly separates "temporarily held" from "confirmed."

### Deep Dive: Idempotency & Exactly-Once Payment
- Client generates an **idempotency key** per checkout attempt; server dedupes on it — a client retry after a network timeout (charge may have actually succeeded server-side) doesn't double-charge. Standard, expected answer — know it cold.
- **Saga pattern** for the multi-step transaction (reserve seat → charge card → confirm booking → send ticket): if a later step fails, need a compensating action (refund), not a single ACID transaction spanning an external, uncontrollable payment processor. Name this explicitly.
- **Idempotent webhook handling**: payment processor's async callback can be delivered more than once — handler must check-then-act on a unique payment/event ID.

### Cross-Cutting
- **Database is the source of truth, not cache** — for anything involving money or inventory, read the primary (or synchronously-replicated replica), accepting latency cost for correctness. This is the opposite instinct from the read-heavy platforms above.

---

## 9. Notification System

### Requirements
- Send notifications (push/email/SMS) triggered by events (e.g., "someone liked your post," "order shipped").
- User preferences (channel choice, opt-outs, quiet hours); avoid spamming via batching/digesting.

### New Bottleneck: Reliable Multi-Channel Fan-Out With Dedup, Not Raw Scale

### Architecture
```
Event source (app services) → Event queue (Kafka)
  → Notification Service (checks prefs, dedups, batches)
    → Channel dispatchers (Push/SMS/Email workers)
      → 3rd-party providers (APNs/FCM, Twilio, SendGrid)
```

### Deep Dives
- **Preference/dedup layer**: check user's channel preferences and whether a similar notification was recently sent (e.g., batch "5 people liked your post" into one push instead of 5) — this batching/digesting logic is the actual product-differentiating complexity.
- **Retry with backoff per provider** + **dead-letter queue** for repeatedly-failing sends (e.g., invalid device token) — flag for cleanup rather than retrying forever.
- **Rate limiting outbound per user** — cap/drop/digest to prevent a bug or abuse from sending hundreds of pushes to one person.
- **Priority tiers**: security alerts should preempt marketing notifications — priority queue, not pure FIFO.

---

## 10. Collaborative Editing (Google Docs / Figma)

### Requirements
- Multiple users edit the same document simultaneously; all see each other's changes near-real-time, converging to the same final state.

### New Bottleneck: Conflict Resolution — a Genuinely Different Consistency Model
The one place where "eventual consistency, last-write-wins" actually breaks the product: naive LWW on simultaneous edits at the same position would silently drop one person's text.

### The Two Real Approaches (name both, pick one)
- **Operational Transformation (OT)**: each edit is an operation (insert/delete at position X); concurrent operations are transformed against each other so they can apply in any order and converge to the same result. What Google Docs actually uses — complex, many subtle edge cases, but well-proven.
- **CRDTs**: structure the document as a data type mathematically guaranteed to converge regardless of operation order (e.g., each character has a unique ordered ID; inserts/deletes are commutative). Simpler correctness guarantees than OT, some memory overhead (tombstones for deletions). Figma uses a CRDT-like approach.

### Architecture
- Persistent connection per active editor (same connection-management problem as Telegram) to a **document session server** holding authoritative in-memory state while the doc is active.
- All edits flow through that session server, which applies OT/CRDT merge logic and broadcasts the resulting operation to other connected clients.
- Periodic **snapshotting** to durable storage (don't replay the entire edit history from scratch on open) plus the full operation log for undo/version history.

### Cross-Cutting
- **Sharding is per-document, not per-user** — pin each active document to one session server (a "leader" for that doc) since all edits must go through one place to resolve conflicts. The opposite instinct from hash-sharding by user ID everywhere else.

---

## 11. Metrics / Monitoring Infrastructure (Datadog-style)

### Requirements
- Ingest metrics from millions of hosts/services (CPU, latency, custom counters) at high frequency.
- Support dashboards and alerting over arbitrary time ranges.

### New Bottleneck: Extremely High-Volume Time-Series Writes + Downsampling
- 1M hosts × 100 metrics × 1 sample/10sec ≈ **~10M writes/sec** — write volume dwarfs even the video platform's read volume, but in small, structured, append-only records rather than large blobs.

### Deep Dives
- **Time-series database**, not general RDBMS — data naturally partitions by time (write to the "current" bucket, rarely touch old ones), enabling simple, efficient sharding/compaction unlike general OLTP data.
- **Downsampling/rollups**: raw 10-sec granularity isn't needed/affordable forever — background jobs aggregate old data into coarser granularity (1-min → 1-hour → 1-day), archiving/deleting raw data after a retention window. Frame explicitly: recent data is precise and expensive, old data is coarse and cheap — dashboards/alerting UX must be designed around this (can't zoom into 10-sec granularity on 8-month-old data).
- **Write path optimized for append-only, batched ingestion** — client-side batching before sending, bulk server writes rather than per-metric inserts.
- **Alerting** runs as a separate consumer on the same ingest stream in near-real-time (can't wait for rollups) — evaluates threshold rules per incoming point/window, fires alerts async, decoupled from the storage write path so a slow rule never blocks ingestion.

---

## Cross-System Patterns Worth Recognizing

These recur across multiple problems above — naming the pattern by name (and why it does/doesn't apply) is a strong senior/staff signal:

- **Fan-out on write vs. read** (blog feed, messaging channels): push is fast to read but breaks on high-fan-out ("celebrity problem"); pull avoids that but costs read latency. Hybrid with a threshold is usually the right answer.
- **Two-stage narrow-then-rank** (TikTok feed, search query serving): never run an expensive operation over the full corpus — cheaply filter to a candidate set first, then rank precisely.
- **Async event pipeline for anything non-critical-path** (analytics, counters, search indexing, moderation): keep the hot path (redirect, read, ingest) free of slow/best-effort work; decouple via Kafka + consumers.
- **Sharding should follow the dominant query pattern, not be applied uniformly**: hash by short_code (URL shortener), hash by follower_id (feeds), geography (ride-hailing), per-document leader (collab editing). Always ask "what's the most common lookup, and does my shard key let that lookup hit one shard?"
- **Distributed ID/coordination problems** (Snowflake IDs, worker assignment, rate limiter counters) generally resolve to: use an atomic operation (Lua script, CAS) or a coordination service (etcd/ZooKeeper) rather than hoping for the best across independent processes.
- **Consistency requirements are not uniform across a system**: read-your-writes for the author's own content; eventual consistency for likes/views/counters; strong consistency for payments/inventory. Explicitly identifying *which* pieces of a system need which consistency model — rather than picking one model for everything — is the meta-skill tested across all of these.
- **Cost as a constraint, not an afterthought**: storage/CDN egress dominates cost in content-heavy systems (video, blog images) — worth naming tiered storage, downsampling, and retention policies unprompted.

---

## Suggested Remaining Prep (with limited time)

1. **Interactive mock mode** on 2-3 of the above — ideally the payment/booking system (biggest mindset gap vs. the read-heavy platforms) and whichever else feels shakiest. Reading is passive; the interview tests whether you can *generate* this reasoning live under mild pressure.
2. Practice **defending your own scale estimates out loud** before being challenged on them — catching an unrealistic number yourself is a stronger signal than being corrected.
3. For each problem, practice stating **2-3 options before picking one** on the key decision (fan-out strategy, consistency model, sharding key) — this is the single biggest lever separating mid-level from senior/staff performance.
