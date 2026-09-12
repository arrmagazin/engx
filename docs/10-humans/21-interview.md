---
type: Guide
title: Interview Technique
description: The cloud-agnostic layer of interview prep — STAR structure, diagram narration, trade-off answers, and a final checklist.
tags: [interview, career, communication]
---

# Interview Technique

The parts of interview preparation that do not change with the technology: how you shape a story, how you narrate a diagram, and how you answer a question whose honest answer is "it depends". The cloud guides link here rather than repeating it, and [System Design Loop](#system-design-loop) covers the design half of a loop.

## Behavioral Stories (STAR)

Interviewers mix conceptual questions with "tell me about a time you...". Prepare 2–3 stories per competency area. Reuse the same project across areas — one substantial migration can supply four different stories depending on which angle you emphasize.

Also prepare the two that come up regardless of role: **a failure you caused** (own it, show the systemic fix — not "I worked too hard") and **a disagreement with a colleague** (show you changed your mind on evidence, or escalated cleanly).

For a cloud or platform role, four decisions come up often enough to be worth a rehearsed answer — a first-party infrastructure language against Terraform, managed Kubernetes against a serverless container service, configuration management against baked images, and scaling a relational database up against out. All four are stated cloud-neutrally in [Cross-Cloud Trade-Offs](../07-clouds/03-trade-offs.md#the-same-decision-in-three-vocabularies).

### The Format

| Part | What Goes Here | Time |
| --- | --- | --- |
| **Situation** | Context, scale, and constraints, with numbers | ~15s |
| **Task** | What *you* specifically owned | ~10s |
| **Action** | Decisions and trade-offs, not a task list; the bulk of the answer | ~60s |
| **Result** | Measured outcome, plus what you would do differently | ~20s |

Two rules that separate a strong story from a weak one:

- **"We" is a red flag.** Say "I" for your decisions, "we" only for team context.
- **Quantify the Result.** "Deploys went from 4 hours to 12 minutes" beats "deploys got much faster."

## Diagrams You Should Be Able to Sketch

Expect "can you draw how that would look?" on a whiteboard or shared doc. Practice the ones your cloud guide lists until you can draw each in ~3 minutes while talking. **Narrate the order you draw in** — it demonstrates how you decompose a problem.

## Trade-Offs

Definitions get you a pass; trade-offs get you the offer. The pattern:

> **"It depends on three things: [A], [B], [C]. If [A], I'd pick X — because [reason]. Where I'd flip to Y is [specific condition]."**

Never answer "which is better?" without naming the deciding variable. Also be willing to say "we chose X and it was the wrong call, here's what we learned."

### Three Phrases That Read as Senior

- *"I'd want to know X before answering"* — then answer both branches. Better than guessing.
- *"We chose X and it was wrong, because we underestimated Y."* — one of these, ready to go.
- *"The technical answer is X, but the organizational answer is Y."* — shows you've operated the thing, not just built it.

## System Design Loop

A framework that applies to any system design question, and the signals that separate a senior or staff answer from a mid-level one.

The worked problems it draws on live in [Canonical Systems](../03-system-design/08-canonical-systems.md), which covers eleven of them, each filed under the bottleneck it tests.

Interviewers care less about whether you know the buzzwords and more about:

1. **Justified assumptions** — every number (scale, storage, ratios) should be defensible, not pulled from thin air.
2. **Generating options before picking one** — for any key decision, name 2-3 alternatives and explain the tradeoff rather than stating your first idea.
3. **Recognizing the *actual* hard problem** — different systems have different bottlenecks (write-heavy vs. read-heavy, strong vs. eventual consistency, connection-state vs. stateless). Reflexively reapplying the same pattern to every problem is a mid-level tell.
4. **Naming failure modes and cross-cutting concerns unprompted** — cache stampedes, hot shards, clock skew, idempotency, moderation, and cost.

Work these six steps in order, whatever the problem.

1. **Requirements** — functional and non-functional, stating explicitly what is out of scope.
2. **Scale estimates** — traffic (reads/writes per sec), storage growth, and which ratio (read:write) dominates. Sanity-check against real-world reference points.
3. **High-level architecture** — draw the boxes: clients, load balancer, services, cache, DB, and async pipeline.
4. **Data model and sharding** — what is the shard key, and why does it match the dominant query pattern?
5. **Deep dives** — 2-4 of the *actually hard* parts, since not everything deserves equal depth.
6. **Cross-cutting concerns** — failure modes, caching, consistency tradeoffs, and cost, named without being asked.

## Prep to Prioritize With Limited Time

1. **Interactive mock mode** on 2-3 of the [canonical systems](../03-system-design/08-canonical-systems.md) — ideally the payment/booking system (biggest mindset gap vs. the read-heavy platforms) and whichever else feels shakiest. Reading is passive; the interview tests whether you can *generate* this reasoning live under mild pressure.
2. Practice **defending your own scale estimates out loud** before being challenged on them — catching an unrealistic number yourself is a stronger signal than being corrected.
3. For each problem, practice stating **2-3 options before picking one** on the key decision (fan-out strategy, consistency model, sharding key) — this is the single biggest lever separating mid-level from senior/staff performance.
