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

Intentional debt pays off in two situations. The first is a critical release date, where minor and non-disruptive flaws are accepted to hit the deadline and repaid afterward. The second is a POC or MVP, where only the concept needs validating and code quality is not yet what the work is judged on.

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
| **Demotivation** | Team | Team members feel forced to cut corners, sometimes to the point of wanting off the project |

## Tracking Technical Debt

Three approaches, best used together:

| Approach | What It Is |
| --- | --- |
| **Debt registry** | A shared, living document logging identified debt items so none is forgotten |
| **Debt backlog** | A prioritized, actionable task list derived from the registry, used to plan repayment capacity |
| **Analysis tooling** | Quality-gate tools such as SonarQube that surface metrics without manual logging |

Issue trackers such as Jira are also used to make intentional debt visible, for example by charting logged vs. fixed defects over time. Two tool metrics carry most of the signal:

- **Code coverage** — flags areas of the codebase that lack unit tests.
- **[Code smells](../05-coding/04-code-smells.md)** — count and density of patterns that point at underlying design problems.

## Managing Technical Debt

Project health is commonly reported as a Red/Amber/Green status:

| Status | Meaning |
| --- | --- |
| **Red** | Issues that must be resolved for successful delivery |
| **Amber** | Potential issues that may need attention later |
| **Green** | Healthy performance |

Unmanaged debt tends to move a project from green to amber to red as it accumulates.

### Risks of Leaving Debt Unmanaged

| Risk | Effect |
| --- | --- |
| **Damage to quality** | New features become harder to add cleanly, and rework, cost overruns, and schedule slippage follow |
| **Scalability and performance limits** | Unresolved trade-offs block scaling and performance gains until the root design issues are fixed |
| **Team strain** | Heavy debt makes progress slow and effortful, leading to burnout and lower-quality output |
| **Strained client communication** | Lack of transparency about debt erodes trust and reputation with clients |

## Recommendations

### For Leaders

- Reserve dedicated time for debt work, as buffers or stabilization sprints.
- Estimate intentional debt when it is logged, so repayment can be planned against capacity.
- Report debt statistics regularly for visibility.
- Recognize debt-reduction work the way feature work is recognized.
- Review debt and repayment plans with client stakeholders on a regular cadence.

### For Developers

- Follow [design principles](../05-coding/02-design-principles.md) such as SOLID and DRY to avoid introducing smells.
- Use [code review](02-code-review.md) to catch inconsistencies early.
- Share knowledge so the codebase does not depend on a few people.
- Run static analysis rather than relying on manual checks.
- Use [automated testing](04-quality-assurance.md) at unit, API, and end-to-end level for fast, safe feedback.

## Further Reading

- Ward Cunningham, [The WyCash Portfolio Management System](http://c2.com/doc/oopsla92.html) — the OOPSLA '92 experience report that introduced the debt metaphor.
- Martin Fowler, [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) — separates deliberate from inadvertent debt, and prudent from reckless.
- Nicolli S. R. Alves et al., "Towards an Ontology of Terms on Technical Debt" — Sixth International Workshop on Managing Technical Debt (MTD), 2014.
