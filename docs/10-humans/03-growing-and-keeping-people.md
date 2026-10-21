---
type: Guide
title: Growing and Keeping People
description: The recurring practice of people management — 1:1s, feedback and performance, the growth levers, and the health signals.
tags: [people, management, feedback, growth, team-health]
---

This is the part of the job that repeats every week. [Roles and the Employee Lifecycle](02-roles-and-lifecycle.md) decides who is accountable for whom. This guide covers what that accountability consists of:

- the private channel where problems surface;
- the feedback that keeps expectations honest;
- the assignments that raise what someone can handle alone;
- the signals that show whether the current pace can continue.

Related: [Engineering Management](../01-methodology/00-engineering-management.md) · [Team Lead](01-team-lead.md) · [Development Process](../04-development-process/index.md)

## Core Concepts

Expectation
: The observable behavior and output level a person is accountable for, at their level\
  *An expectation nobody has stated cannot be missed — only resented*

Feedback
: An observation about specific behavior and its effect, delivered close in time to the behavior\
  *It describes what happened; judgement of the person is a different thing*

Growth
: A durable increase in the scope a person can handle without supervision

Autonomy Level
: How much decision authority a person holds in one specific area; the delegation ladder in [Team Lead](01-team-lead.md#delegation) grades it\
  *Per-area, not per-person — a staff engineer can be trusted with architecture and still need support in incident command*

Motivation
: The internal driver that makes discretionary effort available — commonly autonomy, mastery, and purpose (Daniel Pink, *Drive*)\
  *Managers cannot supply it; they can remove what destroys it*

Psychological Safety
: The shared belief that raising a problem, an error, or a dissenting view carries no personal cost (a concept from Amy Edmondson's team research)\
  *The measurable signal is whether bad news travels upward early; if it only arrives at the deadline, safety is absent*

Retention Risk
: The probability a person leaves within a period, weighted by the cost of replacing them\
  *Judged only from what the person tells you, never inferred from health, family, age, or another protected trait*

Bus Factor
: The number of people who must become unavailable before a system or process stalls\
  *A bus factor of 1 is a delivery risk recorded as a people problem*

## 1:1s

The recurring activity with the highest leverage in people management.

| Property | Default |
| --- | --- |
| Frequency | Weekly, or bi-weekly for senior and stable reports |
| Length | 30 minutes |
| Agenda owner | The report — the manager brings a backup agenda |
| Cancellation | Reschedule, never cancel |
| Record | Shared running notes with actions and owners; keep health and private details out of them |

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

Use **Situation-Behavior-Impact** (SBI™, a model from the Center for Creative Leadership), then agree on the change. Skip the "compliment sandwich": it hides the message and teaches people to distrust praise.

### Handling Underperformance

Address it early and explicitly; ambiguity is unkind to everyone.

1. **Name the gap** — specific expectation, specific observed behavior, specific difference.
2. **Rule out the system first** — unclear expectations, missing context, wrong task fit, a personal situation, or a broken process. Each produces the same visible symptoms as lack of ability, and each is cheaper to fix.
3. **Agree a written plan** — what changes, by when, how it will be measured.
4. **Support and check in** — weekly, with written evidence either way.
5. **Decide** — improved, reassigned, or exited. Do not let step 4 run indefinitely.

Rules differ by country and contract, so involve HR or legal before a written plan or an exit. A cause linked to health, disability, or pregnancy may call for an accommodation rather than a performance process.

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

Handing over an area raises someone's Autonomy Level, so set the level deliberately, not by mood. The five levels, each with its instruction, are in [Delegation](01-team-lead.md#delegation).

Write down the target level's expectations and the evidence gathered so far. A promotion case put together in the week it is needed fails.

**Promotion follows demonstrated scope.** Promote for what someone is already doing, not for what they might do.

## Team Health

Health metrics **lead** delivery metrics — they degrade first, and they are the early warning for the DORA and flow numbers in [Engineering Management](../01-methodology/00-engineering-management.md#metrics).

| Signal | What it reveals | Watch for |
| --- | --- | --- |
| **Attrition (regretted)** | Whether good people want to stay | Any cluster in one team or one manager |
| **On-call load** | Operational burden per person | Pages outside hours; the same name every time |
| **Unplanned-work share** | Whether commitments are realistic | Sustained above the reserve |
| **Working hours pattern** | Sustainability | Late-night and weekend commits becoming normal across the team — read as a team aggregate only, never per person |
| **Bus factor per system** | Concentration risk | Any system at 1 |
| **1:1 sentiment** | Everything the metrics miss | Energy dropping over consecutive weeks |
| **Time to first contribution** | Onboarding quality | Trending up as the team grows |

Commit and pull request timestamps are employee personal data. In the EU the GDPR applies, and member states may add stricter rules for employment (Art. 88); in Germany, technical monitoring of employees needs the works council's agreement where one exists (BetrVG §87(1) no. 6). Rules differ by country; this is not legal advice.

Read these as properties of the system, not as scores for the people in it. [Metrics](../01-methodology/00-engineering-management.md#metrics) explains why, and what happens when individual output is measured instead.

## Best Practices

- **Hold the 1:1.** A canceled 1:1 says the person is lower priority than whatever replaced it.
- **State expectations in writing.** Level, scope, and what "good" looks like — before the work, not during the review.
- **Give feedback within days.** Feedback delayed to the review cycle is a complaint, not feedback.
- **Let people fail safely.** Reversible mistakes are the cheapest training available.
- **Rotate the unglamorous work.** On-call, support, and release duty go to everyone, including the seniors.
- **Fix the system before blaming the person.** When the same failure keeps repeating, look for the process that allows it before deciding the person is the problem.
- **Grow a successor.** If you cannot take two weeks off, you have a bus-factor problem of your own.
- **Protect focus time.** Deep work is the job; meetings are overhead that must justify itself.

Two more apply to people work but are not specific to it, so each is stated once elsewhere:

- Delegate the outcome, not the steps — [Delegation](01-team-lead.md#delegation).
- Raise bad news early enough that it is still a decision — [Best Practices](../01-methodology/00-engineering-management.md#best-practices).

## Anti-patterns

| Anti-pattern | Why it fails | Correction |
| --- | --- | --- |
| Cancelling 1:1s when busy | Signals the person is optional; problems surface later and bigger | Reschedule within the same week |
| 1:1 as status update | Duplicates the board, wastes the only private channel | Status on the board; 1:1 for friction and growth |
| Saving feedback for review season | Removes the chance to correct course | Continuous feedback; reviews summarize only |
| Vague underperformance handling | Unfair to the person and to the team carrying them | Name the gap, write a plan, set a date |
| Treating retention as an HR problem | The causes are manager, work, and growth | Manager owns retention risk per person, based only on what the person says |

Two failure modes that look like people problems — hero culture, and managing individuals by metrics — are listed with the delivery ones in [Anti-Patterns](../01-methodology/00-engineering-management.md#anti-patterns).

## Checklists

**Weekly:**

- [ ] Every 1:1 held, not canceled
- [ ] Feedback given on at least one specific thing observed this week
- [ ] Blocked people have an owner and a next action
- [ ] New joiners checked in on separately

**Per cycle:**

- [ ] Growth plans reviewed against evidence collected
- [ ] Health signals reviewed — on-call, unplanned work, hours pattern as a team aggregate
- [ ] Bus factor checked for systems that changed hands
- [ ] Retro actions about people and process actually done
