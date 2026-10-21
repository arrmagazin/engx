---
type: Guide
title: Canonical Systems
description: Eleven canonical system design problems, each organized by the core bottleneck it tests, plus the patterns that recur across them.
tags: [architecture, system-design, interview]
---

Eleven system design problems, each filed under the bottleneck it tests rather than the product it resembles. Terms are defined in the [System Design Glossary](01-common-concepts.md). These are generic interview designs, not descriptions of how any named company builds its systems.

| System | Similar product | Core Bottleneck Tested |
| --- | --- | --- |
| **URL Shortener** | bit.ly | ID generation, sharding, hot key |
| **Blogging Platform** | Medium | Social graph fan-out, read/write split |
| **Short-Video Platform** | TikTok | Ranking/retrieval at scale, storage + CDN cost |
| **Messaging Platform** | Telegram | Connection state, delivery guarantees, ordering |
| **Ride-Hailing / Nearby Search** | Uber | Geospatial indexing, high-churn writes |
| **Distributed Rate Limiter** | (generic API infra) | Concurrency correctness, tight scope |
| **Web Crawler / Search Engine** | Google | Parallel crawling, inverted index, freshness |
| **Payment / Booking System** | Ticketmaster / Stripe-like | Strong consistency, idempotency, sagas |
| **Notification System** | (generic, multi-channel) | Multi-channel fan-out, dedup, retries |
| **Collaborative Editing** | Google Docs / Figma | Conflict resolution (OT/CRDT) |
| **Metrics / Monitoring Infrastructure** | Datadog-style | Time-series write volume, rollups |

## 1. URL Shortener

**Requirements** — shorten, redirect, custom aliases, click analytics. Short URLs are **immutable**, which removes a whole class of caching problems.

**Scale** — assume ~1,000 writes/sec (86M URLs/day) and 10-100x that in redirects. At ~200-300 bytes per record, 3 years is ~95B records: tens of TB raw, ×3 for replication. **It needs sharding.**

- **IDs** — a Snowflake-style generator: 41 bits of millisecond timestamp (~69 years), 10 bits of worker ID (1,024 workers), 12 bits of sequence (4,096 IDs per worker per ms). Workers claim their ID by a lease in etcd or ZooKeeper, not by config — at the cost of a startup dependency.
- **Codes** — Base62: 62^6 ≈ 57B and 62^7 ≈ 3.5T, so 6-7 characters cover the record count. Shuffle the bits so codes are not sequential, which prevents enumeration and hides volume.
- **Custom aliases** — a Bloom filter in front of the uniqueness check fails fast on "already taken".
- **Sharding** — by hash of `short_code`, because redirects, the dominant query, already hold it. "All links of user X" then needs a secondary index — acceptable for a rarer query.
- **Read path** — cache by `short_code` first (popularity follows a power law), then the shard. Use **302**, not 301: a permanent redirect is cached by browsers and would hide the clicks the analytics requirement needs.
- **Analytics** — publish click events to a queue and aggregate them elsewhere; never write them synchronously to the primary.

**Failure modes** — a cache stampede on a viral link (request coalescing, jittered TTL); a coordination outage (existing workers run on, but no new ones can start).

## 2. Blogging Platform

**Requirements** — authors publish and edit posts; readers read, search, comment, clap, and follow authors for a reverse-chronological feed.

**Scale** — 1M posts/day ≈ 12 writes/sec; 100M reads/day ≈ 1,150 reads/sec, 5-10x that at peak. **Read:write ≈ 100:1**, and images outweigh text by orders of magnitude, so the bottleneck is blob storage and CDN egress, not the relational data.

- **Data** — shard `posts` by `post_id` and `follows` by `follower_id`, matching the feed query "who does X follow". Keep the metadata row apart from the body in blob storage, so list queries stay fast. Route an author's own reads to the primary briefly after an edit (read-your-writes).
- **Feed** — hybrid fan-out: push to followers' feeds for ordinary authors, merge at read time for authors above a threshold (e.g. 100K followers).
- **Claps** — `UPDATE ... claps = claps + 1` serializes on a popular post's row lock. Count in a stream and flush in batches; an approximate count is fine.
- **Search** — index change events into a search engine; never query the primary.
- **CDN** — the biggest lever at 100:1; invalidate on publish with versioned URLs.

## 3. Short-Video Platform

**Requirements** — upload short videos; an algorithmically ranked infinite feed; instant playback on scroll over variable networks.

