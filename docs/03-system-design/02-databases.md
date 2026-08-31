---
type: Guide
title: Databases — Core Concepts
description: Covers relational and document database vocabulary, ACID and isolation levels, indexing, normalization, scaling, and migrations.
tags: [tech-stack, databases, sql]
---

# Databases — Core Concepts

A working vocabulary for relational and document databases: what the pieces are called, what guarantees a transaction gives, how a schema is kept honest, and what breaks first when the data outgrows one machine.

## Core Concepts

- **Table / collection** — a set of records with a shared shape (rigid schema in SQL, flexible/per-document in NoSQL).
- **Row / document** — one record.
- **Primary key** — uniquely identifies a row; every other reference to that row goes through it.
- **Foreign key** — a column referencing another table's primary key; enforces that the referenced row exists (referential integrity).
- **Index** — an auxiliary structure (usually a B-tree) that maps column values to row locations, so lookups avoid a full table scan. Speeds up reads, costs write throughput and storage — every insert/update maintains the index too.
- **Schema** — the shape of the data (columns, types, constraints). SQL enforces it at write time; document stores enforce it at the application layer, if at all.
- **Transaction** — a group of operations that commit or roll back as a unit.
- **Query planner/optimizer** — decides how to execute a query (which index to use, join order) based on statistics about the data.

## ACID

- **Atomicity** — a transaction's operations all succeed or all roll back; no partial writes.
- **Consistency** — a transaction moves the database from one valid state to another, respecting constraints (unique, foreign key, check).
- **Isolation** — concurrent transactions don't see each other's uncommitted changes. Enforced with varying strictness — see isolation levels below.
- **Durability** — once committed, a write survives a crash (written to disk / WAL before acknowledging).


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

## Isolation Levels

The four levels below are defined by the SQL standard, in order of increasing strictness: each prevents everything the one before it prevents, plus one more anomaly.

