---
type: Guide
title: Scrum Framework
description: Summarizes the Scrum framework's roles, ceremonies, and empirical approach to delivering product increments.
tags: [methodology, agile, scrum]
---

# Scrum Framework

![Scrum Framework](/images/10-scrum.svg)

## What is Scrum?

**Scrum** is a lightweight framework that helps to
generate value through adaptive solutions for complex problems.

It's about managing the process of development, delivery, and sustaining of products that:

- Respects an empirical approach to address complex adaptive problems and requirement volatility
- Strives to deliver properly tested product increments of the highest possible value within short iterations
- Employs transparency, inspection, and adaptation to optimize predictability and control risk
- Emphasizes self-organized, high-performing team that values commitment, courage, focus, openness, and respect

## The Scrum Team

| Role | Description |
| ------ | ------------- |
| **Product Owner** | Person representing interests of stakeholders, responsible for maintaining product backlog and ensuring value of work |
| **Scrum Master** | Servant-leader helping everyone understand Scrum theory, practices, rules, and values; responsible for process and maximizing benefits |
| **Development Team** | Cross-functional group working together toward common goals; responsible for delivering Increments at end of every sprint |

## Scrum Ceremonies

1. **Daily** - Daily standup meeting
2. **Planning** - Sprint planning session
3. **Refinement** - Backlog grooming
4. **Review (Demo)** - Sprint review/demonstration
5. **Retro** - Sprint retrospective

```mermaid
sequenceDiagram
    participant PO as Product Owner
    participant SM as Scrum Master
    participant Dev as Development Team
    PO->>Dev: Refinement
    PO->>Dev: Planning
    loop Sprint
        Dev->>Dev: Daily
        SM->>Dev: Remove impediments
    end
    Dev->>PO: Review (Demo)
    SM->>Dev: Retro
    Dev->>PO: Increment
```

## Scrum Artifacts

| Artifact | Description |
| ---------- | ------------- |
| **Sprint Burn-down Chart** | Daily progress for a sprint over the sprint's length |
| **Release Burn-down Chart** | Feature level progress of completed product backlog items |
| **Product Backlog (PBL)** | A prioritized list of high-level requirements |
| **Sprint** | A time period (typically 1-4 weeks) in which development occurs on a set of backlog items committed by team |
| **Sprint Backlog (SBL)** | A prioritized list of tasks to complete during the sprint |
| **Tasks** | Work items added to sprint backlog; usually take a day to finish, should not exceed 12 hours (two days) |
| **Spike** | A time-boxed period used to research a concept or create simple prototype |
| **Definition of Done (DoD)** | Exit-criteria to determine whether a backlog item is complete |
| **Increment** | Sum of all Product Backlog items completed during a Sprint and value of all previous Sprints |

```mermaid
classDiagram
    class PBL {
        prioritized items
    }
    class Sprint {
        1-4 weeks
    }
    class SBL {
        committed items
    }
    class Task {
        <= 12h
    }
    class Spike {
        time-boxed research
    }
    class DoD {
        exit criteria
    }
    class Increment {
        shippable value
    }
    PBL "1" --> "*" Sprint : feeds
    Sprint "1" --> "1" SBL : contains
    SBL "1" --> "*" Task : decomposes
    SBL "1" --> "*" Spike : may include
    Task ..> DoD : verified by
    Sprint "1" --> "1" Increment : produces
```

## Estimation Concepts

| Concept | Description |
| --------- | ------------- |
| **Story Point** | A COMPOSITE, RELATIVE, SUBJECTIVE measure unit estimating "overall" size of work: expected effort, team skills, uncertainties, QA, workflow overheads |
| **Velocity** | Total effort a team is capable of in a sprint; derived from work completed in last sprint's backlog items; guides future sprint planning |
