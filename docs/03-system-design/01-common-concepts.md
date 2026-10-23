---
type: Guide
title: System Design Glossary
description: Defines the system design vocabulary this chapter uses, grouped by the problem each set of terms addresses.
tags: [architecture, system-design, interview, glossary]
---

## System Design Loop

A framework for any system design question, and the signals that separate a senior or staff answer from a mid-level one. Its worked problems are in [Canonical Systems](../03-system-design/08-canonical-systems.md): eleven of them, each filed under the bottleneck it tests.

Care about:

1. **Justified assumptions** — every number (scale, storage, ratios) should be defensible, not invented.
2. **Generating options before picking one** — for any key decision, name 2–3 alternatives and explain the trade-off, instead of stating your first idea.
3. **Recognizing the *actual* hard problem** — different systems have different bottlenecks (write-heavy vs. read-heavy, strong vs. eventual consistency, connection-state vs. stateless). Applying the same pattern to every problem by reflex is a mid-level sign.
4. **Naming failure modes and cross-cutting concerns unprompted** — cache stampedes, hot shards, clock skew, idempotency, moderation, and cost.

Work these six steps in order, whatever the problem.

1. **Requirements** — functional and non-functional, stating explicitly what is out of scope.
2. **Scale estimates** — traffic (reads/writes per sec), storage growth, and which ratio (read:write) dominates. Check them against real-world reference points.
3. **High-level architecture** — draw the boxes: clients, load balancer, services, cache, DB, and async pipeline.
4. **Data model and sharding** — what is the shard key, and why does it match the dominant query pattern?
5. **Deep dives** — 2–4 of the *actually hard* parts; not everything deserves equal depth.
6. **Cross-cutting concerns** — failure modes, caching, consistency trade-offs, and cost, named without being asked.

## Capacity Estimation

Capacity Estimation
: An order-of-magnitude sizing of traffic, storage, and bandwidth from stated assumptions — storage is write rate × record size × retention × replication factor

Read:Write Ratio
: The proportion of reads to writes; decides whether a design optimizes for caching or for write throughput

QPS (Queries per Second)
: The standard throughput unit, quoted separately for average and peak load because the two size different components

## Scale and Reliability

Blast Radius
: How much else breaks when one component breaks; the reason to split stacks, queues, and accounts

Bulkhead
: Separate resource pools (connections, threads, queues) per dependency or consumer, so one slow dependency exhausts only its own pool; it confines a failure rather than preventing it

Circuit Breaker
: A wrapper that stops calling a dependency after a failure threshold, fails fast for a cooling-off period, then lets one trial request through — freeing the caller and giving the dependency room to recover

Graceful Degradation
: Serving a reduced response when part of it cannot be produced, instead of failing the whole request; the optional parts are chosen in advance

Percentile Latency
: The latency below which a stated share of requests fall (p50, p95, p99); an average hides the slow tail, which compounds under fan-out — ten parallel calls each slow 1% of the time make one page in ten slow

