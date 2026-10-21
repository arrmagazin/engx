---
type: Guide
title: Kafka — Core Concepts and Workflow
description: Explains Kafka's core concepts and workflow, delivery semantics, queue patterns, ordering, and where Kafka fits next to other tools.
tags: [tech-stack, kafka, messaging, streaming]
---

Kafka is a durable, partitioned log. Producers append to it and consumers read from it at their own pace, and neither side knows the other. The delivery guarantees and queue patterns below apply to any message broker, not only to Kafka.

## Core Concepts

- **Topic** — a named stream of records (e.g. `orders.created`), split into **partitions**: ordered, append-only logs that are the unit of parallelism and of ordering.
- **Offset** — a record's position in a partition. Consumers track their own offset, and reading removes nothing.
- **Broker** — a Kafka server. Each partition has a leader broker and follower replicas on others.
- **Consumer group** — within a group, each partition goes to exactly one consumer, which gives parallelism and per-partition order. Each further group reads the same topic independently, which is how Kafka serves pub/sub fan-out.
- **Retention** — records stay for a configured time or size (7 days by default), whether consumed or not. This is the core difference from queues such as RabbitMQ and SQS, and what makes replay possible.
- **KRaft** — Kafka's built-in consensus for cluster metadata; ZooKeeper support was removed in 4.0.

## Workflow, End to End

1. The producer hashes the record's key to pick a partition, so one key always keeps its order.
2. The leader appends the record and replicates it; it acknowledges once the configured durability (`acks=0/1/all`) is met.
3. The group coordinator assigns partitions to consumers, rebalancing as they join or leave.
4. Each consumer processes records and commits its offset; a replacement for a crashed consumer resumes from the last commit.

## Delivery Semantics

- **At-least-once delivery** — every message is delivered, possibly more than once. The broker cannot tell "the consumer crashed before processing" from "processed it and crashed before acknowledging", so it must redeliver. Almost every queue offers this guarantee, so idempotent handling is the price of using one, not an optional extra.
- **At-most-once delivery** — never retry; a crash loses the message. Choose it only when a loss costs less than a duplicate, such as a metrics sample.
- **Exactly-once delivery** — impossible at the transport layer: the network can always fail between "processed" and "acknowledged". What can be built is an **exactly-once effect** — at-least-once delivery plus an idempotent consumer — which is what systems advertising exactly-once usually mean.
- **Idempotent consumer** — a handler for which a repeated message changes nothing ([idempotency](01-common-concepts.md#idempotency)), usually keyed on a unique value already in the data, such as an order ID. Two duplicates can arrive *at the same time*, so the check belongs in a [conditional write](02-databases.md#transactions-and-locking), not a read followed by a write.
- **Visibility timeout** — in SQS, a received message is hidden, not deleted, until the consumer deletes it; if the consumer crashes, it reappears. The timeout must exceed the worker's own timeout, or the job runs twice at once.
- **Partial batch failure** — a consumer reports *which* items in a batch failed; without it, one bad message sends the whole batch back, and healthy messages climb toward the dead-letter queue with it.

## Queue Patterns

- **Competing consumers** — several workers take different messages from one queue. This is how a queue scales out, and why it cannot promise order across the whole stream.
- **Back-pressure** — a signal telling a producer to slow down. A bounded queue applies it; an unbounded one only delays the problem, which then surfaces far from its cause as memory, latency, or cost.
- **Dead-letter queue (DLQ)** — a separate queue for messages that failed too many times, such as a malformed *poison message*, so it stops holding a consumer slot. A DLQ that stops being empty is an alert worth waking someone for.
- **Fan-out through a broker** — one event delivered to many consumers ([fan-out](01-common-concepts.md#fan-out)) that the producer does not know, so adding one changes nothing in the producer.
- **Event-carried state transfer** — putting the data a consumer needs *inside* the event, not an ID to call back for. It removes a synchronous dependency, at the cost of a larger payload that may be stale.
- **Transactional outbox** — writing the event to the *same database, in the same transaction* as the state change, and publishing it from there. It solves the dual write: writing to the database and then to a broker leaves them out of step if the process crashes between the calls, in either order.
- **Eventual consistency in consumers** — state updated from events lags the write that caused it, so decide per read path whether that is acceptable; see [Consistency Models](02-databases.md#consistency-models).

## Ordering

- **Kafka** — order holds **within a partition only**. For strict order per entity, key by that entity (e.g. `orderId`).
- **Queues** — standard SQS queues do not keep order. FIFO queues keep it per message group, at a throughput cost and with head-of-line blocking.
- **Order where the state lives** — a queue orders only *delivery*: a retry of message 1 can still land after message 2. A system that depends on order must enforce it where the state is stored, for example with a per-entity sequence number checked in a conditional write.

## Where It Fits

- **Kafka vs. Redis** — Redis Pub/Sub is fire-and-forget ([Pub/Sub vs. Streams](03-caching.md#pubsub-vs-streams)); Kafka is a durable, replayable log for event sourcing, audit trails, and cross-service backbones.
- **Kafka vs. a workflow engine such as Temporal** — complementary: Kafka moves events between systems; a workflow engine runs long, stateful processes with retries and timers.
