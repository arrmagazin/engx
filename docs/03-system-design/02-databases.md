---
type: Guide
title: Databases — Core Concepts
description: Covers relational and document database vocabulary, ACID and isolation levels, concurrency control, indexing, scaling, and migrations.
tags: [tech-stack, databases, sql]
---

The guarantees a transaction gives, how a schema stays fast and correct, and what breaks first when the data outgrows one machine.

## ACID

- **Atomicity** — a transaction's operations all succeed or all roll back.
- **Consistency** — a transaction moves the database between valid states, respecting constraints.
- **Isolation** — concurrent transactions don't see each other's uncommitted changes; how strictly depends on the isolation level.
- **Durability** — a committed write survives a crash, because it reached the write-ahead log before it was acknowledged.

## Consistency Models

Consistency Model
: The guarantee a system gives about when a write becomes visible to a subsequent read

Eventual Consistency
: Updates propagating asynchronously, so replicas may briefly serve stale data but converge

Strong Consistency
: Every read reflecting the most recent write; required wherever a stale answer is a bug, not a cosmetic issue

Read-Your-Writes Consistency
: Users seeing their own recent writes at once, even while others may not; often the only guarantee a user notices, and cheap: route that user's reads to the primary briefly after a write

Last-Write-Wins (LWW)
: Resolving concurrent writes by keeping the most recent — adequate for counters, lossy for collaborative editing

CAP Theorem
: The result that a system split by a network partition can keep its replicas in agreement or keep answering, but not both; partition tolerance is not optional, because partitions happen anyway

PACELC
: An extension of the CAP Theorem naming the else-case: with no partition, the trade-off is latency against a stronger guarantee — the choice a healthy system makes every day

## Isolation Levels

Each SQL standard level prevents one more anomaly than the one before.

| Level | Prevents | Allows |
| --- | --- | --- |
| **Read uncommitted** | Nothing | Dirty reads (seeing uncommitted writes) |
| **Read committed** | Dirty reads | Non-repeatable reads (a row changes between two reads) |
| **Repeatable read** | Non-repeatable reads | Phantom reads (new rows match a repeated filter) |
| **Serializable** | Phantom reads | Nothing; as if run one at a time — the highest cost |

Engines differ behind the same names (Postgres defaults to read committed, MySQL to repeatable read), so read the engine's documentation. Pick the weakest level correctness allows: higher isolation costs write throughput under contention.

## Transactions and Locking

- **Deadlock** — two transactions each hold a lock the other needs; the database aborts one, and the application must retry.
- **Pessimistic locking** — lock the record before modifying it (`SELECT ... FOR UPDATE`), blocking other writers. Simple and correct, but it costs on every operation and limits throughput when many writers want one record.
- **Optimistic concurrency control** — read a version without a lock, write only if it still matches, and re-read and retry on conflict. The right default when conflicts are rare, since it costs nothing without one; it degrades when contention concentrates on one record and most writers lose.
- **Conditional write** — a write applied only if a condition holds, checked atomically with the write ("only if `version` is still 7"). It replaces "read, decide, write", which two concurrent callers can both pass, and is the usual way to enforce optimistic concurrency, [idempotency](01-common-concepts.md#idempotency), and ordering.

## Schema Design

- **Index** — a structure (usually a B-tree) mapping column values to rows, so lookups avoid a full scan. Every write maintains it, so an unused index costs writes for nothing; check with `EXPLAIN`. A composite index on `(a, b)` serves filters on `a`, or `a` and `b`, but not `b` alone.
- **Normalization** — storing each fact once. **Denormalization** duplicates data on purpose (`customerName` beside `customerId`) to avoid joins on hot reads — a sound choice when reads dominate.
- **N+1 queries** — fetching a list, then one query per row: 50 orders become 51 queries. Fix it with a join or a batched `WHERE id IN (...)`. ORMs and GraphQL resolvers are the usual source, because they hide the extra queries.

## SQL vs. NoSQL

| Aspect | SQL (relational) | NoSQL (document/KV/wide-column) |
| --- | --- | --- |
| **Schema** | Fixed, enforced at write | Flexible, enforced by application (if at all) |
| **Consistency** | Strong (ACID transactions) by default | Often tunable; many default to eventual consistency across replicas |
| **Scaling** | Vertical first; sharding is hard and often manual | Built for horizontal scaling from the start |
| **Fit** | Structured data with invariants to enforce (orders, accounts, inventory) | High write volume, evolving shape, denormalized reads (logs, sessions, catalogs) |

The line is blurring (Postgres has JSONB, MongoDB has multi-document transactions), so choose by access pattern and consistency needs, not the label.

## Scaling a Database

Scale up first; then add **read replicas**, which are usually asynchronous and so may serve stale reads; then a [cache](03-caching.md) for hot reads; and only then shard, because cross-shard joins and transactions become expensive or impossible.

### Sharding

Sharding
: Splitting a dataset across database instances so no single machine holds all of it

Shard Key
: The field deciding which shard a record lives on; chosen to match the dominant query, so common lookups reach one shard — a long-term commitment, since changing it means moving the data

Hash-Based Sharding
: Placing records by a hash of the Shard Key — even load, at the cost of geographic and relational locality

Consistent Hashing
: A placement scheme that relocates only a small fraction of keys when instances are added or removed, unlike `hash % N`

Hot Shard
: One shard or key taking disproportionate traffic and throttling while cluster-wide metrics look healthy; fixed by adding cardinality to the Shard Key, such as a date or a suffix

## Key-Value Store Design

Stores such as DynamoDB and Cassandra have no joins, so design starts from the queries, not the entities.

- **Single-table design** — several entity types share one table, and records sharing a partition key are stored together, so one query returns an order with its history. The key design must be worked out from the access patterns in advance, and written down, because no one can infer it.
- **Sparse index** — an index holding only records that have its key attribute, so "find the few items in this state" queries a small index instead of filtering a scan. A Postgres partial index does the same.
- **Provisioned vs. on-demand capacity** — provisioned for steady high volume; on-demand for spiky or mostly idle traffic, where capacity sized for the peak sits idle.

## Migrations

Version-controlled, incremental schema changes, applied in order so every environment converges on the same schema.

- **Backward compatible during rollout** — old and new code run at once in a rolling deploy, so a rename or drop breaks the old code. Split it across deploys: add the new column → dual-write → backfill → switch reads → drop the old one.
- **Reversible** — each migration has a rollback, even if for a destructive change that means restoring a backup.
