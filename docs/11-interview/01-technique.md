---
type: Guide
title: Interview Technique
description: The cloud-agnostic layer of interview prep — STAR structure, diagram narration, trade-off answers, and a final checklist.
tags: [interview, career, communication]
---

# Interview Technique

The parts of interview preparation that do not change with the technology: how you shape a story, how you narrate a diagram, and how you answer a question whose honest answer is "it depends". The cloud guides link here rather than repeating it, and [System Design Loop](02-system-design-loop.md) covers the design half of a loop.

## Behavioral Stories (STAR)

Interviewers mix conceptual questions with "tell me about a time you...". Prepare 2–3 stories per competency area. Reuse the same project across areas — one substantial migration can supply four different stories depending on which angle you emphasize.

Also prepare the two that come up regardless of role: **a failure you caused** (own it, show the systemic fix — not "I worked too hard") and **a disagreement with a colleague** (show you changed your mind on evidence, or escalated cleanly).

Worked examples with the numbers filled in, plus a story bank mapped to each cloud's competency areas, live in [AWS Interview Prep](../07-cloud-aws/02-aws-interview-prep.md) and [Azure Interview Prep](../08-cloud-azure/02-azure-interview-prep.md).

### The Format

| Part | What Goes Here | Time |
|---|---|---|
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

## Final Prep Checklist

- [ ] 10 STAR stories written out — 2 per competency area, with numbers in the Result
- [ ] Failure story and disagreement story prepared
- [ ] Can sketch each diagram your cloud guide lists in 3 minutes, talking while drawing
- [ ] Can give that guide's trade-off answers without notes
- [ ] 3–4 questions ready for them (their IaC tool and why; who owns cluster upgrades; how they handle prod access; what broke most recently)
