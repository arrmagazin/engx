---
type: Guide
title: System Design Glossary
description: Defines the system design vocabulary this chapter uses, grouped by the problem each set of terms addresses.
tags: [architecture, system-design, interview, glossary]
---

# System Design Glossary

Defines the vocabulary the rest of this chapter uses, grouped by the problem each set of terms addresses. Worked applications of these concepts are in [Canonical Systems](08-canonical-systems.md).

## Design Practice

Design Practice
: The habits that apply to any system design, independent of the system being designed

Requirements Scoping
: Stating what the system must do, which quality attributes bound it, and what is deliberately excluded, before any design follows

Deep Dive
: Detailed treatment of one hard sub-problem, rather than equal shallow coverage of every component

Trade-Off Articulation
: Naming what a choice costs and what was rejected, instead of presenting one option as the only one

Failure Mode
: A specific way a component breaks or degrades under stress, such as a stampede, a storm, or a hotspot

Cost as a Design Constraint
: Treating storage, egress, and compute spend as a factor in the design itself rather than a later concern

## Capacity Estimation

Capacity Estimation
: Sizing a system's traffic, storage, and bandwidth before designing it, so the design answers to numbers rather than intuition

Back-of-Envelope Estimation
: An order-of-magnitude calculation from a few stated assumptions — writes per second times record size times retention

Read:Write Ratio
: The proportion of reads to writes; decides whether a design optimizes for caching and delivery or for write throughput and consistency

QPS (Queries per Second)
: The standard throughput unit, quoted separately for average and peak load because the two size different components

Storage Growth Projection
: Total storage over a stated horizon, from write rate times record size times time, adjusted for the replication factor


## Scale and reliability

**Blast radius** — How much breaks when one thing breaks. It is the metric that
justifies splitting stacks, queues, and accounts, and it is why this scaffold's
table lives in a stack that a routine release cannot touch. Designing for it
means asking "what else fails" before "how do we stop this failing".

**Bulkhead** — Partitioning resources so that exhaustion in one part cannot
starve the others — separate connection pools, separate thread pools, separate
queues per consumer. It is named after ship compartments, and the analogy is
exact: the point is not to prevent flooding but to confine it. Without it, one
slow downstream dependency consumes every connection and takes down endpoints
that never touched it.

**Cache-aside** — The application checks the cache, and on a miss reads the
source and populates the cache itself. It is the most common caching pattern
because it is simple and the cache never needs to know about the database, but
it has two well-known holes: a stampede on a popular miss, and a window where a
concurrent write leaves a stale entry behind.

**Cache stampede** — When a popular cache entry expires, every request that
wanted it goes to the origin at once, and the origin falls over precisely
because the thing was popular. Defences are `stale-while-revalidate` (serve the
stale value while one request refreshes), TTL jitter (so entries created
together do not expire together), and request coalescing. The failure is
counter-intuitive because load is *lowest* right before it happens.

**Circuit breaker** — A wrapper that stops calling a failing dependency after a
threshold, fails immediately for a cooling-off period, then lets a trial request
through. It exists because retrying a struggling service is the worst thing you
can do to it, and because a caller blocked on a dead dependency is a caller
holding resources for nothing. The subtle benefit is to the *callee*: the
breaker gives it room to recover.

**Cold start** — The latency of initialising a new execution environment before
it can serve its first request — for Lambda, downloading and starting the
runtime and the handler's module graph. It matters for user-facing synchronous
work and matters much less for queue consumers, where a few hundred extra
milliseconds are invisible. It is the main reason this scaffold serves the read
path from a container and the write path from Lambda.

**Graceful degradation** — Continuing to serve a reduced version of the response
when part of it cannot be produced, rather than failing the whole thing. It is a
design decision that must be made in advance, because during an incident nobody
is deciding which fields are optional.

**Head-of-line blocking** — When the item at the front of a queue cannot be
processed and everything behind it waits, even though those items are fine. It
is the specific risk of strict ordering: FIFO with a message group means one
stuck message stalls that entire group. Recognising it is what makes "use a FIFO
queue for ordering" a trade rather than an answer.

**p50 / p95 / p99** — Percentile latencies: the value below which that
percentage of requests fall. They are quoted instead of an average because
latency distributions have long right tails, and an average hides the tail
entirely — a service can average 40 ms while one request in a hundred takes four
seconds. At scale, p99 is not an edge case: at 50 requests per second it is one
unhappy user every two seconds.

