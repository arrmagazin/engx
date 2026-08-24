---
type: Guide
title: Development Process
description: Indexes the development process sub-topics—code review, version control, debugging, and CI/CD.
tags: [process, development, methodology]
---

# Development Process

![Development Process](/images/12-Development-Process.svg)

## SDLC

**SDLC (Software Development Lifecycle)**: One-pass or iterative cycle of interdependent phases and processes that turns a stakeholder need into an operated Solution. Each phase consumes the verified output of the previous one and produces artifacts that make the next one verifiable — the lifecycle is what connects Requirements to Metrics in practice.

| Phase | Definition |
| ------- | ------------ |
| **Discovery** | Establishing the problem, stakeholders, constraints, and expected value before committing resources |
| **Analysis** | Turning intent into Requirements — defined boundaries on Metrics that make success verifiable |
| **Design** | Deciding WHAT the product/service should be and WHY, then HOW it decomposes into Components and interfaces |
| **Implementation** | Producing executable code, configuration, and metadata that realizes the design |
| **Verification** | Confirming the built solution satisfies functional and non-functional Requirements |
| **Release** | Delivering a versioned, reproducible artifact into a target environment |
| **Operation** | Running, observing, and supporting the Solution against its Metrics in production |
| **Maintenance** | Correcting defects, absorbing change, and repaying technical debt over the Solution's life |

Phases are *interdependent*, not merely sequential: verification is designed during Analysis, operability is decided during Design, and observations from Operation re-enter Discovery.

| Cycle Shape | Definition |
| ------------- | ------------ |
| **One-pass (Waterfall)** | Each phase completes and is signed off before the next begins; low feedback, viable only when Requirements are stable and known upfront |
| **Iterative** | The full cycle repeats over a growing scope, each pass refining the same Solution |
| **Incremental** | Each pass delivers an additional slice of functional scope that is independently valuable |
| **Continuous** | Phases overlap permanently and are automated into a pipeline (CI/CD), reducing the cycle to a change-sized unit |

The choice of cycle shape is a *methodology* decision constrained by risk, feedback cost, and requirement volatility — not a property of the software itself.
