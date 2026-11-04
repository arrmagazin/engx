---
type: Guide
title: Management
description: Frames engineering management as turning goals into delivered outcomes across product, delivery, people, process, and technical scope.
tags: [management, leadership, process]
---

This guide covers the loops that connect strategy to feedback, and the metrics that show whether those loops work.

## Flow

### Dimensions

| Dimension | Question it answers | Primary artifact |
| --- | --- | --- |
| **Product** | What are we building and why? | Roadmap, backlog |
| **Delivery** | When will it ship, and at what risk? | Plan, milestones, release train |
| **People** | Who does it, and are they growing? | Assignments, 1:1s, growth plans |
| **Process** | How does work flow end to end? | Workflow, definition of done |
| **Technical** | Is the system sustainable? | Architecture decisions, tech-debt budget |

> Hold all five at once. A manager who covers only *delivery* produces burnout; one who covers only *people* produces drift.

### Stages

The stages by which a goal becomes executed work.

Analysis
: Survey of internal resources and external conditions, partitioned as a SWOT

Plan
: Ordered sequence of work with the resources, roles, and schedule that realize an objective

Task
: Atomic unit of a `Plan`, carrying a purpose, a definition of done, required resources, an owner, a timeline, dependencies, and a status

Monitoring
: Continuous evaluation of progress against the `Plan` and adaptation when conditions shift; failure to monitor is failure to act

### The loop

```svg
<Panel flow="TD">
  <Node key="strategy" col="0" row="0" label="Strategy —&#10;why" />
  <Node key="roadmap" col="0" row="1" label="Roadmap —&#10;what, roughly when" />
  <Node key="backlog" col="0" row="2" label="Backlog —&#10;ordered work items" />
  <Node key="plan" col="0" row="3" label="Plan —&#10;scope vs. capacity" />
  <Node key="execution" col="1" row="3" label="Execution —&#10;daily flow" />
  <Node key="delivery" col="1" row="2" label="Delivery —&#10;release" />
  <Node key="feedback" col="1" row="1" label="Feedback — metrics, retro, users" />
  <Edge from="strategy" to="roadmap" />
  <Edge from="roadmap" to="backlog" />
  <Edge from="backlog" to="plan" />
  <Edge from="plan" to="execution" />
  <Edge from="execution" to="delivery" />
  <Edge from="delivery" to="feedback" />
  <Edge from="feedback" to="backlog" label="re-prioritize" fromSide="left" toSide="right" />
  <Edge from="feedback" to="strategy" label="correct direction" fromSide="top" toSide="right" />
</Panel>
```

| Stage | Input → Output | Cadence |
| --- | --- | --- |
| **Business Strategy** | Business goals, market, constraints → themes, success metrics | Quarterly / annually |
| **Roadmap** | Themes → sequenced initiatives with rough sizing | Quarterly |
| **Backlog** | Initiatives, bugs, tech debt, requests → ordered, refined items | Continuous |
| **Plan** | Backlog and capacity → sprint or cycle commitment | Per sprint / cycle |
| **Execution** | Commitment → working increments | Daily |
| **Delivery** | Increments → released, measured change | Per release |
| **Feedback** | Metrics, retro, user signal → corrections to backlog and strategy | Per cycle |

**Key property:** the loop must close. A roadmap that is never corrected by feedback is a forecast presented as a plan.

### Planning Horizons

Plan with decreasing precision as the horizon extends. Precision beyond the evidence is waste.

| Horizon (period) | Granularity | Confidence |
| --- | --- | --- |
| **Strategic** (6–12 months) | Themes, outcomes | Directional |
| **Tactical** (1–3 months) | Initiatives, epics | Sized, not scheduled |
| **Operational** (1–4 weeks) | Stories, tasks | Committed |
| **Daily** (1 day) | Sub-tasks, blockers | Certain |

### Delivery Phases

The phases a solution passes through are defined once, as the SDLC, in [Development Process](../04-development-process/index.md). Management needs no second lifecycle — only the one phase the SDLC does not name, because its work concerns the team, not the product.

| Phase | Activities |
| --- | --- |
| **Pre-production setup** | Staffing the team and covering the required skills; provisioning environments, tooling, and access; agreeing the workflow, the definition of done, and the escalation path |

Complete it before implementation starts. Work that begins without it produces decisions no one can point to later: an undefined done, an unowned environment, an unagreed escalation path.

## How to

### Planning Concepts

The variables a `Plan` is negotiated with, and the conditions that constrain it.

Scope
: Set of work items accepted as in-bounds for an objective

    *The cheapest planning variable to change; time and quality are not*

Capacity
: Effort realistically available in a period, once meetings, support, and leave are taken out

    *Always below headcount multiplied by working hours*

Priority
: Total ordering of work items by value against cost and risk

    *If everything is priority one, nothing is*

