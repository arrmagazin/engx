---
type: Guide
title: Growing and Keeping People
description: The recurring practice of people management — 1:1s, feedback and performance, the growth levers, and the health signals.
tags: [people, management, feedback, growth, team-health]
---

# Growing and Keeping People

This is the part of the job that repeats every week. The structure in [Roles and the Employee Lifecycle](02-roles-and-lifecycle.md) decides who is accountable for whom; this guide covers what that accountability actually consists of — the private channel where problems surface, the feedback that keeps expectations honest, the assignments that raise what someone can handle alone, and the signals that say whether the current pace can continue.

Related: [Engineering Management](../01-methodology/06-engineering-management.md) · [Team Lead](01-team-lead.md) · [Development Process](../04-development-process/00-development-process.md)

## Core Concepts

| Concept | Definition |
| --- | --- |
| **Expectation** | The observable behavior and output level a person is accountable for, at their level<br>*An expectation nobody has stated cannot be missed — only resented* |
| **Feedback** | An observation about specific behavior and its effect, delivered close in time to the behavior<br>*It describes what happened; judgement of the person is a different thing* |
| **Growth** | A durable increase in the scope a person can handle without supervision |
| **Autonomy Level** | How much decision authority a person holds in one specific area; the delegation ladder in [Team Lead](01-team-lead.md#delegation) grades it<br>*Per-area, not per-person — a staff engineer can be trusted with architecture and still need support in incident command* |
| **Motivation** | The internal driver that makes discretionary effort available — commonly autonomy, mastery, and purpose<br>*Managers cannot supply it; they can remove what destroys it* |
| **Psychological Safety** | The shared belief that raising a problem, an error, or a dissenting view carries no personal cost<br>*The measurable signal is whether bad news travels upward early; if it only arrives at the deadline, safety is absent* |
| **Retention Risk** | The probability a person leaves within a period, weighted by the cost of replacing them |
| **Bus Factor** | The number of people who must become unavailable before a system or process stalls<br>*A bus factor of 1 is a delivery risk recorded as a people problem* |

## 1:1s

The single highest-leverage recurring activity in people management.

| Property | Default |
| --- | --- |
| Frequency | Weekly, or bi-weekly for senior and stable reports |
| Length | 30 minutes |
| Agenda owner | The report — the manager brings a backup agenda |
| Cancellation | Reschedule, never cancel |
| Record | Shared running notes with actions and owners |

**It is not a status meeting.** Status belongs on the board. Use the time for friction, growth, feedback, and things not said in public channels.

A rotating focus keeps it from decaying into small talk:

| Week | Focus |
| --- | --- |
| 1 | What is blocked or frustrating right now |
| 2 | Feedback both directions |
| 3 | Growth and career direction |
| 4 | Team, process, and how the manager can do better |

## Feedback and Performance

Feedback is continuous; reviews only summarize it.

| Type | Timing | Setting |
| --- | --- | --- |
| **Reinforcing** | Immediately | Public, when the person is comfortable with it |
| **Corrective** | Within a day or two | Private, always |
| **Developmental** | 1:1s, ongoing | Private, tied to the next level's expectations |
| **Formal review** | Per cycle | Written, no new information |

Use **Situation → Behavior → Impact**, then agree on the change. Skip the "compliment sandwich" — it obscures the message and teaches people to distrust praise.

### Handling Underperformance

Address it early and explicitly; ambiguity is unkind to everyone.

1. **Name the gap** — specific expectation, specific observed behavior, specific difference.
2. **Rule out the system first** — unclear expectations, missing context, wrong task fit, a personal situation, or a broken process each produce the same visible symptoms as lack of ability, and each is cheaper to fix.
3. **Agree a written plan** — what changes, by when, how it will be measured.
4. **Support and check in** — weekly, with written evidence either way.
5. **Decide** — improved, reassigned, or exited. Do not let step 4 run indefinitely.

**Nothing in a formal review should ever be a surprise.** If it is, the manager failed at step 1, not the report.

## Growth

Growth is assigned, not granted. A person grows by doing work slightly above their current level with a safety net.

| Lever | How to use it |
| --- | --- |
| **Stretch assignment** | Give the next level's scope now; review more closely, not less often |
| **Ownership** | Hand over a system, a ritual, or an area end to end |
| **Pairing and review** | Deliberate pairing across skill gaps; reviews as teaching, not gatekeeping |
| **Teaching** | Have them explain, document, or onboard someone — it forces mastery |
| **External input** | Conferences, courses, open source — the weakest lever, so do not rely on it alone |

Handing over an area raises someone's Autonomy Level, so grade the handover deliberately rather than by mood; the five levels and the instruction that goes with each are in [Delegation](01-team-lead.md#delegation).

Write down the target level's expectations and the evidence gathered so far. A promotion case assembled the week it is needed is a case that fails.

**Promotion follows demonstrated scope.** Promote for what someone is already doing, not for what they might do.

## Team Health

Health metrics **lead** delivery metrics — they degrade first, and they are the early warning for the DORA and flow numbers in [Engineering Management](../01-methodology/06-engineering-management.md#metrics).

| Signal | What it reveals | Watch for |
| --- | --- | --- |
| **Attrition (regretted)** | Whether good people want to stay | Any cluster in one team or one manager |
| **On-call load** | Operational burden per person | Pages outside hours; the same name every time |
| **Unplanned-work share** | Whether commitments are realistic | Sustained above the reserve |
| **Working hours pattern** | Sustainability | Late-night and weekend commits becoming normal |
| **Bus factor per system** | Concentration risk | Any system at 1 |
| **1:1 sentiment** | Everything the metrics miss | Energy dropping over consecutive weeks |
| **Time to first contribution** | Onboarding quality | Trending up as the team grows |

Read these as properties of the system rather than as scores for the people in it — the reasoning, and what happens when individual output is measured instead, is in [Metrics](../01-methodology/06-engineering-management.md#metrics).

## Best Practices

- **Hold the 1:1.** A canceled 1:1 says the person is lower priority than whatever replaced it.
- **State expectations in writing.** Level, scope, and what "good" looks like — before the work, not during the review.
- **Give feedback within days.** Feedback delayed to the review cycle is a complaint, not feedback.
- **Let people fail safely.** Reversible mistakes are the cheapest training available.
- **Rotate the unglamorous work.** On-call, support, and release duty go to everyone, including the seniors.
- **Fix the system before blaming the person.** When the same failure keeps repeating, look for the process that allows it before concluding the person is the problem.
- **Grow a successor.** If you cannot take two weeks off, you have a bus-factor problem of your own.
- **Protect focus time.** Deep work is the job; meetings are overhead that must justify itself.

Two more apply to people work without being specific to it, and are each stated once elsewhere: delegate the outcome rather than the steps, under [Delegation](01-team-lead.md#delegation), and raise bad news early enough for it to still be a decision, under [Best Practices](../01-methodology/06-engineering-management.md#best-practices).

## Anti-patterns

| Anti-pattern | Why it fails | Correction |
| --- | --- | --- |
| Cancelling 1:1s when busy | Signals the person is optional; problems surface later and bigger | Reschedule within the same week |
| 1:1 as status update | Duplicates the board, wastes the only private channel | Status on the board; 1:1 for friction and growth |
| Saving feedback for review season | Removes the chance to correct course | Continuous feedback; reviews summarize only |
| Vague underperformance handling | Unfair to the person and to the team carrying them | Name the gap, write a plan, set a date |
| Treating retention as an HR problem | The causes are manager, work, and growth | Manager owns retention risk per person |

Two failure modes that show up as people problems are cataloged with the delivery ones in [Anti-Patterns](../01-methodology/06-engineering-management.md#anti-patterns): hero culture, and managing individuals by metrics.

## Checklists

**Weekly:**

- [ ] Every 1:1 held, not canceled
- [ ] Feedback given on at least one specific thing observed this week
- [ ] Blocked people have an owner and a next action
- [ ] New joiners checked in on separately

**Per cycle:**

- [ ] Growth plans reviewed against evidence collected
- [ ] Health signals reviewed — on-call, unplanned work, hours pattern
- [ ] Bus factor checked for systems that changed hands
- [ ] Retro actions about people and process actually done