**Read-your-writes** — The consistency property that a client immediately sees
its own write, even if others do not yet. It is often the only consistency
guarantee a user actually notices, which means it is frequently the cheapest one
worth buying: route a user's reads to the primary briefly after they write,
rather than making the whole system strongly consistent.

**Tail latency** — The slow end of the latency distribution, and usually the
only end that matters once a service is fast on average. It compounds badly with
fan-out: if a page makes ten parallel calls each with a 1% chance of being slow,
roughly one page in ten is slow. This is why budgets and timeouts belong on
individual calls rather than only on the whole request.

**Thundering herd** — Many clients waking simultaneously and hitting the same
resource — retries synchronised by a common timeout, or caches expiring
together. The fix is always to break the synchronisation: jitter on TTLs, jitter
and exponential backoff on retries. A retry policy without jitter converts one
outage into a repeating one.

---

## Identifier Generation

Identifier Generation
: Producing unique keys for records across many machines without a central allocator on the request path

Distributed ID Generator
: A scheme yielding globally unique, roughly time-ordered 64-bit IDs from independent machines; typically timestamp bits, worker bits, and sequence bits

Sequence Number
: A counter incremented within one timestamp tick on one worker, disambiguating IDs generated in the same millisecond

Clock Skew
: A machine's clock jumping backward after a correction, risking reuse of an already-issued timestamp; detected by refusing to generate while `now < last_timestamp`

Worker ID Assignment
: Giving each generator instance a unique slot automatically rather than by hand, and reclaiming the slot when the instance dies

Lease
: A time-bound claim on a resource, renewed by heartbeat and expiring on its own if the holder crashes

Compare-and-Swap (CAS)
: An atomic update applied only if the current value matches an expected one, used to claim a shared slot without a race

Base62 Encoding
: Representing a number in the 62 URL-safe alphanumeric characters, turning a large integer ID into a short code

## Idempotency

Idempotency
: The property that applying an operation more than once has the same effect as applying it once

Idempotency Key
: A client-generated unique value per operation, letting the server recognize a retry instead of repeating the side effect

Idempotent Webhook Handling
: A callback handler that checks a unique event ID before acting, so a redelivered event takes effect once

At-Least-Once Delivery
: A guarantee that a message arrives one or more times but never zero, leaving duplicate handling to the receiver

Client-Side Deduplication
: Discarding repeats by message ID on the receiving side, the standard counterpart to at-least-once delivery

## Concurrency Control

Concurrency Control
: Keeping simultaneous writers from corrupting shared state

Optimistic Concurrency Control
: Reading a version, updating only if it still matches, and retrying on conflict; higher throughput until contention concentrates on one record

Pessimistic Locking
: Taking a lock before modifying a record and blocking other writers until release; simple and correct, but throughput-limiting

Reservation with TTL
: A short-lived hold that expires unless confirmed, separating temporarily held state from committed state

## Service Decomposition

Service Decomposition
: Dividing a system into independently deployable units and deciding where the lines between them fall

Monolith
: One deployable unit holding the whole application, where calls between modules are in-process and a release ships every part at once

Microservice
: A unit owning one capability and the data behind it, released on its own schedule, at the price of network calls and operational surface where an in-process call once served

Service Boundary
: The line drawn around such a unit, placed where data and reasons to change are cohesive, since a line cutting through either turns routine work into a multi-team release

Bounded Context
: The scope within which one model of a domain term holds without qualification, the usual guide for where that line belongs

Distributed Monolith
: Units deployed separately yet coupled tightly enough that none can ship alone, paying the cost of the split without collecting its benefit

Shared Database Coupling
: Two units reading and writing the same tables, which removes the independence the split was meant to buy because a schema change forces a coordinated release

Remote Call Cost
: What a call becomes once it crosses a process boundary — slow, able to fail on its own, and able to arrive twice — which is why cross-unit operations need retries and repeat-safe handlers

## Distributed Transactions

Distributed Transaction
: A single logical operation spanning services that share no database and therefore no commit

Saga Pattern
: Running that operation as an ordered series of local transactions, each with an undo step for when a later one fails

Compensating Action
: The undo step in a saga — a refund, a released hold, a canceled reservation

## Fan-Out

Fan-Out
: The multiplication of one write into many downstream writes or reads, one per recipient

Fan-Out on Write
: Pushing content into every recipient's feed at publish time; fast reads, expensive for accounts with many followers