Commitment
: Promise made with known `Scope`, known `Capacity`, and accepted `Risk`

    *Without capacity data it is a wish*

Dependency
: Work whose completion is required by other work, inside or outside the team

    *Cross-team ones sit outside the team's control, so track them explicitly*

Constraint
: Fixed boundary — budget, deadline, compliance, headcount — that planning must respect

Efficiency
: The *ratio* of `Value` delivered to `Resources` spent — doing things right;

  > not to be confused with *effectiveness*, doing the right things

### Prioritization

Pick one framework and apply it consistently; mixing frameworks produces arguments, not order.

| Framework | Formula / Rule | Best for |
| --- | --- | --- |
| **RICE** | `(Reach × Impact × Confidence) / Effort` | Product backlogs with comparable items |
| **WSJF** | `Cost of Delay / Job Duration` | Scaled delivery, competing epics |
| **MoSCoW** | Must / Should / Could / Won't | Fixed-date releases, scope negotiation |
| **Eisenhower** | Urgent × Important quadrants | Personal and interrupt-driven work |
| **Cost of Delay** | Value lost per period of delay | Deciding sequence, not selection |

**Reserve capacity explicitly.** Give each kind of work a named share of the cycle: planned features, tech debt and maintenance, and interrupt-driven support. Set the shares from the team's own measured unplanned-work share, and revise them when that measurement moves. Without an explicit reserve, unplanned work silently consumes the commitment and every sprint "fails".

### Estimation

Estimation
: A quantitative *forecast* of the `Resources` needed, made under stated assumptions about scope, complexity, risks, and contingency; a probable range, not a commitment

- Estimate **relatively** (points, sizes) rather than in hours; relative sizing stays stable when the person doing the work changes.
- Estimate as a **range**, not a point value, and carry the range through to the plan instead of collapsing it early.
- Forecast from **historical throughput** (items completed per cycle), not from summed estimates.
- Re-estimate only when new information arrives, never to fit a desired date.
- Treat unestimatable work as a **spike**: timebox it, produce knowledge, then estimate.

**Anti-pattern:** negotiating estimates downward. It changes the number, not the work.

### Decision Making

| Decision type | Approach |
| --- | --- |
| **Reversible, low impact** | Delegate. Decide fast, correct later |
| **Reversible, high impact** | Decide with input, set an explicit review point |
| **Irreversible** | Slow down. Gather data, write it down, review with peers |

Use a single accountable decider per decision (`DACI`: Driver, Approver, Contributors, Informed). Consensus is a nice outcome, not a decision procedure.

**Record decisions.** Every non-trivial technical decision gets an ADR: context, options, decision, consequences. See [Architecture](../02-architecture/index.md).

### SWOT Analysis

**SWOT**: Four-cell partition of a situation into `Strengths`, `Weaknesses`, `Opportunities`, and `Threats`.

Strengths
: Internal factors that give an advantage — resources, expertise, processes, relationships

Weaknesses
: Internal factors that hold back — missing resources, skills, or capabilities

Opportunities
: External factors worth exploiting — market trends, emerging technologies, unserved segments

Threats
: External factors that can cause harm — competition, downturns, shifting preferences, disruption

### SMART Goals

**SMART**: Five criteria that make a goal *actionable*: Specific, `Measurable`, `Achievable`, `Relevant`, and `Time-bound`.

Specific
: Clear and well-defined enough to answer who, what, when, where, and why

Measurable
: Quantifiable, so progress can be tracked by `Monitoring`

Achievable
: Realistic given the Resources and conditions in play

Relevant
: Aligned with the higher-level aims it serves, so local wins do not cost more elsewhere

Time-bound
: Anchored to a defined timeframe or deadline

### Metrics

Measure the **system**, not individuals. Individual metrics get gamed and destroy trust.

**Delivery performance (DORA):**

| Metric | Signal |
| --- | --- |
| Deployment frequency | Batch size and pipeline health |
| Lead time for change | End-to-end flow efficiency |
| Change failure rate | Quality of the delivery process |
| Time to restore | Operational resilience |

**Flow:**

| Metric | Signal |
| --- | --- |
| Throughput | Items completed per period — the basis for forecasting |
| Cycle time | Start to done for one item; watch the distribution, not the mean |
| WIP | Work started but not finished; the primary lever on cycle time |
| Flow efficiency | Active time divided by total time |
| Blocked time | Where dependencies are hurting |

**Health:** attrition, on-call load, unplanned-work share, and 1:1 sentiment. These lead the delivery metrics — they degrade first.

> Little's Law: `Cycle Time = WIP / Throughput`. To go faster, lower WIP before adding people.

## Problem Solving

Problem
: A factor that prevents or impedes progress toward a goal: conflicting interests, missing resources, a runtime failure, or a misunderstanding

