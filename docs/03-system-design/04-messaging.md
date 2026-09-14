---
type: Guide
title: Kafka — Core Concepts and Workflow
description: Explains Kafka's core concepts, end-to-end workflow, delivery semantics, and how it compares to Redis and Temporal.
tags: [tech-stack, kafka, messaging, streaming]
---

Kafka is a durable, partitioned log that producers append to and consumers read from at their own pace, without either side knowing the other. This guide covers the vocabulary, the path a record takes end to end, the delivery guarantees on offer, and where Kafka sits next to Redis and Temporal.

## Core Concepts

- **Topic** — named stream of records (e.g. `orders.created`). Logical category, not a queue.
- **Partition** — a topic is split into ordered, immutable, append-only logs. This is how Kafka scales horizontally and parallelizes consumption.
- **Offset** — each record in a partition gets a monotonically increasing ID. Consumers track their own position; Kafka is pull-based and non-destructive (reads don't remove data).
- **Broker** — a Kafka server. A cluster is many brokers; each partition has one leader broker plus N follower replicas.
- **Producer** — writes records to a topic, targeting a partition (via key hash, round-robin, or custom partitioner).
- **Consumer / consumer group** — consumers pull records. Within a group, each partition is assigned to exactly one consumer (parallelism + per-partition ordering). Multiple groups can independently read the same topic (pub/sub fan-out).
- **Replication factor** — copies of each partition across brokers for fault tolerance.
- **Retention** — records persist for a configured time/size window regardless of consumption (default 7 days) — the core difference from queue systems like RabbitMQ/SQS.
- **KRaft** — Kafka's own Raft-based consensus for cluster metadata, replacing ZooKeeper. Shipped as a preview in 2.8, declared production-ready in 3.3, and the only option from 4.0, which removed ZooKeeper support entirely.

## Workflow, End to End

1. Producer serializes a record (key + value + headers) and picks a partition — usually by hashing the key, so the same key always lands on the same partition (per-key ordering).
2. Record is appended to the leader partition's log; followers replicate it.
3. Broker acks the write once it meets the configured durability level (`acks=0/1/all`).
4. Consumer group coordinator assigns partitions to consumers (rebalance on join/leave).
5. Each consumer polls its assigned partitions, processes records, and commits its offset (auto or manual) — this commit marks progress, independent of the data itself.
6. On consumer crash, its partitions are reassigned; the new owner resumes from the last committed offset.

## Delivery Semantics

**At-least-once delivery** — The guarantee that a message will be delivered, and
the admission that it may be delivered more than once. It falls out of how
acknowledgement works: the broker cannot distinguish "the consumer crashed
before processing" from "the consumer processed it and crashed before
acknowledging", so it must redeliver. Every practical queue offers this, which
is why idempotency is not an optional refinement but the price of using one.

**At-most-once delivery** — Deliver, and do not retry. A crash between delivery
and processing loses the message permanently. It is the right choice only when
losing an item is cheaper than handling it twice — a metrics sample, a cache
warm — and almost never right for anything a customer paid for.

**Exactly-once delivery** — Does not exist at the transport layer, and claiming
it usually means somebody has moved the problem without solving it. The network
can always fail in the window between "processed" and "acknowledged", so the
sender cannot know which side of that window the receiver died on. What is
achievable is **exactly-once *effect*** — at-least-once delivery plus an
idempotent consumer, so duplicates land on the same state. Systems advertising
exactly-once are doing this internally and calling it a delivery guarantee.

**Back-pressure** — The signal that flows *backwards* from an overloaded
consumer to its producer, telling it to slow down. Without it, a fast producer
and a slow consumer produce an unbounded queue, and the failure surfaces far
from its cause — as memory exhaustion, as latency, as a bill. A queue with a
bounded depth applies back-pressure; a queue with unlimited depth converts a
throughput problem into a much later, much worse one.

**Competing consumers** — Several workers reading from one queue, each taking
different messages. It is how a queue scales horizontally, and it is *why* a
queue cannot promise ordering across the whole stream: two consumers working
concurrently will finish in whatever order they finish. Ordering and this
pattern are in direct tension, which is the trade FIFO queues make explicit.

**Dead letter queue** — A separate queue that receives messages which failed
processing too many times. Its purpose is not storage but *isolation*: without
it, one message that can never succeed retries forever, consuming the consumer's
capacity and hiding healthy traffic behind it. The DLQ turning non-empty is one
of the few alerts that is almost always worth waking someone for, because it
means a message was accepted and then permanently could not be handled.

**Event-carried state transfer** — Putting the data a consumer needs *inside*
the event, rather than an identifier the consumer must call back to resolve.
It removes a synchronous dependency — the consumer no longer needs the producer
to be up — at the cost of a larger payload and a snapshot that may be stale by
the time it is read. The alternative, a thin event plus a callback, keeps events
small and reintroduces exactly the coupling the queue was meant to break.

**Eventual consistency** — A guarantee that replicas will converge, with no
promise about when. It is what you accept in exchange for availability during a
network partition, which is the trade the CAP theorem describes. The practical
consequence is not philosophical: a user who writes and then immediately reads
may not see their own write, and the design has to decide whether that is
acceptable or whether it needs a strongly consistent read.

**Fan-out** — One event, many independent consumers. The reason to do it through
a broker rather than by having the producer call each consumer is that the
producer then does not need to know they exist — adding a subscriber becomes a
change in one place instead of a deployment of the producer. SNS fans out to
known subscribers; EventBridge fans out through rules that match on content.

**Idempotency** — The property that applying an operation twice leaves the same
state as applying it once. It is what makes at-least-once delivery survivable,
and the cheapest way to get it is usually a natural unique key already present
in the data — here, `scanId` — rather than a separate deduplication store. The
subtle part is that idempotency must hold for *concurrent* duplicates too, which
is why it belongs in a conditional write rather than a read-then-write check.

**Message ordering** — The promise that messages are processed in the order they
were sent. Standard queues do not offer it; FIFO queues offer it per message
group, at a throughput cost and with head-of-line blocking. The important
insight is that a queue can only order *delivery* — a retry of message 1 can
still land after message 2 — so any system that truly depends on order must
enforce it where the state lives, not where the messages travel.

**Partial batch failure** — When a consumer is handed a batch and only some
items fail, reporting *which* ones failed rather than failing the batch. Without
it, one bad message in a batch of ten forces all ten to be redelivered, so nine
successful items are processed again and the poison message's retry count climbs
ten times slower. In SQS-triggered Lambda this is the `ReportBatchItemFailures`
response type, and it is off by default.

**Poison message** — A message that will never succeed no matter how many times
it is retried, usually because it is malformed or references something that no
longer exists. It is dangerous out of proportion to its size: retried forever,
it occupies a consumer slot permanently. The DLQ plus a maximum receive count is
the standard containment.

**Transactional outbox** — Writing the event to the *same database, in the same
transaction* as the state change, and having a separate process publish it from
there. It solves the dual-write problem: if you write to the database and then
publish to a broker, a crash between the two leaves the two permanently
disagreeing, and there is no ordering of those two calls that fixes it. The cost
is a publisher process and a small delay.

**Visibility timeout** — When a consumer receives an SQS message, the message is
not deleted; it is hidden from other consumers for the visibility timeout. If
the consumer deletes it in time, it is gone; if the consumer crashes, the
message reappears and someone else gets it. This is *why* SQS gives at-least-once
and not exactly-once delivery, and it is why the timeout must exceed the worker's
own timeout — otherwise the message reappears while the first consumer is still
working on it and the job runs twice concurrently.

## Ordering

Kafka guarantees order **within a partition only**, not across a topic. For strict ordering of an entity (e.g. all events for one `orderId`), key by that entity so it always maps to the same partition.

## Where It Fits

- **Kafka vs. Redis (pub/sub)** — Redis pub/sub is fire-and-forget, no replay, no persistence. Kafka is a durable, replayable log. Use Redis for ephemeral fan-out/caching, Kafka for event sourcing, audit trails, cross-service event backbones.
- **Kafka vs. Temporal** — different layers. Kafka moves events between systems; Temporal orchestrates long-running, stateful workflows (retries, timers, human-in-the-loop), often triggered by or emitting Kafka events. Complementary, not competing.

## Entities Diagram

```text
Producers (write by key)
      │
      ▼
┌─────────────── Kafka cluster ───────────────┐
│  Topic: orders.created                      │
│  ┌─────────────────┐                        │
│  │ Partition 0      │──┐                    │
│  │ Leader: broker 1 │  │                     │
│  ├─────────────────┤  │                     │
│  │ Partition 1      │──┼──► Consumer group   │
│  │ Leader: broker 2 │  │    (orders-service) │
│  ├─────────────────┤  │    C1 ← Partition 0  │
│  │ Partition 2      │──┘    C2 ← Partition 1  │
│  │ Leader: broker 3 │       C3 ← Partition 2  │
│  └─────────────────┘                        │
└───────────────────────────────────────────────┘
```

A second, independent consumer group could read the same topic from its beginning without affecting this one, which is how Kafka serves pub/sub fan-out.

## Node.js / TypeScript (kafkajs)

```ts
const kafka = new Kafka({ clientId: 'app', brokers: ['broker:9092'] });

const producer = kafka.producer();
await producer.send({
  topic: 'orders.created',
  messages: [{ key: orderId, value: JSON.stringify(payload) }],
});

const consumer = kafka.consumer({ groupId: 'orders-service' });
await consumer.subscribe({ topic: 'orders.created', fromBeginning: false });
await consumer.run({
  eachMessage: async ({ partition, message }) => {
    // process; offset commit is automatic unless autoCommit: false
  },
});
```

Use `eachBatch` for manual offset control when processing needs stronger guarantees than automatic commits give. When slow processing triggers rebalances, the knobs are `sessionTimeout` and `heartbeatInterval` on the consumer — kafkajs names them differently from the Java and librdkafka clients, where they are `session.timeout.ms` and `heartbeat.interval.ms`.
