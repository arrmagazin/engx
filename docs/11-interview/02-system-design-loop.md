---
type: Guide
title: System Design Loop
description: The framework to work any system design question, and what senior and staff interviewers weigh in the answer.
tags: [architecture, system-design, interview]
---

# System Design Loop

A framework that applies to any system design question, and the signals that separate a senior or staff answer from a mid-level one. The worked problems it draws on live in [Canonical Systems](../03-system-design/06-canonical-systems.md), which covers eleven of them, each filed under the bottleneck it tests.

## What Interviewers Weigh at Senior and Staff Level

Interviewers at this level care less about whether you know the buzzwords and more about:

1. **Justified assumptions** — every number (scale, storage, ratios) should be defensible, not pulled from thin air.
2. **Generating options before picking one** — for any key decision, name 2-3 alternatives and explain the tradeoff rather than stating your first idea.
3. **Recognizing the *actual* hard problem** — different systems have different bottlenecks (write-heavy vs. read-heavy, strong vs. eventual consistency, connection-state vs. stateless). Reflexively reapplying the same pattern to every problem is a mid-level tell.
4. **Naming failure modes and cross-cutting concerns unprompted** — cache stampedes, hot shards, clock skew, idempotency, moderation, and cost.

## The Standard Framework

Work these six steps in order, whatever the problem.

1. **Requirements** — functional and non-functional, stating explicitly what is out of scope.
2. **Scale estimates** — traffic (reads/writes per sec), storage growth, and which ratio (read:write) dominates. Sanity-check against real-world reference points.
3. **High-level architecture** — draw the boxes: clients, load balancer, services, cache, DB, and async pipeline.
4. **Data model and sharding** — what is the shard key, and why does it match the dominant query pattern?
5. **Deep dives** — 2-4 of the *actually hard* parts, since not everything deserves equal depth.
6. **Cross-cutting concerns** — failure modes, caching, consistency tradeoffs, and cost, named without being asked.

## Prep to Prioritize With Limited Time

1. **Interactive mock mode** on 2-3 of the [canonical systems](../03-system-design/06-canonical-systems.md) — ideally the payment/booking system (biggest mindset gap vs. the read-heavy platforms) and whichever else feels shakiest. Reading is passive; the interview tests whether you can *generate* this reasoning live under mild pressure.
2. Practice **defending your own scale estimates out loud** before being challenged on them — catching an unrealistic number yourself is a stronger signal than being corrected.
3. For each problem, practice stating **2-3 options before picking one** on the key decision (fan-out strategy, consistency model, sharding key) — this is the single biggest lever separating mid-level from senior/staff performance.
