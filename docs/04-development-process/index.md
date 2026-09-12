---
type: Guide
title: Development Process
description: Maps the software development lifecycle onto the version control, review, delivery, quality, and maintenance guides in this chapter.
tags: [process, development, methodology]
---

# Development Process

The development process is the lifecycle that turns a stakeholder need into an operated solution, together with the practices that keep each phase verifiable. This chapter covers how teams version their work, review it, deliver it, test it, debug it, and keep it maintainable.

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Version Control](01-version-control.md)** | Centralized and distributed systems, branch lifetime, and branching strategies |
| **[Code Review](02-code-review.md)** | Review types and workflow, checklists, and how to give feedback |
| **[CI/CD](03-ci-cd.md)** | Continuous integration and delivery, and the environment stages a change passes through |
| **[Quality Assurance](04-quality-assurance.md)** | Test case and defect management, QA metrics, and the test automation strategy |
| **[Testing](05-testing.md)** | The F.I.R.S.T. principles, TDD and BDD, unit testing, test doubles, coverage types, and tests in CI |
| **[Debugging](06-debugging.md)** | Reproducing, reducing, bisecting and verifying a fix, plus the Chrome DevTools panels and console utilities |
| **[Technical Debt](07-technical-debt.md)** | Where debt comes from, the signals that expose it, and how to manage repayment |

## SDLC

**SDLC (Software Development Lifecycle)**: One-pass or iterative cycle of interdependent phases and processes that turns a stakeholder need into an operated [Solution](../00-software-engineering/01-glossary.md#solution). Each phase consumes the verified output of the previous one and produces artifacts that make the next one verifiable — the lifecycle is what connects [Requirements](../00-software-engineering/01-glossary.md#solution) to [Metrics](../00-software-engineering/01-glossary.md#solution) in practice.

| Phase | Definition |
| --- | --- |
| **Discovery** | Establishing the problem, stakeholders, constraints, and expected value before committing resources |
| **Analysis** | Turning intent into Requirements — defined boundaries on Metrics that make success verifiable |
| **[Design](../00-software-engineering/01-glossary.md#delivery)** | Deciding WHAT the solution should be and WHY, judged against usability from the end-user perspective |
| **Implementation** | Producing executable code, configuration, and metadata that realizes the design |
| **Verification** | Confirming the built solution satisfies its functional and [non-functional requirements](../02-architecture/01-quality-attributes.md) |
| **Release** | Delivering a versioned, reproducible artifact into a target environment |
| **Operation** | Running, observing, and supporting the Solution against its Metrics in production |
| **Maintenance** | Correcting defects, absorbing change, and repaying [technical debt](07-technical-debt.md) over the solution's life |

Phases are *interdependent*, not merely sequential: verification is designed during Analysis, operability is decided during Design, and observations from Operation re-enter Discovery.

## Cycle Shapes

| Cycle Shape | Definition |
| --- | --- |
| **One-pass (Waterfall)** | Each phase completes and is signed off before the next begins; low feedback, viable only when Requirements are stable and known upfront |
| **Iterative** | The full cycle repeats over a growing scope, each pass refining the same solution |
| **Incremental** | Each pass delivers an additional slice of functional scope that is independently valuable |
| **Continuous** | Phases overlap permanently and are automated into a [CI/CD pipeline](03-ci-cd.md), reducing the cycle to a change-sized unit |

The choice of cycle shape is a [methodology](../01-methodology/index.md) decision constrained by risk, feedback cost, and requirement volatility — not a property of the software itself. Iterative and incremental delivery is treated as one practice, [IID](../01-methodology/02-agile.md#agile-practices), in the agile guide.
