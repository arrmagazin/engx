---
type: Guide
title: Roles and the Employee Lifecycle
description: The accountabilities behind common engineering titles, and the six stages a person passes through from hire to offboarding.
tags: [people, management, roles, hiring, onboarding]
---

Two structural questions must be settled before anyone can run a useful 1:1 or write a growth plan:

- Who is accountable for what?
- Where does this person currently stand in their time at the company?

Both change rarely, and everything in [Growing and Keeping People](03-growing-and-keeping-people.md) assumes them. Write them down once instead of deciding them again for each person.

Related: [Engineering Management](../01-methodology/00-engineering-management.md) · [Team Lead](01-team-lead.md) · [Knowledge Sharing](04-knowledge-sharing.md)

## Scope

The people side of management splits into six areas. Structure settles the first two: the roles defined below and the lifecycle stage a person is in. The other four are continuous work, covered in [Growing and Keeping People](03-growing-and-keeping-people.md).

| Area | Question it answers | Primary artifact |
| --- | --- | --- |
| **Staffing** | Do we have the right people and skills? | Role definitions, hiring plan, skill matrix |
| **Onboarding** | How fast does a new person become productive? | Onboarding checklist, first-90-days plan |
| **Alignment** | Does each person know what "good" means for them? | Expectations, goals, definition of done |
| **Growth** | Is each person getting better at something? | Career ladder, growth plan, learning budget |
| **Feedback** | Does each person know where they stand? | 1:1 notes, review cycles, feedback given |
| **Health** | Can this pace be sustained? | On-call load, unplanned work, sentiment, attrition |

The six are sequential in a person's experience and simultaneous in a manager's week.

## Roles

Titles vary by company; the *accountabilities* do not. Confusion about them is a common cause of dropped work.

| Role | Owns | Does not own |
| --- | --- | --- |
| **Engineer (IC)** | Their own delivery and craft | Team scope, priorities |
| **Tech Lead** | Technical direction of a team's work | Careers, compensation, performance |
| **Team Lead** | Day-to-day flow, unblocking, local process | Usually not compensation or headcount |
| **Engineering Manager** | People, performance, hiring, headcount, delivery | Detailed technical decisions |
| **Staff / Principal** | Technical scope across teams | Line management |

Two rules:

- **One accountable person per accountability.**
- **The person who runs someone's 1:1s owns their growth.** If these are two different people, say so explicitly and agree who gives which feedback.

## The Employee Lifecycle

```mermaid
graph LR
    H["Hire"] --> O["Onboard"]
    O --> C["Contribute"]
    C --> G["Grow"]
    G --> C
    C --> T["Transition"]
    T --> X["Offboard"]
    X -.->|"alumni, referrals"| H
```

| Stage | Manager's job | Success signal |
| --- | --- | --- |
| **Hire** | Define the role by the gap it fills; run a consistent, evidence-based loop | The scorecard predicted the first six months |
| **Onboard** | Give context, a buddy, and a small real task in week one | First meaningful merge within days, not weeks |
| **Contribute** | Set expectations, remove friction, give feedback continuously | The person knows what "good" means without asking |
| **Grow** | Match assignments to the next level's scope, not the current one | Autonomy rises while quality holds |
| **Transition** | Promote, move, or reassign before frustration forces the issue | Internal moves outnumber surprise resignations |
| **Offboard** | Capture knowledge, exit honestly, keep the relationship | Handover exists; the person would return |

**Key property:** doing a stage well is cheaper than the stage its failure leads to. Onboarding well is cheaper than re-hiring.

At the offboard stage, an unexamined [Bus Factor](03-growing-and-keeping-people.md#core-concepts) turns into lost work. Treat handover as a deliverable with a reviewer, not as a conversation. The practices that keep the bus factor above one are in [Knowledge Sharing](04-knowledge-sharing.md).

## Anti-patterns

| Anti-pattern | Why it fails | Correction |
| --- | --- | --- |
| Promoting the best coder to manager by default | Different job, different skills; loses an engineer and gains a poor manager | Dual ladder — IC track with equal ceiling |
| Hiring for "culture fit" | Selects for sameness; suppresses dissent | Hire for values alignment and skill gap |
| Onboarding as document dump | Context does not transfer by reading | Buddy plus a small real task in week one |

## Checklists

**When someone joins:**

- [ ] Role, level, and expectations written down before day one
- [ ] Accounts, access, and environment ready on day one
- [ ] Buddy assigned; first 1:1 scheduled in week one
- [ ] A small, real, shippable task in week one
- [ ] 30/60/90-day checkpoints in the calendar

**When someone leaves:**

- [ ] Knowledge handover written, not just walked through
- [ ] Ownership of systems and rituals reassigned by name
- [ ] Access revoked on the last day
- [ ] Honest exit conversation held and the cause recorded per local privacy rules, kept only as long as the retention policy allows
- [ ] Team told directly, in words agreed with the leaver, before the rumor
