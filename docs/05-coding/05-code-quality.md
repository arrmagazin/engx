---
type: Guide
title: Code Quality
description: Explains functional vs. structural code quality, what late-found defects cost, and the standards, tools, and metrics that hold quality up.
tags: [coding, code-quality, maintainability]
---

# Code Quality

Code quality has two sides: whether the code does the right thing, and how it is built. This guide covers both dimensions, what a late-found defect costs, the standards and analysis tools that keep quality up, and the metrics that make it measurable — for the developers writing code and the peers reviewing it.

## Two Dimensions

- **Functional** — what the code *does*: does it meet the functional requirements? Checked by unit and functional tests, covered in [Quality Assurance](../04-development-process/04-quality-assurance.md)
- **Structural** — how the code is *organized*: readable, free of extra detail, consistent with project guidelines. Checked by static analysis and [code review](../04-development-process/02-code-review.md)

## Why It Matters

| Aspect | High Quality | Poor Quality |
| --- | --- | --- |
| **Cost of change** | Code is quick to read, so a change lands where it was meant to | Code takes longer to understand, so changes are more likely to be wrong |
| **Defects** | Fewer defects reach users | More defects reach users |
| **New features** | New work builds on what is already there | Each feature costs more than the last |
| **Onboarding** | Newcomers become productive sooner | Newcomers need longer before they can be trusted with changes |
| **End state** | The system keeps evolving | The system accumulates [technical debt](../04-development-process/07-technical-debt.md) until a rewrite looks cheaper |

## The Cost of Defects

A defect can destroy the system it runs on. On 4 June 1996 the European Space Agency's Ariane 5 was destroyed less than a minute after launch on its first flight, Flight 501. The inquiry traced the failure to an unprotected conversion of a 64-bit floating-point value to a 16-bit signed integer in inertial reference software reused from Ariane 4, where a value that large could not arise.

Fixing a defect costs far more than the edit itself. Reproducing it, logging it, assigning it, discussing it, changing the code, and verifying the change each take time, usually from more than one person.

That cost rises the later the defect is found — cheapest while requirements are still being written, most expensive once the software is in production and maintenance. Barry Boehm set out this curve in *Software Engineering Economics* (1981), and it is the argument behind every early-feedback practice: static analysis, [code review](../04-development-process/02-code-review.md), and [CI/CD](../04-development-process/03-ci-cd.md) quality gates.

## Two Supporting Practices

### Coding Standards

Standards are agreed guidelines for style, practice, and method. Agreeing on them up front sets one expectation for everyone instead of one per developer. Abelson and Sussman state the goal in *Structure and Interpretation of Computer Programs*: "Programs must be written for people to read, and only incidentally for machines to execute."

They improve clarity, readability, consistency, and maintainability, and hold complexity down. The broader industry and regulatory layer above a team's own rules is covered in [Software Engineering Standards](../00-software-engineering/02-standards.md).

- **Style** — visual layout: indentation, whitespace, capitalization, naming style, comments
- **Design** — structure: use of language constructs (exception handling, `goto`/`break`), logical structure (method size, parameter count, naming), and the [design principles](02-design-principles.md) the team follows, such as SOLID and KISS
- **Conventions** — project-specific rules that extend or override the above: implementation guidance, feature rules, naming patterns, and explicit do-nots

### Automated Code Analysis

Automated analysis checks code against a rule set with no manual effort, catching security issues, duplication, and style violations at a scale review cannot reach. It runs statically, without executing the application; some tools flag violations as you type.

[SonarQube](https://www.sonarsource.com/products/sonarqube/) from SonarSource is a widely used platform for continuous inspection. Its open-source edition was renamed Community Build in late 2024; analysis of C, C++, and several other languages is available only in the commercial editions. IntelliJ IDEA and Visual Studio ship their own inspections.

Static analysis has limits. It has no business context, cannot confirm that code meets a specific requirement, and cannot catch architecture or design problems that depend on developer intent — which is what review and the [Code Smells](04-code-smells.md) catalog are for.

## Metrics

Quality judgments are subjective; metrics make part of the judgment measurable and surface risk early.

| Metric | What It Measures |
| --- | --- |
| **Cyclomatic complexity** | The number of linearly independent paths through a piece of code, derived from its decision points; defined by Thomas McCabe in 1976. Higher values mean more branches to read, test, and get wrong |
| **Class coupling** | How many other classes a class depends on. Lower coupling makes a class easier to reuse and to change in isolation |
| **Depth of inheritance tree** | How many levels a class sits below its root ancestor. Deeper hierarchies make behavior harder to trace |
| **Code duplication** | Repeated code sequences. A change to one copy can miss the others |
| **LCOM (Lack of Cohesion of Methods)** | Whether a class's methods serve one clear purpose; defined by Chidamber and Kemerer in their 1994 metrics suite. Low cohesion produces large classes that do several unrelated things |

## Best Practices

Writing the standards and enforcing them with tooling are covered above, under [Coding Standards](#coding-standards) and [Automated Code Analysis](#automated-code-analysis). What keeps both of them working:

- Keep the standards current in the knowledge base
- Include them in onboarding for every newcomer
- Extend the tool's default rule set with project-specific rules
- Keep CI quality gates green, and never leave a gate broken
- Measure the metrics on a regular schedule and act where one falls short