| Level | Prevents | Allows |
| --- | --- | --- |
| **Read uncommitted** | Nothing | Dirty reads (seeing another transaction's uncommitted writes) |
| **Read committed** | Dirty reads | Non-repeatable reads (same query, different result, within one transaction) |
| **Repeatable read** | Dirty and non-repeatable reads | Phantom reads (new rows matching a filter appear on re-query) |
| **Serializable** | All of the above | Transactions behave as if run one at a time — the highest cost |

Engines do not implement these names identically. Most default to **read committed** (Postgres, Oracle) or **repeatable read** (MySQL/InnoDB); Postgres implements `REPEATABLE READ` as snapshot isolation, and InnoDB's consistent non-locking reads prevent phantoms that the standard permits at that level. Read the engine's documentation rather than the level's name. Higher isolation reduces write throughput under contention, so pick the weakest level the application's correctness actually requires.

## Normalization

Splitting data to eliminate redundancy, so each fact is stored once.

- **1NF** — atomic columns, no repeating groups (no comma-separated lists in a cell).
- **2NF** — no partial dependency on part of a composite key.
- **3NF** — no dependency on non-key columns (a column shouldn't depend on another non-key column).

**Denormalization** — deliberately duplicating data (e.g. storing a `customerName` alongside `customerId`) to avoid joins on hot read paths. Trades write complexity/storage for read speed — a deliberate choice, not a mistake, when read volume dominates.

## Indexing in Practice

- An index speeds up `WHERE`, `JOIN`, and `ORDER BY` on the indexed column(s), at the cost of slower writes and extra storage.
- A **composite index** on `(a, b)` serves queries filtering on `a` alone or on `a` and `b` together, but not on `b` alone — column order matters.
- An index that isn't used by the query planner (e.g. wrapping the column in a function, or the table being too small to bother) costs writes and storage and returns nothing — verify with `EXPLAIN`.
- Unique indexes double as constraints (enforce no duplicates) as well as speeding up lookups.

## Transactions and Locking

- A transaction's isolation level determines what locks (or MVCC snapshot rules) it takes on read/write.
- **Deadlock** — two transactions each hold a lock the other needs; the database detects the cycle and aborts one. Application code must retry.
- **Optimistic vs. pessimistic concurrency** — pessimistic takes a lock upfront (`SELECT ... FOR UPDATE`); optimistic reads without locking and checks a version/timestamp at write time, retrying on conflict.

## SQL vs. NoSQL

| Aspect | SQL (relational) | NoSQL (document/KV/wide-column) |
| --- | --- | --- |
| **Schema** | Fixed, enforced at write | Flexible, enforced by application (if at all) |
| **Relationships** | Joins across normalized tables | Usually denormalized/embedded to avoid joins |
| **Consistency** | Strong (ACID transactions) by default | Often tunable; many default to eventual consistency across replicas |
| **Scaling** | Vertical first; horizontal (sharding) is hard and often manual | Built for horizontal scaling from the start |
| **Fit** | Structured data with relationships and invariants to enforce (orders, accounts, inventory) | High write volume, flexible/evolving shape, denormalized read patterns (logs, sessions, catalogs) |

The distinction is no longer clean: Postgres has JSONB columns for schema-flexible data, and MongoDB supports multi-document ACID transactions. Choose based on the dominant access pattern and consistency needs, not the label.

## Scaling a Database

- **Vertical scaling** — bigger machine (more CPU/RAM/disk). Simple, has a ceiling.
- **Read replicas** — copies of the primary that serve reads, replicated asynchronously (usually). Scales read throughput; replicas can lag, so reads from them may be stale.
- **Sharding / partitioning** — splitting data across multiple database instances by key range or hash. Scales writes, but cross-shard joins/transactions become expensive or impossible — the shard key choice is a long-term commitment.
- **Caching in front of the database** (Redis, etc.) — reduces load for hot reads; introduces cache-invalidation problems.

### Sharding

| Concept | Definition |
|---|---|
| **Sharding** | Splitting a dataset across database instances so no single machine holds all of it |
| **Shard Key** | The field deciding which shard a record lives on; chosen to match the dominant query so common lookups reach one shard |
| **Hash-Based Sharding** | Placing records by a hash of the shard key — even load, at the cost of geographic and relational locality |
| **Consistent Hashing** | A placement scheme that relocates only a small fraction of keys when instances are added or removed, unlike `hash % N` |
| **Region-Based Sharding** | Partitioning by geography rather than by hash, used where queries are inherently local |
| **Hot Shard** | One shard or key taking disproportionate traffic, unbalancing a cluster that is otherwise evenly partitioned |

## Data semantics

**Conditional write** — A write that the database applies only if a condition
holds, evaluated atomically with the write itself. It is the difference between
"read, decide, write" — which two concurrent callers can both pass — and a
single operation the database serialises. In this scaffold both idempotency and
ordering are enforced this way, because both are decisions that must be made at
the moment of writing, not a moment before.

**Hot partition** — A single storage partition receiving far more traffic than
its siblings, throttling even though the table as a whole is far below its
limits. It is caused by low cardinality in the partition key, and it is
especially nasty because aggregate dashboards look healthy while individual
requests fail. The fix is always to add cardinality — a date, a shard suffix —
to the key. 

**Item collection** — All the items in a DynamoDB table sharing one partition
key. It is the unit that single-table design exploits: because a query on a
partition key returns the whole collection, storing a parcel's current state and
its scan events under the same key means one round trip returns both. It is also
the unit that has a size limit when a local secondary index exists, which is one
reason to prefer a GSI.

**Optimistic concurrency** — Allowing concurrent writers to proceed and
detecting the conflict at write time, usually with a version number that the
write requires to be unchanged. It is the right default when conflicts are rare,
because it costs nothing when there is no conflict — unlike a lock, which costs
on every operation. The loser of a conflict must re-read and retry, so the
caller needs a plan for that.

**Projection** — Which attributes an index copies from the base table. It is a
direct trade: `ALL` makes the index self-sufficient but doubles the write cost of
every item, `KEYS_ONLY` is cheapest but forces a second read for anything beyond
the keys, and `INCLUDE` sits between them. The decision belongs to the query the
index exists to serve, not to convenience.

**Provisioned vs on-demand capacity** — Provisioned means declaring RCU and WCU
in advance and paying for them whether used or not; on-demand means paying per
request at a higher unit price. On-demand wins for spiky or unknown traffic and
for anything that idles, because provisioned capacity sized for the peak is idle
capacity most of the time. Provisioned wins at steady high volume, where the
unit price difference outweighs the waste — roughly, if utilisation is
consistently above half.

**Single-table design** — Putting multiple entity types in one DynamoDB table so
that a single query returns a whole object graph. It exists because DynamoDB has
no joins: the alternative is several round trips the application stitches
together. The cost is a key design that must be worked out in advance from the
access patterns, and a table that is unreadable without knowing that design —
which is why it is written down rather than inferred.

**Sparse index** — An index that only contains items which have its key
attribute, because DynamoDB simply omits the rest. It turns "find the few items
in this state" into a query over a tiny index rather than a scan with a filter,
and it costs nothing to maintain for the items that do not qualify. Writing the
attribute becomes the act of adding to the index, and removing it becomes the
act of deleting.

**Strongly vs eventually consistent read** — A strongly consistent read returns
the most recent committed write; an eventually consistent read may return a
slightly stale value, costs half as much, and is the default. Global secondary
indexes offer *only* eventual consistency, which is not a setting but a
consequence of the index being maintained asynchronously. The practical question
is never "which is better" but "would a stale answer here be wrong, or just
old".

## N+1 Queries

Fetching a list, then issuing one additional query per row to fetch related data (e.g. loading 50 orders, then querying each order's customer separately) — 1 query becomes 51. Fix by joining, or by batching the related fetch (`WHERE id IN (...)`) instead of looping. ORMs are the most common source of this, since the extra queries are hidden behind attribute access.

## Migrations

Version-controlled, incremental changes to schema (and sometimes data), applied in order and tracked so every environment converges on the same schema. Two properties matter for production systems:

- **Backward compatibility during rollout** — if old and new application code run simultaneously (rolling deploy), a migration that drops or renames a column breaks the old code. Split into additive-then-cleanup steps (add new column → dual-write → backfill → switch reads → drop old column) across separate deploys.
- **Reversibility** — a migration should have a corresponding rollback, even if "rollback" for a destructive change (dropped column) means restoring from backup rather than an automated `down` migration.
