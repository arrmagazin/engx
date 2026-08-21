---
type: Guide
title: System Design Interview Prep (Senior / Staff)
description: Walks through a standard framework and 10 canonical system design problems for senior/staff-level interviews, organized by bottleneck.
tags: [architecture, system-design, interview]
---

# System Design Interview Prep (Senior / Staff)

A comprehensive reference covering 10 canonical system design problems, organized by the *core bottleneck* each one tests. Built for a senior/staff-level interview loop.

At senior/staff level, interviewers care less about "do you know the buzzwords" and more about:

1. **Justified assumptions** — every number (scale, storage, ratios) should be defensible, not pulled from thin air.
2. **Generating options before picking one** — for any key decision, name 2-3 alternatives and explain the tradeoff, don't just state your first idea.
3. **Recognizing the *actual* hard problem** — different systems have fundamentally different bottlenecks (write-heavy vs. read-heavy, strong vs. eventual consistency, connection-state vs. stateless). Reflexively reapplying the same pattern to every problem is a mid-level tell.
4. **Naming failure modes and cross-cutting concerns unprompted** — cache stampedes, hot shards, clock skew, idempotency, moderation, cost.

### The Standard Framework (apply to any problem)

1. **Requirements** — functional + non-functional, explicitly state what's out of scope.
2. **Scale estimates** — traffic (reads/writes per sec), storage growth, and what ratio (read:write) dominates. Sanity-check against real-world reference points.
3. **High-level architecture** — draw the boxes: clients, load balancer, services, cache, DB, async pipeline.
4. **Data model & sharding** — what's the shard key, and why does it match the dominant query pattern?
5. **Deep dives** — 2-4 of the *actually hard* parts (not everything deserves equal depth).
6. **Cross-cutting concerns** — failure modes, caching, consistency tradeoffs, cost — named without being asked.

## Suggested Remaining Prep (with limited time)

1. **Interactive mock mode** on 2-3 of the above — ideally the payment/booking system (biggest mindset gap vs. the read-heavy platforms) and whichever else feels shakiest. Reading is passive; the interview tests whether you can *generate* this reasoning live under mild pressure.
2. Practice **defending your own scale estimates out loud** before being challenged on them — catching an unrealistic number yourself is a stronger signal than being corrected.
3. For each problem, practice stating **2-3 options before picking one** on the key decision (fan-out strategy, consistency model, sharding key) — this is the single biggest lever separating mid-level from senior/staff performance.
