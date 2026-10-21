---
type: Guide
title: Technical Debt
description: Explains intentional vs. unintentional technical debt, how to recognize it, and how to track and repay it.
tags: [development-process, technical-debt, architecture]
---

Technical debt is the extra rework a team takes on when it ships a quick solution instead of a thorough one. Ward Cunningham, one of the Agile Manifesto's authors, coined the metaphor in a 1992 OOPSLA experience report on the WyCash portfolio management system. This guide covers where debt comes from, how to recognize it, and how to track and repay it.

## Intentional vs. Unintentional Debt

| Kind | How It Arises | How It Behaves |
| --- | --- | --- |
| **Intentional** | Consciously chosen, visible to the whole team, and documented | A trade-off the team can plan around and repay |
| **Unintentional** | Accumulates without the team noticing | Surfaces later as unexplained development friction |

### Where Each Kind Comes From

| Driver | Kind | What Happens |
| --- | --- | --- |
| **Design trade-offs** | Intentional | The team knowingly accepts low cohesion or tight coupling to keep momentum, treating the shortcut as temporary |
| **Business pressure** | Intentional | Demand for frequent releases or last-minute changes forces faster but rougher delivery |
| **Gaps in expertise** | Unintentional | Insufficient experience on the team leads to accidental design flaws |
| **Weak internal process** | Unintentional | Poor collaboration, knowledge gaps, or unclear [standards](../00-software-engineering/02-standards.md) create flaws that harden into debt |

Intentional debt pays off in two situations:

- **A critical release date** — minor, non-disruptive flaws are accepted to hit the deadline and repaid afterward.
- **A POC or MVP** — only the concept needs validating, and code quality is not yet what the work is judged on.

## Recognizing Technical Debt

| Signal | Where It Shows | What It Looks Like |
| --- | --- | --- |
| **Quality degradation** | Delivery | Rising regressions, defects appearing in unrelated areas, and a growing list of known issues the team tolerates |
| **High cost of change** | Delivery | Small changes take disproportionate effort because of workarounds and poor reuse |
| **Slow experimentation** | Delivery | Spikes and POCs take longer and produce messier results than they should |
| **High barrier to entry** | Delivery | Only a couple of people understand the code, and onboarding is slow |
| **Hard to integrate** | Architecture | Adding features or connecting systems becomes difficult or unworkable |
| **Hard to reuse** | Architecture | High coupling and low cohesion stop components from being used elsewhere |
| **Hard to grow** | Architecture | The system resists scaling and performance work |
| **Hard to support** | Architecture | Documentation and maintainability suffer, especially where test coverage is uneven |
| **Delays** | Team | Onboarding friction and unplanned overtime during stabilization and regression phases |
| **Low estimation confidence** | Team | Chronic under- or over-estimation caused by unpredictable debt-related issues |
| **Low morale** | Team | People keep cutting corners against their own standards; in time some ask to move to other work |

## Tracking Technical Debt

Three approaches, best used together:

| Approach | What It Is |
| --- | --- |
| **Debt registry** | A shared, living document logging identified debt items so none is forgotten |
| **Debt backlog** | A prioritized, actionable task list derived from the registry, used to plan repayment capacity |
| **Analysis tooling** | Quality-gate tools such as SonarQube that surface metrics without manual logging |

Issue trackers such as Jira also make intentional debt visible, for example by charting logged vs. fixed defects over time. Two tool metrics carry most of the signal:

- **Code coverage** — flags areas of the codebase that lack unit tests.
- **[Code smells](../05-coding/06-code-smells.md)** — count and density of patterns that point at underlying design problems.

## Managing Technical Debt

Unmanaged debt moves a project through three states as it grows:

1. Delivery is on track.
2. Risks appear that will need action later.
3. Problems block delivery until they are solved.

Status reports often color these states green, amber, and red, so a slow drift from green to red is a common sign of debt nobody is managing.

### Risks of Leaving Debt Unmanaged

| Risk | Effect |
| --- | --- |
| **Damage to quality** | New features become harder to add cleanly, and rework, cost overruns, and schedule slippage follow |
| **Scalability and performance limits** | Unresolved trade-offs block scaling and performance gains until the root design issues are fixed |
| **Team strain** | Heavy debt makes progress slow and effortful, leading to burnout and lower-quality output |
| **Lost stakeholder trust** | Debt kept out of sight surfaces later as missed dates and surprise costs, and stakeholders stop trusting the team's plans |

## Keeping Debt Under Control

Control comes from three habits: let less debt in, keep what is there in plain view, and pay it down on purpose. Developers carry most of the first habit; whoever leads the team carries most of the other two.

**Let less debt in:**

- Apply [design principles](../05-coding/04-design-principles.md) such as SOLID and DRY, so fewer smells enter the code.
- Catch inconsistencies early in [code review](02-code-review.md).
- Spread knowledge, so no part of the codebase depends on a few people.
- Let static analysis do the checks people would otherwise do by hand.
- Rely on [automated tests](06-automated-testing.md) at unit, API and end-to-end level for fast, safe feedback.

**Keep debt in plain view:**

- Estimate each intentional debt item when it is logged, so its repayment can be planned against capacity.
- Publish debt figures on a fixed schedule.
- Go through the debt and the repayment plan with stakeholders at regular intervals.

**Pay it down on purpose:**

- Set capacity aside for debt work, as a buffer in each sprint or as a stabilization sprint.
- Give the same credit for reducing debt as for shipping features.

## Further Reading

- Ward Cunningham, [The WyCash Portfolio Management System](http://c2.com/doc/oopsla92.html) — the OOPSLA '92 experience report that introduced the debt metaphor.
- Martin Fowler, [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) — separates deliberate from inadvertent debt, and prudent from reckless.
- Nicolli S. R. Alves et al., "Towards an Ontology of Terms on Technical Debt" — Sixth International Workshop on Managing Technical Debt (MTD), 2014.
