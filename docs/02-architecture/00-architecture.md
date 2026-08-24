---
type: Guide
title: System Architecture
description: Defines system architecture as a discipline and describes its architectural views (logical, process, deployment, technology).
tags: [architecture, system-design]
---

# System Architecture

![System Architecture](/images/02-architecture.svg)

**`System Architecture`** as a discipline is 
:= an art of making *fundamental* *decisions* about a *solution* 
in way to *effectively* and *efficiently* satisfy business *expectations* in *given* context
by choosing the *optimal* options from *available* ones.

An *outcome* of **System Architecture** is 
the a fundamental high-level holistic *vision* of a solution, its: 
- design (inner components structure and dependencies, exteranal integration), 
- functioning (matching quality attributes, conforming constraints)
- and evolution over time.

SA incorporates, captures, and conveys:

- Significant **Decisions** against business *expectations*
- **Principles** guiding design and evolution
- **Aspects** that make a system function as it should
- General **goals**, **constraints**, technical **characteristics**
- **Measures** to ensure the system satisfies its intended purpose

Architecture stops at the decisions; turning them into schemas, endpoints, and algorithms is
[System Design](../03-system-design/00-system-design.md).


## Architectural Levels

| Level | Answers | Example |
| ------- | --------- | --------- |
| **Value** | Why we care | Changeable software costs less to own |
| **Principle** | What must hold | Separation of Concerns — cut along axes of change |
| **Pattern** | A reusable solution shape | Strategy, Repository, Observer |
| **BestPractice** | A repeatable action | Code review, refactoring, TDD |
| **Idiom** | A language-local form | RAII, context managers, `defer` |

Confusing the levels is the usual failure: a pattern applied where no principle demanded it is
accidental complexity, and a principle restated as a rule loses the trade-off that justified it.

## Architectural Views

| View | Description |
| ------ | ------------- |
| **Logical View** | Composition of components, units, layers, tiers in environment context; relations between components and agents |
| **Process View** | Relations, roles, behavior, interoperability, data flow of system components; integration with external systems |
| **Deployment View** | System integration with external environment |
| **Technology View** | Detailed design documents, prototypes, technical specifications |

```mermaid
mindmap
  root((Architecture))
    Logical
      Components
      Layers
      Tiers
    Process
      Roles
      Behavior
      Data Flow
    Deployment
      Environment
      Integration
    Technology
      Specs
      Prototypes
      Designs
```
