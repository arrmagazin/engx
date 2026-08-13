---
type: Guide
title: Databases — core concepts
description: Covers core database concepts, ACID properties, isolation levels, and normalization.
tags: [tech-stack, databases, sql]
---

# Databases — core concepts

## Core concepts

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

## Isolation levels (strongest to weakest guarantee, in practice weakest to strongest below)

| Level | Prevents | Allows |
| --- | --- | --- |
| Read uncommitted | Nothing | Dirty reads (seeing another transaction's uncommitted writes) |
| Read committed | Dirty reads | Non-repeatable reads (same query, different result, within one transaction) |
| Repeatable read | Dirty + non-repeatable reads | Phantom reads (new rows matching a filter appear on re-query) |
| Serializable | All of the above | Transactions behave as if run one at a time — highest cost |

Most databases default to **read committed** (Postgres, Oracle) or **repeatable read** (MySQL/InnoDB). Higher isolation reduces write throughput under contention — pick the weakest level the application's correctness actually requires.

## Normalization

Splitting data to eliminate redundancy, so each fact is stored once.

- **1NF** — atomic columns, no repeating groups (no comma-separated lists in a cell).
- **2NF** — no partial dependency on part of a composite key.
- **3NF** — no dependency on non-key columns (a column shouldn't depend on another non-key column).

**Denormalization** — deliberately duplicating data (e.g. storing a `customerName` alongside `customerId`) to avoid joins on hot read paths. Trades write complexity/storage for read speed — a deliberate choice, not a mistake, when read volume dominates.

## Indexing, in practice

- An index speeds up `WHERE`, `JOIN`, and `ORDER BY` on the indexed column(s), at the cost of slower writes and extra storage.
- A **composite index** on `(a, b)` serves queries filtering on `a` alone or on `a` and `b` together, but not on `b` alone — column order matters.
- An index that isn't used by the query planner (e.g. wrapping the column in a function, or the table being too small to bother) is dead weight — verify with `EXPLAIN`.
- Unique indexes double as constraints (enforce no duplicates) as well as speeding up lookups.

## Transactions and locking

- A transaction's isolation level determines what locks (or MVCC snapshot rules) it takes on read/write.
- **Deadlock** — two transactions each hold a lock the other needs; the database detects the cycle and aborts one. Application code must retry.
- **Optimistic vs pessimistic concurrency** — pessimistic takes a lock upfront (`SELECT ... FOR UPDATE`); optimistic reads without locking and checks a version/timestamp at write time, retrying on conflict.

## SQL vs NoSQL

| | SQL (relational) | NoSQL (document/KV/wide-column) |
| --- | --- | --- |
| Schema | Fixed, enforced at write | Flexible, enforced by application (if at all) |
| Relationships | Joins across normalized tables | Usually denormalized/embedded to avoid joins |
| Consistency | Strong (ACID transactions) by default | Often tunable; many default to eventual consistency across replicas |
| Scaling | Vertical first; horizontal (sharding) is hard and often manual | Built for horizontal scaling from the start |
| Fit | Structured data with relationships and invariants to enforce (orders, accounts, inventory) | High write volume, flexible/evolving shape, denormalized read patterns (logs, sessions, catalogs) |

The line has blurred — Postgres has JSONB columns for schema-flexible data; MongoDB supports multi-document ACID transactions. Choose based on the dominant access pattern and consistency needs, not the label.

## Scaling a database

- **Vertical scaling** — bigger machine (more CPU/RAM/disk). Simple, has a ceiling.
- **Read replicas** — copies of the primary that serve reads, replicated asynchronously (usually). Scales read throughput; replicas can lag, so reads from them may be stale.
- **Sharding / partitioning** — splitting data across multiple database instances by key range or hash. Scales writes, but cross-shard joins/transactions become expensive or impossible — the shard key choice is a long-term commitment.
- **Caching in front of the database** (Redis, etc.) — reduces load for hot reads; introduces cache-invalidation problems.

## N+1 queries — the detail people get wrong

Fetching a list, then issuing one additional query per row to fetch related data (e.g. loading 50 orders, then querying each order's customer separately) — 1 query becomes 51. Fix by joining, or by batching the related fetch (`WHERE id IN (...)`) instead of looping. ORMs are the most common source of this, since the extra queries are hidden behind attribute access.

## Migrations

Version-controlled, incremental changes to schema (and sometimes data), applied in order and tracked so every environment converges on the same schema. Two properties matter for production systems:

- **Backward compatibility during rollout** — if old and new application code run simultaneously (rolling deploy), a migration that drops or renames a column breaks the old code. Split into additive-then-cleanup steps (add new column → dual-write → backfill → switch reads → drop old column) across separate deploys.
- **Reversibility** — a migration should have a corresponding rollback, even if "rollback" for a destructive change (dropped column) means restoring from backup rather than an automated `down` migration.