Fan-Out on Read
: Merging content from followed sources when a feed is requested; cheap writes, costly reads across shards

Celebrity Problem
: One account with a very large follower count making write-time fan-out prohibitive, since a single post triggers millions of writes

Hybrid Fan-Out
: Pushing for ordinary accounts and merging at read time above a follower threshold

## Feed Ranking

Feed Ranking
: Ordering candidate items for one user by predicted relevance rather than by recency alone

Two-Stage Candidate Generation
: Narrowing a large corpus cheaply and approximately, then scoring only the survivors with an expensive model

Cold-Start Problem
: New items or users having no engagement history, so popularity-based ranking cannot yet place them

Exploration vs. Exploitation
: The trade-off between serving proven content and deliberately serving unproven content to learn its quality

## Real-Time Delivery

Real-Time Delivery
: Pushing data to a client as it happens, rather than waiting for the client to ask

Persistent Connection
: A connection held open between client and server so the server can send without being polled

Connection Gateway
: A layer holding many open client connections, sharded so each user is pinned to one node

Presence Service
: The mapping from user to the gateway node currently holding their connection, rewritten on every reconnect

Reconnection Storm
: Every client of a failed gateway reconnecting at once, requiring backoff and jitter to avoid toppling the replacement

Message Ordering via Sequence Numbers
: A per-conversation monotonic counter that fixes order and exposes gaps, avoiding reliance on clocks that differ across servers

Server-Authoritative Message Store
: The server holding the definitive durable copy that every device syncs against, rather than each device managing its own queue

Multi-Device Sync
: Keeping message content and read state consistent across one user's logged-in devices

Backpressure
: Limiting how fast work is handed to a component that cannot keep up, through pagination, incremental sync, or queueing

## Geospatial Indexing

Geospatial Indexing
: Organizing points on the earth's surface so nearby ones can be found without scanning all of them

Geohashing
: Encoding latitude and longitude into a string whose shared prefixes mean physical proximity, which also makes it usable as a shard key

Quadtree
: A tree that recursively subdivides two-dimensional space, subdividing further where points are dense

Google S2 Library
: A production library for spherical geometry and cell-based indexing, used where a rectangular grid distorts

Ring Search
: Querying a small area first and widening it until enough candidates are found

## Rate Limiting

Rate Limiting
: Capping how many requests a caller may make in a period, to protect capacity and enforce quotas

Fixed Window Counter
: Counting requests per calendar window; simple, but permits a double-rate burst across a window boundary

Sliding Window Log
: Storing each request's timestamp and counting those inside the trailing window; exact, but memory-heavy

Sliding Window Counter
: Approximating the log by weighting the current and previous fixed windows, at constant memory

Limit Scope
: What the limit is counted *per* — user, IP, or API key; a single global limit lets one heavy caller starve everyone else

Token Bucket
: Tokens accruing at a fixed rate and one being spent per request, permitting bursts up to the bucket size

Atomic Increment
: Checking and incrementing a counter in one indivisible step, such as Redis `INCR` inside a Lua script, so two concurrent requests cannot both pass the same limit

## Search Indexing

Search Indexing
: Precomputing a structure that answers queries by term, instead of scanning every document per query

Inverted Index
: The mapping from each term to the documents containing it

Posting List
: The document IDs recorded against one term in an inverted index, often with positions and frequencies

Crawl Frontier
: The queue of URLs a crawler has yet to fetch, with its prioritization and deduplication rules

Politeness Policy
: A per-domain rate limit that keeps a crawler from overwhelming any one site

Bloom Filter
: A compact probabilistic membership test that can report a false positive but never a false negative

## Asynchronous Processing

Asynchronous Processing
: Moving work off the request path so a caller is not made to wait for it

Async Event Pipeline
: Publishing events to a queue and handling them in separate consumers, keeping analytics, counters, and indexing off the hot path

Stream Aggregation
: Computing rolling aggregates from an event stream rather than updating one row per event

Write Amplification via Row-Lock Contention
: Concurrent increments to a single row serializing behind its lock, so throughput falls as traffic on that row rises

Dead-Letter Queue (DLQ)
: A holding queue for messages that have failed processing repeatedly, so they can be inspected instead of retried forever

## Conflict Resolution

Conflict Resolution
: Reconciling concurrent edits to the same data into one agreed result

Operational Transformation (OT)
: Transforming concurrent operations against each other so they apply in any order and converge; the approach Google Docs uses

