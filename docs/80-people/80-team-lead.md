# Team Lead: Responsibility, Way of Working, Workflow

A team leader serves as the central hub connecting company strategy with daily operations — bridging upper management and frontline staff by translating high-level business goals into practical, actionable milestones.

In a hybrid software team, the leader also acts as a **friction remover**, balancing asynchronous engineering work with synchronous collaboration across time zones.

---

## Core Responsibilities

A team leader's work splits evenly between **managing processes** and **developing people**:

| Area | What it means |
|---|---|
| **Task Delegation** | Assign work units to individuals based on their strengths, current workload, and skill level. |
| **Goal Alignment** | Set clear, quantifiable short-term metrics that map to the company's macro milestones. |
| **Performance Coaching** | Run routine evaluations, deliver constructive feedback, and mentor to close skill gaps. |
| **Conflict Resolution** | Intervene early on interpersonal tension; maintain healthy cross-functional relationships. |
| **Resource Advocacy** | Procure the software, materials, training, and clearances the team needs to work smoothly. |

**In a software / hybrid team, add:**

- **Architectural Alignment** — Ensure developers understand the technical vision before writing code, preventing technical debt.
- **Asynchronous Documentation** — Mandate that system designs, API contracts, and decisions are written down, not just spoken.
- **Deployment Guardrails** — Set up automated CI/CD pipelines to catch bugs early.
- **Hybrid Inclusion** — Structure meetings so remote and office workers have equal presence, visibility, and speaking time.
- **Burnout Monitoring** — Track commit patterns and PR data to spot developers working unhealthy hours.

---

## Way of Working (WoW)

Values and behavioral standards the leader models to drive execution:

- **Extreme Transparency** — Document operational goals openly; over-communicate strategic updates to eliminate ambiguity.
- **Psychological Safety** — Encourage independent decision-making; treat failures as systemic optimization steps.
- **Leading by Example** — Hold high standards of integrity, punctuality, and work ethic the team can mirror.
- **Continuous Feedback** — Replace annual appraisals with real-time praise and corrective coaching.

**In a software / hybrid team, add:**

- **Async-First Mindset** — Default to written updates over instant meetings to protect deep-focus coding time.
- **Output Over Hours** — Measure success by working software and sprint velocity, never by desk occupancy or green status dots.
- **Over-Communication** — Write detailed tickets, record short video walkthroughs (Loom), document edge cases explicitly.
- **Structured Office Days** — Use in-person days for brainstorming, complex debugging, or team bonding — never for solo coding.

---

## Workflow

A continuous, process-driven pipeline moves tasks from kickoff to deployment:

```
[1. Intake & Prioritization] ➔ [2. Sprint / Capacity Planning] ➔ [3. Daily Execution] ➔ [4. Review & QA] ➔ [5. Retrospective]
```

| Stage | General | Software / Hybrid |
|---|---|---|
| **1. Intake & Prioritization** | Evaluate incoming requests against the roadmap using prioritization matrices to determine urgency. | Async grooming: PMs and leads write tickets; engineers review requirements and post questions in comments before meetings. |
| **2. Sprint / Capacity Planning** | Map the prioritized pipeline against team hours and technical availability to prevent over-allocation. | Synchronous hybrid video call; commit scope based on historical velocity. |
| **3. Daily Execution** | Run short syncs (standups) to unblock dependencies and address friction. | Slack/Teams bots collect text standups; calendar blocks stay open for uninterrupted coding. |
| **4. Review & QA** | Act as final-review filter; ensure deliverables meet compliance standards before release. | Senior devs peer-review PRs; automated tests trigger on every commit. |
| **5. Retrospective** | Analyze post-delivery metrics to implement lean improvements for future cycles. | Every two weeks, review what slowed delivery and optimize CI/CD tools or workflows. |

### Operational Blueprint: Hybrid Scrum in Jira

Jira is the single, absolute source of truth — **if a task isn't in Jira, it doesn't exist.**

**Board columns:**

```
Backlog ➔ Selected for Development ➔ In Progress ➔ Code Review (PR) ➔ QA/Testing ➔ Done
```

**WIP limits** — Cap the *In Progress* column (e.g. max 1 task per developer). Forces engineers to close active tickets before opening new ones.

**Automation rules:**

- Link Jira to GitHub/GitLab.
- Opening a PR → auto-move ticket from *In Progress* to *Code Review*.
- Merging to main → auto-move ticket to *QA/Testing*.

**Rituals & cadence:**

| # | Ritual | When | How it works | Goal |
|---|---|---|---|---|
| 1 | **Async Refinement** | Mid-sprint | Lead tags engineers in tickets 48h ahead; questions go in comments. Meeting trimmed to 30 min for final alignment. | Avoid the 2-hour meeting; resolve edge cases async. |
| 2 | **Sprint Planning** | Day 1 | Synchronous call on the Jira backlog; digital planning poker so remote and office peers vote simultaneously. | Commit scope based on the historical Velocity Chart. |
| 3 | **Daily Standup** | Every morning | Slack bot (Geekbot / Standuply) collects text at 9:00 AM: did / will do / blockers. | Protect focus; lead calls a 10-min huddle only for flagged blockers. |
| 4 | **Code Review & QA** | Continuous | On *Code Review*, developer assigns the ticket to a peer. | SLA: PRs reviewed within 4 business hours — keeps code moving without calls. |
| 5 | **Sprint Review & Retro** | Last day | Live screen-share demo of staging to stakeholders; retro on a digital whiteboard (Miro / Confluence). | Use the Burndown Chart to diagnose scope creep or stalled reviews; fix for next sprint. |