Thundering Herd
: Many clients hitting one resource at the same moment, as when retries share a timeout; fixed by jitter and exponential backoff, without which retries turn one outage into a repeating one — the cache case is a [cache stampede](03-caching.md#core-concepts)

Head-of-Line Blocking
: One stuck item at the front of an ordered queue stalling every item behind it — the price of strict ordering

## Identifier Generation

Distributed ID Generator
: A scheme producing unique, roughly time-ordered 64-bit IDs on independent machines with no central allocator — timestamp, worker, and sequence bits

Clock Skew
: A machine's clock jumping backward after a correction, risking reuse of an already-issued timestamp; detected by refusing to generate while `now < last_timestamp`

Compare-and-Swap (CAS)
: An atomic update applied only if the current value matches an expected one, used to claim a shared slot without a race

Lease
: A time-bound claim on a resource, renewed by heartbeat and expiring if the holder crashes — how a generator claims a worker slot by Compare-and-Swap

Base62 Encoding
: Writing a number with the 62 URL-safe alphanumeric characters, turning a large integer ID into a short code

## Idempotency

Idempotency
: The property that applying an operation more than once has the same effect as applying it once

Idempotency Key
: A client-generated unique value per operation, letting the server recognize a retry instead of repeating the side effect

Why almost every queue makes Idempotency mandatory is in [Delivery Semantics](04-messaging.md#delivery-semantics).

## Concurrency Control

Concurrency Control
: Keeping simultaneous writers from corrupting shared state; optimistic and pessimistic approaches are compared in [Transactions and Locking](02-databases.md#transactions-and-locking)

Reservation with TTL
: A short-lived hold that expires unless confirmed, separating temporarily held state from committed state

## Service Decomposition

Service Decomposition
: Dividing a system into independently deployable units and deciding where the lines between them fall

Monolith
: One deployable unit holding the whole application, where calls between modules are in-process and a release ships every part at once

Microservice
: A unit owning one capability and its data, released on its own schedule, at the price of network calls and operational surface

Service Boundary
: The line around a deployable unit, placed where data and reasons to change are cohesive; a line cutting through either turns routine work into a multi-team release

Bounded Context
: The scope within which one model of a domain term holds without qualification, the usual guide for where that line belongs

Distributed Monolith
: Units deployed separately yet coupled tightly enough that none can ship alone, paying the cost of the split without collecting its benefit

Shared Database Coupling
: Two units using the same tables, so a schema change forces a coordinated release and the split buys nothing

Remote Call Cost
: What a call becomes across a process boundary — slow, able to fail alone, able to arrive twice — so it needs retries and repeat-safe handlers

## Distributed Transactions

Distributed Transaction
: A single logical operation spanning services that share no database and therefore no commit

Saga Pattern
: Running a Distributed Transaction as an ordered series of local transactions, each with an undo step for when a later one fails

Compensating Action
: The undo step in a saga — a refund, a released hold, a canceled reservation

## Fan-Out

Fan-Out
: The multiplication of one write into many downstream writes or reads, one per recipient

Fan-Out on Write
: Pushing content into every recipient's feed at publish time; fast reads, but expensive for accounts with many followers

Fan-Out on Read
: Merging content from followed sources when a feed is requested; cheap writes, but costly reads across shards

Celebrity Problem
: One account with a very large follower count making write-time fan-out prohibitive, since a single post triggers millions of writes

Hybrid Fan-Out
: Pushing for ordinary accounts and merging at read time above a follower threshold

## Rate Limiting

Rate Limiting
: Capping a caller's requests per period, counted per user, IP, or API key — one global limit lets a heavy caller starve everyone

Fixed Window Counter
: Counting requests per calendar window; simple, but permits a double-rate burst across a window boundary

Sliding Window Log
: Storing each request's timestamp and counting those inside the trailing window; exact, but memory-heavy

Sliding Window Counter
: Approximating the Sliding Window Log by weighting the current and previous fixed windows, at constant memory

Token Bucket
: Tokens added at a fixed rate and one spent per request, allowing bursts up to the bucket size

Atomic Increment
: Checking and incrementing a counter in one indivisible step, such as a Redis Lua script, so two concurrent requests cannot both pass the limit

## Indexing

Geohashing
: Encoding latitude and longitude into a string whose shared prefixes mean physical proximity, which also makes it usable as a shard key

Quadtree
: A tree that recursively subdivides two-dimensional space, more finely where points are dense

Inverted Index
: The mapping from each term to the documents containing it (its posting list), so a query is answered by term instead of by scanning every document

Bloom Filter
: A compact probabilistic membership test that can report a false positive but never a false negative

Time-Series Database
: A store partitioned by time, so writes land in the current bucket and old buckets compact or archive whole

Downsampling
: Replacing fine-grained history with coarser aggregates as it ages, then deleting the raw points after a retention window

## Conflict Resolution

Operational Transformation (OT)
: Transforming concurrent operations against each other so they apply in any order and converge; the approach Google has described for Google Docs

CRDT (Conflict-Free Replicated Data Type)
: A data type whose concurrent updates merge deterministically without resolution logic, typically by giving every element a unique ordered ID

Tombstone
: A marker left where data was deleted, so the deletion can be ordered against concurrent operations, at the cost of storage
