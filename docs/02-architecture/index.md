---
type: Guide
title: System Architecture
description: Opens the architecture chapter — what architecture decides, the levels it works at, and the views it is described through.
tags: [architecture, system-design]
---

**System architecture** is the practice of making the decisions about a solution that are expensive to reverse: what its parts are, how they interact, and how it is expected to change. This chapter covers those decisions and the quality attributes they are judged against. Architecture stops at the decisions — turning them into schemas, endpoints, and algorithms is [System Design](../03-system-design/index.md), and the attack classes a web application is built to withstand are [Web Application Security](../06-frontend/05-security-web.md).

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Key Quality Attributes](01-quality-attributes.md)** | The design, runtime, system, and user properties an architecture is evaluated against |
| **[Architectural Views](02-architectural-views.md)** | The logical, process, deployment, and technology views an architecture is described through |
| **[Architectural Patterns](03-architectural-patterns.md)** | Layered, MVC, and hexagonal inside a unit; monolith, microservices, and event-driven across units |

## What Architecture Captures

| Element | What it records |
| ------- | --------------- |
| **Decisions** | The significant choices made against business expectations, and what each one costs |
| **Principles** | The rules that guide design and evolution once the decisions are made |
| **Constraints** | Goals, limits, and technical characteristics the system must respect |
| **Measures** | How the system is checked against its intended purpose |

## Architectural Levels

| Level | Answers | Example |
| ------- | --------- | --------- |
| **Value** | Why we care | Changeable software costs less to own |
| **Principle** | What must hold | Separation of Concerns — cut along axes of change |
| **Pattern** | A reusable solution shape | Strategy, Repository, Observer |
| **Idiom** | A language-local form | RAII, context managers, `defer` |

Confusing the levels is the usual failure: a pattern applied where no principle demanded it is accidental complexity, and a principle restated as a rule loses the trade-off that justified it. The patterns that shape a whole system rather than a single class are covered in [Architectural Patterns](03-architectural-patterns.md).

## Architectural Views

No single diagram holds the whole architecture, so it is described through four views, each answering one set of concerns.

| View | What it describes |
| ------ | ------------- |
| **Logical View** | Components, units, layers, and tiers, and the relations between them |
| **Process View** | Roles, behavior, data flow, and integration with external systems |
| **Deployment View** | How the system is placed in its runtime environment |
| **Technology View** | Detailed design documents, prototypes, and technical specifications |

What each view records, who reads it, and which ones are worth producing when: [Architectural Views](02-architectural-views.md).