CRDT (Conflict-Free Replicated Data Type)
: A data type whose concurrent updates merge deterministically without resolution logic, typically by giving every element a unique ordered ID

Tombstone
: A marker left where data was deleted, so the deletion can be ordered against concurrent operations, at the cost of storage

Per-Document Leader
: Pinning every edit for one active document to a single server, because merge logic needs one point all edits pass through

## Time-Series Data

Time-Series Data
: Measurements stamped with a time, written in time order and queried by range

Time-Series Database
: A store partitioned by time, so writes land in the current bucket and old buckets compact or archive whole

Downsampling
: Replacing fine-grained history with coarser aggregates as it ages, since old data rarely needs full resolution

Retention Window
: The age at which raw points are deleted or archived, leaving only downsampled versions

Batched Ingestion
: Grouping many points into one request before sending, cutting per-point overhead at high write volume


---
## Abbreviations

| Abbreviation | Expansion |
| --- | --- |
| ADR | Architecture Decision Record |
| AI | Artificial Intelligence |
| ALB | Application Load Balancer |
| API | Application Programming Interface |
| ARN | Amazon Resource Name |
| ASG | Auto Scaling Group |
| AWS | Amazon Web Services |
| AZ | Availability Zone |
| CAP | Consistency, Availability, Partition tolerance |
| CD | Continuous Delivery / Continuous Deployment |
| CDK | Cloud Development Kit |
| CDN | Content Delivery Network |
| CFN | CloudFormation |
| CI | Continuous Integration |
| CIDR | Classless Inter-Domain Routing |
| CORS | Cross-Origin Resource Sharing |
| CPU | Central Processing Unit |
| CQRS | Command Query Responsibility Segregation |
| CRUD | Create, Read, Update, Delete |
| CSR | Client-Side Rendering |
| CSS | Cascading Style Sheets |
| DAX | DynamoDB Accelerator |
| DDD | Domain-Driven Design |
| DLQ | Dead Letter Queue |
| DNS | Domain Name System |
| DOM | Document Object Model |
| EBS | Elastic Block Store |
| EC2 | Elastic Compute Cloud |
| ECR | Elastic Container Registry |
| ECS | Elastic Container Service |
| EKS | Elastic Kubernetes Service |
| EMF | Embedded Metric Format |
| ENI | Elastic Network Interface |
| FIFO | First In, First Out |
| GSI | Global Secondary Index |
| HA | High Availability |
| IaC | Infrastructure as Code |
| IAM | Identity and Access Management |
| IGW | Internet Gateway |
| ISR | Incremental Static Regeneration |
| JVM | Java Virtual Machine |
| JWT | JSON Web Token |
| KMS | Key Management Service |
| LRU | Least Recently Used |
| LSI | Local Secondary Index |
| MTTR | Mean Time To Recovery |
| NACL | Network Access Control List |
| NAT | Network Address Translation |
| NLB | Network Load Balancer |
| PITR | Point-In-Time Recovery |
| PK | Partition Key |
| RCU | Read Capacity Unit |
| RDS | Relational Database Service |
| RPO | Recovery Point Objective |
| RPS | Requests Per Second |
| RSC | React Server Component |
| RTO | Recovery Time Objective |
| S3 | Simple Storage Service |
| SDK | Software Development Kit |
| SDL | Schema Definition Language |
| SDLC | Software Development Life Cycle |
| SEO | Search Engine Optimisation |
| SG | Security Group |
| SK | Sort Key |
| SLA | Service Level Agreement |
| SLI | Service Level Indicator |
| SLO | Service Level Objective |
| SNS | Simple Notification Service |
| SPA | Single Page Application |
| SPOF | Single Point Of Failure |
| SQS | Simple Queue Service |
| SSE | Server-Side Encryption |
| SSG | Static Site Generation |
| SSL | Secure Sockets Layer |
| SSR | Server-Side Rendering |
| STS | Security Token Service |
| SWR | Stale-While-Revalidate |
| TCP | Transmission Control Protocol |
| TDD | Test-Driven Development |
| TLS | Transport Layer Security |
| TTFB | Time To First Byte |
| TTL | Time To Live |
| UI | User Interface |
| UUID | Universally Unique Identifier |
| VPC | Virtual Private Cloud |
| WAF | Web Application Firewall |
| WCU | Write Capacity Unit |
| WIP | Work In Progress |
