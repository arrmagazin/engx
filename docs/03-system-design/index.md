---
type: Guide
title: System Design
description: Defines system design as the process turning architectural decisions into an implementable specification, and catalogs its components.
tags: [architecture, system-design]
---

**System design** is the *process* that turns architectural decisions into a specification developers can implement directly: database schemas, `API` endpoints, algorithms, data structures, and the components chosen to run them. It works one level below [System Architecture](../02-architecture/index.md), which decides what the parts are and stops there.

```svg
<Panel>
  <Node key="principles" col="0" row="0" label="Principles" />
  <Node key="constraints" col="0" row="1" label="Constraints" />
  <Node key="architecture" col="1" row="0" label="Architecture" />
  <Node key="decisions" col="2" row="0" label="Decisions" />
  <Node key="system-design" col="3" row="0" label="System Design" />
  <Node key="blueprint" col="3" row="1" label="Blueprint" />
  <Node key="implementation" col="2" row="1" label="Implementation" />
  <Node key="measures" col="1" row="1" label="Measures" />
  <Edge from="principles" to="architecture" />
  <Edge from="constraints" to="architecture" />
  <Edge from="architecture" to="decisions" />
  <Edge from="decisions" to="system-design" />
  <Edge from="system-design" to="blueprint" />
  <Edge from="blueprint" to="implementation" />
  <Edge from="implementation" to="measures" />
  <Edge from="measures" to="architecture" />
</Panel>
```

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[System Design Glossary](01-common-concepts.md)** | The vocabulary this chapter uses, grouped by the problem each set of terms addresses |
| **[Databases — Core Concepts](02-databases.md)** | Storage models, consistency, isolation, concurrency control, and sharding |
| **[Caching — Core Concepts](03-caching.md)** | Caching patterns, CDNs, and Redis |
| **[Kafka — Core Concepts and Workflow](04-messaging.md)** | Partitions, consumer groups, delivery guarantees, queue patterns, and ordering |
| **[Containers — Core Concepts and Orchestration](05-containers.md)** | Images, isolation, orchestration, and what containers mean for state |
| **[Client-Server Communication](06-client-server.md)** | Load balancing, HTTP semantics, REST and GraphQL, and streaming transports |
| **[Data Formats](../99-appendices/07-data-formats.md)** | JSON, YAML, XML, CSV, Markdown, and Parquet, and the parsing traps of each |
| **[Canonical Systems](08-canonical-systems.md)** | Eleven worked problems, each filed under the bottleneck it tests |
| **[Abbreviations](../99-appendices/09-abbreviations.md)** | The abbreviations used across this book |

## Information System

Information System
: An artificial system that performs data transformation flows across `Hardware`, `Software`, and the data sources they reach

Component
: A named unit of code or data with a declared interface, replaceable by any other unit honoring that interface without changing its callers

Application
: Deliverable Software providing functional scope in a business domain

Library
: Reusable Component the `Application` *calls*; it owns no control flow, so the `Application` decides when, whether, and in what order it runs

Software Framework
: Component that owns the control flow and *calls* the `Application`'s code through the extension points it defines (*inversion of control*); it dictates structure, so it is chosen once and swapped rarely

API
: The contract a `Component` exposes for others to call — operations, inputs, outputs, and errors — stated independently of how it is implemented; see [Client-Server Communication](06-client-server.md)

Configuration
: Data that *parameterizes* `Software` without changing it — what varies per environment, tenant, or deployment; versioned like code, but applied without rebuilding

This chapter says **Software Framework**, never plain *`Framework`*: [Core concepts](../01-methodology/00-core_concepts.md#how-work-is-run) defines a `Framework` as a Method that offers predefined options to choose from. One is a piece of code; the other is a way of running a process.

## Hardware

Hardware
: Physical *circuit* that transforms and exchanges binary data

Network
: The *fabric* (links, addressing, protocols) that carries data between `Hardware` nodes; it is unreliable by nature, so latency, loss, and partition are design inputs, not edge cases

Virtual Machine (VM)
: *Emulated* Hardware — a hypervisor slices one physical host into several machines, each running its own `Operating System` kernel; the unit of isolation is the machine

## Software

Software
: Executable code, configurations, and metadata defining data processing

Operating System
: Software that manages a machine's `Hardware` and schedules the processes running on it, exposing a stable interface the `Application` is programmed against

Container
: An Application packaged with its userspace dependencies as an immutable *image*, isolated by the host's kernel instead of by emulation; the unit of isolation is the process

## Database

Database
: Component that stores structured data and answers queries over it under transactional guarantees

Data Warehouse
: Database shaped for *analytics*: historical, modeled, read-heavy — schema fixed on write

Data Lake
: Storage of *raw* data in its original form at scale; the schema is applied on read, by whoever consumes it

Object Storage
: Component storing immutable *blobs* (files, media, backups) addressed by key, without structure or query over their content

Cache
: Component holding *derived copies* of data closer to its consumer to trade freshness for speed; never a source of truth — see [Caching](03-caching.md)

Search Index
: Component storing a *query-optimized projection* of data to answer lookups a `Database` cannot serve efficiently

## Service

Service
: Component deployed and operated on its own, reached over the `Network` rather than linked into the `Application`

Message Broker
: Service that transfers data between `Components` *asynchronously*, decoupling producer from consumer in time and availability — see [Kafka](04-messaging.md)

Identity Provider (IdP)
: Service that authenticates *principals* and issues verifiable *claims* about them, so other `Components` authorize instead of authenticate

A `Service` here is a deployed component. [Core concepts](../01-methodology/00-core_concepts.md#how-a-solution-is-made) defines a `Service` as a way of delivering outcomes through ongoing interaction. One runs on a network; the other is how a `Solution` reaches its users.
