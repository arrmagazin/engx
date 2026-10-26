---
type: Guide
title: Caching — Core Concepts
description: Covers caching patterns and failure modes, CDNs, and Redis's core concepts, messaging primitives, and typical uses.
tags: [tech-stack, redis, caching, in-memory]
---

The vocabulary of caching, the edge that serves cached content (CDNs), and the store most often used for caching (Redis).

## Core Concepts

Caching
: Keeping a copy of a result closer to its consumer than the system that produced it

Cache-Aside Pattern
: The application reading the cache first and, on a miss, loading from the database and filling the cache itself; simple, but exposed to Cache Stampede and to a concurrent write leaving a stale entry

Write-Through
: Writing to the cache and the database in the same operation, so reads after a write find a fresh entry, at the cost of slower writes

Cache Stampede
:   Many requests missing the same popular key at once — typically the moment it expires, often when load looked lowest — and all reaching the database together; a [thundering herd](01-common-concepts.md#scale-and-reliability) on the origin, defended by:

    - stale-while-revalidate — serve the old value while one request refreshes it
    - jittered expiry — so related keys do not expire together
    - request coalescing — one origin fetch per key, shared by every waiting request

Cache Invalidation
: Purging or versioning a cached copy when the data behind it changes

## Content Delivery Network

Content Delivery Network (CDN)
: Geographically distributed edge servers holding static and semi-static content close to users, cutting latency and origin load

301 vs. 302 Redirect
: The choice between a permanent redirect browsers cache, which saves requests but hides per-click data, and a temporary one that reaches the server every time

Adaptive Bitrate Streaming
: Video published as short segments at several quality levels, with the client switching level as network conditions change; HLS and DASH are the two standards in use

## Redis

An in-memory store that runs commands one at a time, so each is atomic without locking — the default choice for caches, sessions, rate limiters, and leaderboards. Redis left the BSD license in 2024; its last BSD release was forked as **Valkey**, which shares its commands and protocol, so everything below applies to both.

### Redis Concepts

- **Data structures** — strings, hashes, lists, sets, sorted sets, streams, HyperLogLog, geospatial indexes.
- **Persistence (optional)** — point-in-time snapshots, an append-only log replayed on restart (slower, but loses less), or both.
- **Replication** — primary-replica, asynchronous by default, so a failover can lose the last writes.
- **Cluster mode** — 16,384 hash slots spread across primaries; a key's slot is `CRC16(key) mod 16384`, resolved by the client.
- **Expiry and eviction** — per-key TTL; once memory is full, a policy chooses what goes (LRU, LFU, or random, over all keys or only keys with a TTL) or rejects writes.
- **Atomic multi-step operations** — a Lua script, which runs as one command.

### Pub/Sub vs. Streams

- **Pub/Sub** — fire-and-forget: no persistence, no replay. A message is lost if no subscriber is listening.
- **Streams** — Redis's Kafka-like primitive: persistent, replayable, with consumer groups and per-consumer offsets.

For a durable event backbone between services, use a log such as [Kafka](04-messaging.md).

### Typical Uses

- **Cache and session store** — fast key lookup with expiry built in.
- **Rate limiting** — atomic `INCR` plus `EXPIRE`, or a sliding window on a sorted set.
- **Leaderboards** — sorted sets: insert is O(log N), reading the top M is O(log N + M).
- **Distributed locks** — `SET key value NX PX ttl` on one instance. The multi-node Redlock algorithm is publicly disputed: [Kleppmann](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) argues its safety depends on bounded clock drift and pauses; [antirez disputes that](https://antirez.com/news/101). Where a lock lost mid-operation corrupts data, use a system that issues a fencing token.

## References

1. [Redis Cheat Sheet](https://devsheets.io/sheets/redis) — DevSheets
