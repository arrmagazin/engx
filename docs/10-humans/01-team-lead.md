---
type: Guide
title: Team Lead
description: The team lead role — core responsibilities, way of working, and the workflow that carries a task from intake to release.
tags: [people, leadership, team-lead, management]
---

# Team Lead

A team lead connects company strategy to daily engineering work, turning business goals into milestones a team can act on and removing the friction that stops it. This guide covers the role's responsibilities, the behaviors it models, and the workflow that moves a task from intake to release — for leads of hybrid software teams and for the engineers working with them.

## Core Responsibilities

| Area | What It Means |
| --- | --- |
| **Task Delegation** | Assign work to individuals based on their strengths, current workload, and skill level |
| **Goal Alignment** | Set short-term, measurable goals that map to the company's longer-term milestones |
| **Performance Coaching** | Run routine evaluations, give constructive feedback, and mentor to close skill gaps |
| **Conflict Resolution** | Intervene early on interpersonal tension and keep cross-functional relationships working |
| **Resource Advocacy** | Obtain the software, training, and access the team needs so nobody waits on a request |

**In a software or hybrid team, add:**

- **Architectural Alignment** — Make sure developers understand the technical direction before they write code, so the design does not accumulate [technical debt](../04-development-process/07-technical-debt.md) by accident.
- **Asynchronous Documentation** — Require that system designs, API contracts, and decisions are written down, not only spoken.
- **Deployment Guardrails** — Put automated [CI/CD](../04-development-process/03-ci-cd.md) pipelines in place so defects are caught before release.
- **Hybrid Inclusion** — Structure meetings so remote and office participants get equal presence and speaking time.
- **Burnout Monitoring** — Watch commit and pull request patterns for people working unhealthy hours.

## Way of Working (WoW)

The values and behaviors a lead models so the team copies them:

- **Transparency** — Keep operational goals in the open and repeat strategic updates until they are understood.
- **Psychological Safety** — Encourage independent decisions; treat a failure as evidence about the system rather than about a person.
- **Leading by Example** — Hold the standards of integrity, punctuality, and work ethic the team is expected to match.
- **Continuous Feedback** — Give praise and correction when the work happens, instead of saving both for an annual review.

**In a software or hybrid team, add:**

- **Async-First Mindset** — Default to written updates rather than immediate meetings, to protect uninterrupted coding time.
- **Output Over Hours** — Judge the work by what ships, not by desk occupancy or a green status dot.
- **Over-Communication** — Write detailed tickets, record short screen walkthroughs, and spell out edge cases.
- **Structured Office Days** — Use in-person days for design discussion, hard debugging, and team building, not for solo coding.


## Delegation

Delegate the **outcome**, not the steps. Match the level of autonomy to demonstrated competence in that specific area:

| Level | Instruction | Use when |
| --- | --- | --- |
| 1 | "Do exactly this" | New to the domain |
| 2 | "Investigate, report back, I decide" | Learning |
| 3 | "Recommend an option, then act on approval" | Growing |
| 4 | "Decide and act, tell me afterwards" | Competent |
| 5 | "Own this area" | Expert |

Delegating at too low a level stalls growth; too high a level sets people up to fail. Autonomy level is per-area, not per-person.

## Communication Cadence

| Ritual | Frequency | Purpose | Failure mode to avoid |
| --- | --- | --- | --- |
| **Standup** | Daily | Surface blockers | Status theater for the manager |
| **1:1** | Weekly / bi-weekly | Growth, friction, feedback | Canceled when busy; turned into status |
| **Planning** | Per cycle | Commit scope to capacity | Committing beyond capacity |
| **Review / Demo** | Per cycle | Show working software | Slides instead of software |
| **Retrospective** | Per cycle | Improve the process | Repeated actions never done |
| **Stakeholder update** | Weekly, written | Alignment, expectation control | Only communicating bad news late |

What these events *are*, and the timeboxes the Scrum Guide sets for them, is covered in [Scrum](../01-methodology/03-scrum.md); the table above covers only how often a manager runs them and how each one fails.

**Default to written and asynchronous.** Meetings are for decisions and disagreements, not for information transfer.


## Workflow

| Stage | General | Hybrid Software Team |
| --- | --- | --- |
| **1. Intake and Prioritization** | Evaluate incoming requests against the roadmap to decide urgency and order | Product managers and leads write the tickets; engineers read the requirements and raise questions in comments before any meeting |
| **2. Sprint and Capacity Planning** | Match the prioritized queue against the team's available [capacity](../01-methodology/index.md#planning-concepts) so nobody is over-allocated | One synchronous video call; scope is committed against the team's own delivery history |
| **3. Daily Execution** | Hold a short sync to surface blockers and dependencies | A chat bot collects written standups, and calendars keep long blocks free for coding |
| **4. Review and QA** | Act as the last filter before release, checking deliverables against the agreed quality bar | Peers review pull requests, as described in [Code Review](../04-development-process/02-code-review.md), and automated [tests](../04-development-process/04-quality-assurance.md) run on every commit |
| **5. Retrospective** | Look back at the delivered cycle and pick improvements for the next one | At the end of each sprint, review what slowed delivery and fix the tooling or the process behind it |

### Operational Blueprint: Hybrid Scrum in Jira

One team's concrete configuration, recorded as a worked example rather than as a recommended standard — every value below is that team's own setting, not a benchmark for teams at large. The five Scrum events and their official timeboxes are defined in [Scrum Framework](../01-methodology/03-scrum.md); this section covers only how this team adapts them to hybrid work.

For this team, Jira is the single source of truth: a task that is not in Jira does not exist.

**Board columns:**

```text
Backlog ➔ Selected for Development ➔ In Progress ➔ Code Review (PR) ➔ QA/Testing ➔ Done
```

**WIP limits** — the *In Progress* column is capped at one task per developer, so an engineer closes an active ticket before opening another.

**Automation rules:**

- Jira is linked to GitHub or GitLab.
- Opening a pull request moves the ticket from *In Progress* to *Code Review*.
- Merging to the main branch moves the ticket to *QA/Testing*.

**Rituals and cadence:**

| Ritual | When | How It Works | Goal |
| --- | --- | --- | --- |
| **Backlog Refinement** | Ongoing | Refinement is a continuous activity rather than a scheduled event: the lead tags engineers in tickets around 48 hours before planning, questions are answered in the comments, and a 30-minute call closes whatever is still open | Settle edge cases in writing instead of in a long meeting |
| **Sprint Planning** | Day 1 | Synchronous call over the Jira backlog, with digital planning poker so remote and office peers vote at the same time | Commit scope against the team's velocity chart |
| **Daily Standup** | Every working day | A Slack bot such as Geekbot or Standuply collects written answers at 9:00 AM: done, next, blockers | Protect focus, with a 10-minute huddle only for flagged blockers |
| **Code Review** | Continuous | When a ticket reaches *Code Review* the author assigns a peer, and pull requests are reviewed within four business hours | Keep changes moving without scheduling a call; the process itself is in [Code Review](../04-development-process/02-code-review.md) |
| **Sprint Review** | Last day | Live screen share of the staging environment for stakeholders | Inspect the increment with the people who asked for it |
| **Sprint Retrospective** | Last day, after the review | The team works through a digital whiteboard such as Miro or Confluence | Use the burndown chart to diagnose scope creep or stalled reviews, and pick fixes for the next sprint |
