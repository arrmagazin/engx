---
type: Guide
title: Code Review
description: Covers code review's value, its types including pair programming, the workflow, what reviewers check, checklists, and feedback practices.
tags: [development-process, code-review, quality]
---

# Code Review

Code review is the practice of having teammates read new code before it merges. This guide covers the review types — pair programming among them, as review happening while the code is written — the workflow, what reviewers check, how to build a review checklist, and how to write useful feedback — for the developers submitting code and for the peers reviewing it.

## Why It Matters

| Dimension | With Review | Without Review |
| --- | --- | --- |
| **Defects** | An outside reader catches logic, algorithm, and architecture errors before the change merges | Errors survive into production and degrade the correctness of the product |
| **Maintainability** | Code stays readable because it is written to be read by someone else first | Code becomes harder to follow and harder to change, so every later edit costs more |
| **Knowledge Sharing** | Domain knowledge, business logic, and refactoring techniques spread across the team | Developers duplicate work instead of reusing solutions, and miss business functionality that already exists |
| **Consistent Standards** | The team converges on one agreed [style guide](../00-software-engineering/02-standards.md), so any developer can pick up any file | Technical approaches diverge and have to be reconciled later, at cost and sometimes with friction between authors |
| **Security and Compliance** | Missing authorization checks, weak configuration, and dependencies with unsuitable licenses or known vulnerabilities are caught before release | Vulnerabilities reach end users, exposing customer data and the company's reputation |

## Review Types

| Type | How It Works | When to Use |
| --- | --- | --- |
| **Peer Review** | The author publishes a branch and opens a pull or merge request; peers review asynchronously while the author moves on to another task | The default for every change. Internal peers spread product knowledge, external reviewers bring in expertise the team lacks |
| **Specialist Review** | A named expert in architecture, security, or performance reviews one fragment of code, often from outside the delivery team | Critical or high-risk code, periodically or on request |
| **Pair Programming** | Two developers write and review the code together, line by line, in one session | Peers of similar level working through a complex problem, senior-to-junior mentoring, and onboarding |

## Review Workflow

Every review type follows the same three-step cycle:

1. **Notify** — the author finishes the change and requests review; reviewers leave feedback on specific lines or on the change as a whole.
2. **Approve** — if there is nothing to change, the review ends and the code merges into the main codebase.
3. **Revise** — if changes are requested, the author addresses the feedback and resubmits for final approval.

Agree on a turnaround time, or reviews stall the board. [the team lead guide](../10-management/02-team-lead.md) documents one concrete version: opening a pull request moves the ticket to a *Code Review* column automatically, the author assigns a peer, and pull requests are reviewed within four business hours.

## What Reviewers Check

Five areas span both dimensions of [code quality](../05-coding/05-code-quality.md) — what the code does, and how it is organized.

| Area | What to Verify |
| --- | --- |
| **Functional Correctness** | The change implements every requested behavior and does not break existing business logic |
| **Design** | Edge cases are handled, patterns suit the problem, redundancy and unnecessary dependencies are gone, and no shorter or safer equivalent exists |
| **Readability** | Naming and control flow are logical and consistent, the change can be followed across files and functions, project and API conventions are respected, and no leftover TODO comments remain |
| **Tests** | Tests exist, are readable, cover the edge cases and the business use cases, and match the project's test style |
| **Non-Functional Implications** | Authorization and authentication are correct, configuration and untrusted input are handled safely, behavior holds no surprises, and no library arrives with an unsuitable license |

For anything touching authentication, authorization, or untrusted input, check the change against the [OWASP Top Ten](https://owasp.org/www-project-top-ten/) and consult an application security specialist when in doubt.

## Review Checklists

A review checklist is a shared project artifact that both authors and reviewers work from, and it belongs in the onboarding materials. It keeps review quality stable regardless of who reviews and stops steps from being skipped. Its reviewer half is the five areas above, agreed by the whole team at project initiation and revised as the project matures.

### Building One

1. Get agreement from the project or account manager to create it.
2. Write down the review process the team already follows, including the undocumented parts: the scope of a reviewable change, required checks, tools, how many reviewers and how they are chosen, the process steps, time limits, and how non-critical notes are handled.
3. Propose improvements as a list to discuss with the team, rather than changing the process alone.

### Tailoring It

- **Match reviewers to the goal** — more reviewers, juniors included, when the goal is knowledge sharing; senior specialists when the goal is quality or security.
- **Make peer review mandatory** for every change, and reserve specialist review for the critical parts.
- **Weight high-risk code** — critical business logic, performance-sensitive paths, code handling sensitive data, changes from new team members, and large refactors.
- **Treat the checklist as a living document** — revisit it periodically, for example at a retrospective.
- **Keep it where the team already looks** — a shared wiki page, pinned in the team's chat channel.

### Developer Self-Check

Before requesting review, the author confirms that:

- The code compiles and passes linting, tests, and quality gates.
- Unit tests exist and the change has been tested by the developer.
- The code is documented and tidy: consistent indentation, no commented-out blocks, no typos.
- Unused imports and compiler warnings are gone.
- The team's coding standards are followed.
- No development-only values are hardcoded.
- Performance and security implications were considered.
- Nothing in the change duplicates an existing reusable component or library.

## Making Review Efficient

- **Keep changes small** — one merge request per issue, so a reviewer can hold the whole change in mind.
- **Book a fixed slot** — a set time each day, for example one hour each morning, keeps review regular and stops it from being postponed to the end of the iteration.
- **Rotate a main reviewer** — one person per sprint carries a reduced delivery workload and takes first look at every request, pulling in extra reviewers based on their workload and expertise.
- **Run static analysis first** — [SonarQube](https://www.sonarsource.com/products/sonarqube/) or [Codacy](https://www.codacy.com/) catch style and defect patterns automatically, leaving reviewers the higher-level concerns.
- **Run tests first** — a branching strategy plus a [CI/CD](03-ci-cd.md) pipeline ensures only code that has already passed automated checks reaches a reviewer.
- **Use the tools reviewers already have** — the [GitHub](https://docs.github.com/en/pull-requests) and [GitLab](https://docs.gitlab.com/) web interfaces and IDE plugins for VS Code and JetBrains let reviewers highlight changes, mark checked sections, and add inline notes.

## Giving Feedback

- **Comment on the code, not the author** — keep feedback about the change itself, especially when the point is contentious.
- **Own subjective opinions** — phrase a preference as your own view rather than as fact.
- **Give the reason** — state why something is a concern, so the author can weigh it instead of only being told it is wrong.
- **Ask instead of accusing** — a question opens a conversation, an accusation closes it.
- **Drop dismissive phrasing** — "it's obvious" and "why didn't you check" read as judgments; neutral wording makes the same point.