**Scale** — 100M DAU × ~60 views/day ≈ 6B views/day ≈ **70,000 views/sec**; 1M uploads/day ≈ 12/sec, a view:upload ratio near 6,000:1. The bottleneck is storage, transcoding, and CDN egress, not the metadata database.

- **Upload** — store the raw file, create a `pending` row, and return. A queue feeds transcoding workers (several resolutions, thumbnails, moderation); on completion the video goes to the CDN origin and the ranking pool. The creator sees it at once; others only after moderation.
- **Feed** — not social fan-out: content comes from the whole corpus. A cheap pass narrows billions of videos to hundreds, then a heavy model ranks only those, per session rather than per scroll to save cost.
- **Prefetching** — the client fetches the next videos' first segments before the swipe. This removes a round trip from the critical path, so it matters more for first-frame latency than faster ranking.
- **Delivery** — adaptive bitrate from the CDN. New videos have no engagement history (the cold-start problem), so some traffic goes to unproven content on purpose.
- **Counters** — aggregate view events in a stream processor and flush deltas; never increment per view.

**Main trade-off** — cost is first-class. Storage, transcoding, and egress dominate spend, so evicting cold high-resolution renditions of long-tail videos is a design decision.

## 4. Messaging Platform

**Requirements** — 1:1 and group chat, real-time when online and queued when offline; receipts and presence; multi-device sync; broadcast channels with millions of subscribers.

**Scale** — 100M DAU × 20 messages/day ≈ **23,000 messages/sec** average. The sizing question is how many sockets are open at peak, not how many messages are sent: **a latency and connection problem, not a storage problem.**

- **Connections** — persistent connections to a gateway sharded by user, plus a presence map (user → node) that changes on every reconnect. Clients reconnect with backoff and jitter, or every client of a crashed gateway returns at once and topples the next.
- **Delivery** — persist first, then deliver: durability must not depend on the recipient being online. The sender's acknowledgment means "persisted"; delivered and read are later state changes.
- **Ordering** — a per-conversation sequence number, not wall-clock time. It exposes gaps and makes resumption idempotent ("everything after #4521").
- **Multi-device** — every device syncs by sequence number against the server's store, so read state reaches every device.
- **Groups and channels** — fan out on write for small groups; for large channels store each post once and let subscribers pull, the blog's celebrity problem again.
- **Guarantees** — at-least-once delivery plus client-side deduplication by message ID. Typing indicators and presence are loss-tolerant and never persisted.

**Main contrast** — the content platforms were carried by caching and CDNs; this one by connection state and delivery guarantees.

## 5. Ride-Hailing / Nearby Search

**Requirements** — match riders to nearby available drivers; drivers report location every few seconds; surge pricing from local supply and demand.

**Scale** — 5M connected drivers reporting every ~4 sec ≈ **1.25M location writes/sec**: write-heavy and high-churn. Ride requests are only thousands per second.

- **Spatial index** — a distance scan over rows does not work. Index by geohash and query the neighboring cells, or use a quadtree or the S2 library.
- **Storage** — positions live in memory; losing a few seconds of them on a crash is acceptable.
- **Matching** — search outward from the rider's cell in rings until there are enough candidates, rank by road-network ETA, offer to the best, and on decline or timeout move to the next.
- **Sharding** — by region, not by hash: a Tokyo driver never matches a Chicago rider, and the shard key should follow the query.

**Main trade-off** — update the index on every ping (fresh, expensive) or in batches (cheap, stale); a few seconds of staleness is usually fine.

## 6. Distributed Rate Limiter

**Requirements** — limit each API key to N requests per window, correctly across many stateless servers. Concurrency correctness, not volume, sets the design.

