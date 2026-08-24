---
type: Guide
title: Redis — Core Concepts and Workflow
description: Explains Redis's core concepts, request workflow, pub/sub vs. streams, and typical use cases.
tags: [tech-stack, redis, caching, in-memory]
---

# Redis — Core Concepts and Workflow

Redis holds its dataset in memory and executes commands one at a time, which is what makes single commands atomic without locking and what makes it the default choice for caches, sessions, rate limiters, and leaderboards. This guide covers the data structures, how a command travels through persistence and replication, the two messaging primitives, and the patterns built on top.

## Core Concepts

- **In-memory data store** — key-value at its core, with rich structures: strings, hashes, lists, sets, sorted sets (ZSETs), streams, bitmaps, HyperLogLog, geospatial.
- **Single-threaded event loop** — commands execute one at a time per shard, giving atomicity for single commands with no locking. Redis 6+ added I/O threading for networking, but command execution itself stays single-threaded.
- **Persistence (optional)**:
  - **RDB** — point-in-time snapshots to disk.
  - **AOF** — append-only log of every write, replayed on restart. Slower, more durable.
  - Can run both together.
- **Replication** — primary-replica, async by default. Replicas serve reads and stand by for failover.
- **Cluster mode** — sharding via 16,384 hash slots; each master owns a subset. Client resolves the shard via `CRC16(key) mod 16384`.
- **Sentinel** — separate HA/failover manager for non-cluster deployments.
- **Eviction** — once `maxmemory` is reached, `maxmemory-policy` decides what goes. `noeviction` returns an error on writes instead of evicting anything. The `allkeys-*` policies consider every key and the `volatile-*` policies only keys that have a TTL set, each available as `lru`, `lfu`, and `random`; `volatile-ttl` evicts the nearest expiry first.
- **Transactions** — `MULTI`/`EXEC` (optimistic, queued), `WATCH` for compare-and-swap.
- **Lua scripting** — `EVAL` for atomic multi-step server-side operations.
- **Expiry** — per-key TTL (`EXPIRE`), core to cache and rate-limiter patterns.

## Workflow

1. Client sends a command over RESP (Redis's binary-safe protocol).
2. Event loop processes it synchronously against the in-memory dataset.
3. If persistence is enabled, the write is appended to the AOF log and/or captured in the next RDB snapshot.
4. If replication is set up, the write is asynchronously propagated to replicas.
5. In cluster mode, the client (or a proxy) resolves which shard owns the key's hash slot before sending the command.

## Pub/Sub vs. Streams

- **Pub/Sub** (`PUBLISH`/`SUBSCRIBE`) — fire-and-forget, no persistence, no replay. Message is lost if no subscriber is listening.
- **Streams** (`XADD`/`XREAD`, consumer groups via `XREADGROUP`) — Redis's actual Kafka-like primitive: persistent, replayable, per-consumer offsets.

## Typical Use Cases

- **Cache** — cache-aside or write-through, TTL-based invalidation.
- **Session store** — fast key lookup with expiry built in.
- **Rate limiting** — atomic `INCR` + `EXPIRE`, or sliding-window via sorted sets.
- **Leaderboards** — sorted sets: `ZADD` is O(log N), and `ZRANGE` is O(log N + M) for the M entries it returns.
- **Distributed locks** — `SET key value NX PX ttl` against a single instance. The multi-node Redlock algorithm extends this across independent masters, but its safety is disputed in public — Kleppmann argues it depends on bounded clock drift and pause times, antirez disputes that reading. Do not use it where a lock lost mid-operation corrupts data; use a system that offers a fencing token instead.

## Entities Diagram

```
Clients (commands)
      │
      ▼
┌─────────────── Redis instance ───────────────┐
│  In-memory key-value store                    │
│  ┌──────────────────┐                         │
│  │ Event loop        │                         │
│  │ Single-threaded    │                         │
│  ├──────────────────┤     ──► Replicas          │
│  │ Dataset            │        R1, R2 (async)    │
│  │ Strings, hashes,   │                         │
│  │ sets, ZSETs        │                         │
│  ├──────────────────┤                         │
│  │ Expiry & eviction  │                         │
│  │ TTL + LRU/LFU      │                         │
│  └──────────────────┘                         │
└────────────────────┬───────────────────────────┘
                      ▼
                 Disk (RDB / AOF)
```

## Node.js / TypeScript (ioredis)

```ts
import Redis from 'ioredis';
const redis = new Redis(process.env.REDIS_URL);

await redis.set('session:abc123', JSON.stringify(sessionData), 'EX', 3600);
const session = await redis.get('session:abc123');

// atomic rate limit counter
const count = await redis.incr(`rate:${userId}`);
if (count === 1) await redis.expire(`rate:${userId}`, 60);
```
