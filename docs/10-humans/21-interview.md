---
type: Guide
title: Interview Technique
description: The cloud-agnostic layer of interview prep — STAR structure, diagram narration, trade-off answers, and a final checklist.
tags: [interview, career, communication]
---

The parts of interview preparation that do not change with the technology: how you shape a story, how you narrate a diagram, and how you answer a question whose honest answer is "it depends". The cloud guides link here instead of repeating it. [System Design Loop](../03-system-design/01-common-concepts.md#system-design-loop) covers the design half of an interview loop.

## Behavioral Stories (STAR)

Interviewers mix conceptual questions with "tell me about a time you...". Prepare 2–3 stories per competency area. Reuse the same project across areas: one substantial migration can supply four different stories, depending on which angle you stress.

Also prepare the two stories that come up in every role:

- **A failure you caused** — own it and show the systemic fix (not "I worked too hard").
- **A disagreement with a colleague** — show you changed your mind on evidence, or escalated cleanly.

For a cloud or platform role, four decisions come up often enough to deserve a rehearsed answer:

- a first-party infrastructure language vs. Terraform;
- managed Kubernetes vs. a serverless container service;
- configuration management vs. baked images;
- scaling a relational database up vs. out.

All four are stated cloud-neutrally in [Cross-Cloud Trade-Offs](../08-clouds/04-trade-offs.md#the-same-decision-in-three-vocabularies).

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

Expect "can you draw how that would look?" on a whiteboard or shared doc. Practice the diagrams your cloud guide lists until you can draw each in ~3 minutes while talking. **Narrate the order you draw in** — it shows how you break down a problem.

## Trade-Offs

Definitions get you a pass; trade-offs get you the offer. The pattern:

> **"It depends on three things: [A], [B], [C]. If [A], I'd pick X — because [reason]. Where I'd flip to Y is [specific condition]."**

Never answer "which is better?" without naming the deciding variable. Also be willing to say "we chose X and it was the wrong call; here's what we learned."

### Three Phrases That Read as Senior

- *"I'd want to know X before answering"* — then answer both branches. Better than guessing.
- *"We chose X and it was wrong, because we underestimated Y."* — one of these, ready to go.
- *"The technical answer is X, but the organizational answer is Y."* — shows you've operated the thing, not just built it.

## Prep to Prioritize With Limited Time

1. **Interactive mock mode** on 2–3 of the [canonical systems](../03-system-design/08-canonical-systems.md) — ideally the payment/booking system (the biggest mindset gap vs. the read-heavy platforms) and whichever else feels weakest. Reading is passive; the interview tests whether you can *generate* this reasoning live, under mild pressure.
2. Practice **defending your own scale estimates out loud** before anyone challenges them. Catching an unrealistic number yourself is a stronger signal than being corrected.
3. For each problem, practice stating **2–3 options before picking one** on the key decision (fan-out strategy, consistency model, sharding key). This is the biggest single lever separating mid-level from senior/staff performance.