- **Algorithm** — a sliding window counter is the usual default (constant memory, close enough); a token bucket where controlled bursts are wanted. The algorithms are compared in [Rate Limiting](01-common-concepts.md#rate-limiting).
- **Shared state** — counters in a central Redis. "Read, check, increment" lets two requests on different servers both pass; use one atomic round trip — `INCR` returning the new value, or a Lua script.

**Main trade-off** — at extreme scale the central store becomes a bottleneck and a single point of failure. Shard it by key, or keep local counters synced periodically and accept a less exact limit.

## 7. Web Crawler / Search Engine

**Requirements** — crawl the web, discover pages through links, re-crawl changed pages, and serve ranked results in under 200 ms.

**Core constraint** — fetching is easily parallel; the coordination is not. Thousands of workers share one record of visited URLs, a web where one heavily linked domain could absorb them all, and one fetch budget.

- **Frontier** — the queue of URLs to fetch, partitioned by domain. Deduplicate with a Bloom filter: a false positive skips a page, never fetches one twice, and it fits billions of URLs in memory.
- **Politeness and priority** — per-domain rate limits, so no site is overwhelmed; re-crawl frequency from each page's change rate and importance.
- **Index** — an inverted index sharded by term or by document range, rebuilt in large batches; "how soon must a new page be searchable?" is a scoping question.
- **Query** — look up posting lists across shards, merge, and rank the candidates in two stages, as in the video feed.

**Main trade-off** — the budget is split between discovering new pages (completeness) and re-checking old ones (freshness); no split maximizes both.

## 8. Payment / Booking System

**Requirements** — book a seat or take a payment; never oversell or double-charge; integrate with an external payment processor.

**Core constraint** — every system above could accept eventual consistency, caching, and approximate counts. **This one cannot**: correctness outranks latency and throughput.

- **Overselling** — [locking or optimistic concurrency](02-databases.md#transactions-and-locking) on the seat row; optimistic slows when everyone wants the front row. A **reservation with TTL** separates a 10-minute hold from a sale, and a background job releases expired holds.
- **Double charges** — an idempotency key per checkout attempt, so a retry after a timeout does not charge again.
- **Multi-step flow** — reserve → charge → confirm → issue ticket runs as a saga with compensating actions (a refund), because no ACID transaction spans a processor you do not control.
- **Webhooks** — the processor's callback can arrive more than once, so the handler checks the unique event ID before acting.

**Main trade-off** — the database, not the cache, is the source of truth: read the primary for money and inventory and pay the latency, the opposite instinct from the read-heavy platforms.

## 9. Notification System

**Requirements** — push, email, and SMS triggered by events; per-user preferences, opt-outs, and quiet hours; batching and digests instead of spam.

**Core constraint** — correct, restrained delivery, not volume. Events arrive at-least-once, every send goes through a third-party provider with its own failures, and one replayed event without deduplication becomes duplicate pushes at 3 a.m.

- **Preference and dedup layer** — where most of the product complexity lives: "5 people liked your post" as one push, not five.
- **Retries** — backoff per provider, and a dead-letter queue for sends that keep failing, such as an invalid device token.
- **Per-user limits and priority tiers** — a bug cannot send hundreds of pushes to one person, and security alerts preempt marketing.

## 10. Collaborative Editing

**Requirements** — several users edit one document at once, see each other's changes in near real time, and all copies converge.

**Core constraint** — the one place where last-write-wins breaks the product: two edits at the same position would silently drop one person's text.

- **Merge logic** — Operational Transformation (proven, with subtle edge cases) or a CRDT (simpler convergence, with tombstone overhead; Figma describes its approach as CRDT-inspired).
- **Session server** — each editor connects to a server that holds the document's state in memory, applies the merge, and broadcasts the result; periodic snapshots spare a full history replay on open.

**Main trade-off** — shard per document, not per user: every edit to one document must pass through one leader, the opposite of hash-sharding by user elsewhere.

## 11. Metrics / Monitoring Infrastructure

**Requirements** — ingest metrics from millions of hosts at high frequency; dashboards and alerts over arbitrary time ranges.

**Scale** — 1M hosts × 100 metrics every 10 sec ≈ **10M writes/sec**, in small, append-only records.

- **Time-series database**, not a general relational one: writes go to the current time bucket, which makes sharding and compaction simple.
- **Batched ingestion** — clients batch points before sending; the server writes in bulk.
- **Downsampling** — roll raw 10-second points up to 1-minute, 1-hour, and 1-day aggregates and delete raw data after a retention window. Dashboards must be designed around it: last year cannot be zoomed to 10 seconds.
- **Alerting** — a separate consumer of the ingest stream, so it need not wait for rollups and a slow rule never blocks ingestion.

## Cross-System Patterns

- **Fan-out on write vs. on read** (blog feed, chat channels) — a follower threshold between the two is usually the answer.
- **Narrow, then rank** (video feed, search) — never run the expensive step over the whole corpus.
- **Async pipeline for anything off the critical path** — analytics, counters, indexing, moderation.
- **Shard along the dominant query** — by short code, by follower, by region, by document.
- **Consistency differs within one system** — read-your-writes for an author, eventual for counts, strong for money. Picking one model for the whole system is the mistake.
