# Kafka — core concepts and workflow

## Core concepts

- **Topic** — named stream of records (e.g. `orders.created`). Logical category, not a queue.
- **Partition** — a topic is split into ordered, immutable, append-only logs. This is how Kafka scales horizontally and parallelizes consumption.
- **Offset** — each record in a partition gets a monotonically increasing ID. Consumers track their own position; Kafka is pull-based and non-destructive (reads don't remove data).
- **Broker** — a Kafka server. A cluster is many brokers; each partition has one leader broker plus N follower replicas.
- **Producer** — writes records to a topic, targeting a partition (via key hash, round-robin, or custom partitioner).
- **Consumer / consumer group** — consumers pull records. Within a group, each partition is assigned to exactly one consumer (parallelism + per-partition ordering). Multiple groups can independently read the same topic (pub/sub fan-out).
- **Replication factor** — copies of each partition across brokers for fault tolerance.
- **Retention** — records persist for a configured time/size window regardless of consumption (default 7 days) — the core difference from queue systems like RabbitMQ/SQS.
- **KRaft** — Kafka 3.x+ uses its own Raft-based consensus for cluster metadata, replacing ZooKeeper.

## Workflow, end to end

1. Producer serializes a record (key + value + headers) and picks a partition — usually by hashing the key, so the same key always lands on the same partition (per-key ordering).
2. Record is appended to the leader partition's log; followers replicate it.
3. Broker acks the write once it meets the configured durability level (`acks=0/1/all`).
4. Consumer group coordinator assigns partitions to consumers (rebalance on join/leave).
5. Each consumer polls its assigned partitions, processes records, and commits its offset (auto or manual) — this commit marks progress, independent of the data itself.
6. On consumer crash, its partitions are reassigned; the new owner resumes from the last committed offset.

## Delivery semantics

- **At-most-once** — commit offset before processing; risk losing records on crash.
- **At-least-once** — commit after processing (default/common); risk reprocessing, so downstream must be idempotent.
- **Exactly-once (EOS)** — idempotent producers + transactional writes across topics; used for atomic read-process-write (e.g. Kafka Streams).

## Ordering — the detail people get wrong

Kafka guarantees order **within a partition only**, not across a topic. For strict ordering of an entity (e.g. all events for one `orderId`), key by that entity so it always maps to the same partition.

## Where it fits vs. other tools

- **Kafka vs Redis (pub/sub)** — Redis pub/sub is fire-and-forget, no replay, no persistence. Kafka is a durable, replayable log. Use Redis for ephemeral fan-out/caching, Kafka for event sourcing, audit trails, cross-service event backbones.
- **Kafka vs Temporal** — different layers. Kafka moves events between systems; Temporal orchestrates long-running, stateful workflows (retries, timers, human-in-the-loop), often triggered by or emitting Kafka events. Complementary, not competing.

## Entities diagram

```
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

One consumer group, three consumers, one partition each — parallel processing with per-partition ordering preserved. A second, independent consumer group could read the same topic from scratch (pub/sub fan-out).

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

Use `eachBatch` for manual offset control when you need exactly-once-ish semantics. Tune `heartbeat` / `session.timeout.ms` for operational depth questions.