Failure
: An attempt that does not reach its goal, or reaches it at a cost that outweighs the gain; informative, because it narrows what the next attempt must account for

Trade-off
: A choice in which one need is met at a measurable cost to another; unavoidable whenever resources are bounded and needs are multiple

Contingency
: Buffer reserved for `Problems` that cannot be anticipated, as distinct from the risks that can be

### Solving Approaches

The four stances a team can take toward a `Problem`, as set out by Russell Ackoff, plus one decomposition tactic.

Absolving
: Ignoring a `Problem` in the hope that it resolves itself; valid when acting costs more than the `Problem` does

Resolving
: Settling for a good-enough answer drawn from past experience, trial and error, or common sense; fast, not optimal

Solving
: Studying the `Problem` deeply enough to build a predictable model and choose the best available answer

Dissolving
: Redesigning the surrounding system so the conditions that produced the `Problem` no longer exist

Divide and Conquer
: Breaking a `Problem` into sub-problems until each is trivial, then composing the results; a tactic rather than a stance, so it combines with any of the four

### Risk Management

Risk
: Uncertain event that would affect an objective, sized as probability multiplied by impact

```svg
<Panel flow="LR">
  <Node key="identify" col="0" row="0" label="Identify" />
  <Node key="assess" col="1" row="0" colspan="2" label="Assess — probability × impact" />
  <Node key="plan" col="1" row="1" colspan="2" label="Plan response" />
  <Node key="monitor" col="0" row="1" label="Monitor" />
  <Edge from="identify" to="assess" />
  <Edge from="assess" to="plan" />
  <Edge from="plan" to="monitor" />
  <Edge from="monitor" to="identify" />
</Panel>
```

| Response | When to use |
| --- | --- |
| **Avoid** | Impact unacceptable, alternative path exists |
| **Mitigate** | Reduce probability or impact (spike, prototype, phased rollout) |
| **Transfer** | Another party is better positioned (vendor, insurance, platform team) |
| **Accept** | Cost of response exceeds expected loss — record the decision |

Keep the risk list short and current. Each entry holds a description, probability, impact, owner, response, and review date. A risk without an owner is not managed.

## Practical aspects

### Best Practices

- **Limit WIP.** Finishing beats starting. Cap in-progress items per person.
- **Make work visible.** One board, one source of truth. Untracked work cannot be managed.
- **Small batches.** Smaller changes ship faster, break less, and are easier to review.
- **Protect the reserve.** Defend capacity for tech debt and interrupts; do not let it be borrowed against.
- **Write things down.** `Decisions`, plans, and status in durable text — not in meetings or chat threads.
- **Escalate early.** A risk raised three weeks out is a decision; the same risk raised on the deadline is a failure.
- **Separate the estimate from the commitment.** An estimate is data; a commitment is a choice made with that data.
- **Give feedback continuously.** Nothing in a performance review should be a surprise.
- **Change one process thing at a time.** Otherwise you cannot attribute the effect.
- **Manage the interfaces.** Work waiting on another team sits outside either team's board, so the wait goes unmeasured until someone counts it.

### Anti-Patterns

| Anti-pattern | Why it fails | Correction |
| --- | --- | --- |
| Adding people to a late project | Onboarding cost exceeds short-term gain | Cut scope instead |
| Fixed scope, fixed date, and fixed team | Only quality can absorb variance | Make scope the variable |
| Estimates as commitments | Punishes honest estimation | Forecast with ranges and throughput |
| Planning for full utilization | Any variability turns into queueing delay | Plan below full utilization and keep the slack |
| Status meetings for information transfer | Expensive, synchronous, low bandwidth | Written async updates |
| Hero culture | Single points of failure, burnout | Pair, rotate, document |
| Retro actions never executed | Retros become ritual | Take on only as many actions as the next cycle can finish, each with an owner and a date |
| Managing individuals by metrics | Gaming, distrust | Measure the system |

### Checklists

**Before committing to a plan:**

- [ ] Objective stated as an outcome, with a success metric
- [ ] `Scope` is ordered, not just listed
- [ ] `Capacity` computed from actual availability, not from headcount
- [ ] `Dependencies` identified with named owners and dates
- [ ] Top risks listed with responses
- [ ] Reserve for interrupts and tech debt is intact
- [ ] Definition of done agreed
- [ ] `Stakeholders` know what is *not* in scope

**Weekly:**

- [ ] Board reflects reality
- [ ] Blocked items have an owner and a next action
- [ ] `Risk` list reviewed
- [ ] `Stakeholder` update sent
- [ ] 1:1s held, not canceled

**Per cycle:**

- [ ] Throughput and cycle time reviewed against forecast
- [ ] Retro run; previous actions verified as done
- [ ] Backlog re-prioritized against new information
- [ ] Unplanned-work share checked against the reserve
