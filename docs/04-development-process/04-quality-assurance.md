---
type: Guide
title: Quality Assurance
description: Covers QA process and vocabulary, test case and defect management, non-functional requirement testing, metrics, and test automation.
tags: [testing, qa, tdd]
---

# Quality Assurance

![Quality Assurance](../../images/08-testing.svg)

Quality assurance is the process, mostly run by test engineers, that gives confidence a product meets what clients and users expect. It costs time, money, and people, so its value has to be argued to stakeholders rather than assumed. This guide covers how QA is organized — test cases, defects, non-functional requirements, metrics, and automation; the practices that carry it out, including test principles, TDD, BDD, and unit testing, are in [Testing](05-testing.md).

## QA Overview

**Core distinctions**
- Quality Assurance (process-level, whole lifecycle) → Quality Control (product-level, resolves issues found) → Testing (verifies functionality/defect-free code). Testing is a sub-activity of QC, which is a sub-activity of QA.
- Quality attributes to evaluate: functionality, availability, performance, testability, security, usability, reliability.
- Error (developer mistake) → Defect/bug (code doesn't meet spec) → Failure (system can't function as intended).

**Testing types & methods**
- Manual vs. Automated testing (trade-offs: manual = flexible/slow/costly at scale; automated = fast/repeatable/needs upfront investment).
- Functional (what the system does) vs. Non-functional (how it does it).
- White box (internal structure), black box (interface only), grey box (hybrid, needs DB/design access).

**Process & practices**
- Software Testing Life Cycle (STLC): Requirement Analysis → Test Planning → Test Case Design → Test Environment Setup → Test Execution → Test Closure (not always strictly sequential).
- Key documentation: Test Plan (scope/schedule/resources — the what/when) and Test Strategy (approach/testing types — the how).
- Best practices: single documented test process; participate in planning/refinement/stand-up/retro; include test estimates in iteration planning; keep test plan & strategy updated; produce a test report per release; test non-functional requirements too.

### Testing Pyramid

Layers (bottom→top): Unit → Integration → UI/E2E tests. Width = test count, height = scope, complexity, and instability. The pyramid prescribes a shape, not a ratio: many fast unit tests, fewer integration tests, and a thin layer of end-to-end tests. The proportion that fits a given system is a team decision, not a constant.

- Unit tests: narrowest scope, cheapest, fastest, most numerous.
- Integration tests: verify interaction between components/systems (with or without network).
- UI/E2E tests: broadest scope, slowest, most expensive, most fragile.

| Level | Speed | Isolation | Purpose |
| --- | --- | --- | --- |
| **Unit Tests** | Milliseconds | Full | Component/function logic |
| **Integration Tests** | Seconds | Partial | Component interactions |
| **E2E Tests** | Minutes | None | User journeys |

- Principle: verify everything at the lowest level possible; push tests down the pyramid.
- Practical rules: keep short feedback cycles; run the unit test suite on every code addition (fail fast, cheap fixes).

### Unit vs. Integration Tests

- Unit: isolated, no external dependencies (mocked/stubbed), fast/cheap, pinpoints exact faulty code.
- Integration: involves real external dependencies (DB, network, hardware), slower/costlier, only narrows fault to a module/component.

## Test Case Management

**Building blocks:** Test Case (single verification) → Test Suite (group of cases, e.g. sanity/smoke/regression/UI/performance/API testing) → Test Plan (full scope/timeline).
- Good test case fields: ID, priority, title, description, steps, prerequisites, test data, expected result, requirement ID, environment, comments, defect ID, automation status.

**Design techniques:** Boundary Value Analysis, Equivalence Partitioning, Decision Table Testing, State Transition Diagrams, Use Case Testing, KISS principle.

**Life cycle & quality control**
- Test case life cycle: analyze requirements → set up environment/tools → write & self-review → map requirements → peer review → (automate) → execute → regression → retire/merge duplicates.
- Review types: self-review (vs. SRS/FRD), peer review (maker-checker), supervisor review.
- Common defects in test cases to watch for: missing coverage, spelling/grammar, non-standard templates, jargon, duplication, obsolescence.
- Track coverage via a Requirement Test Coverage Report or Requirement Traceability Matrix.
- Regression suites: categorize (reusable vs. obsolete) → prioritize by business impact → select cases covering critical/frequent/core/recently-changed functionality.

**Best practices:** design cases as discrete verifiable actions; use one specialized tool; prioritize/order regression execution; organize into suites; trace every case to a requirement; have BAs review cases.

## Defect Management

**Core process (Defect Management Process):** Discovery → Triage (priority/severity set, duplicates & change requests filtered out) → Resolution (root cause analysis) → Verification → Closure → Reporting.
**Defect Life Cycle (status flow):** Open → In Progress → (Blocked) → Resolved → Verified → Closed (or Reopened if verification fails).

**Classification**
- Priority (business urgency): Low / Medium / High / Critical.
- Severity (technical impact): Trivial / Minor / Major / Critical / Blocker. Priority and severity can conflict.

**Root Cause Analysis (5 steps):** form a team → define the problem → determine root cause → act on it → prevent recurrence. Common causes: human error, organizational confusion (vague instructions, poor task assignment), mechanical/system failures.

**Production bugs workflow:** stay calm → reproduce → gather info → find cause → set a resolution timeframe → verify fix → analyze root cause (weighted more heavily than internal defects) → prevent recurrence.

**Metrics:** defect containment (share of defects caught before release), defect rejection ratio, created-vs-resolved trend, quality debt (deferred-fix backlog risk).

**Best practices:** one specialized defect tool (Jira/Bugzilla/Azure DevOps/Rally); link defects to user stories; standard severity/priority definitions and workflow; resolve high/critical defects within the iteration; regular triage meetings; separate defects from change requests; consistent defect submission template; recurring root cause analysis and metrics reporting.

## Testing of Non-Functional Requirements

- Functional = what the system does (mandatory); Non-functional = how well it does it (performance, usability, scalability, etc. — often negotiable against time/cost).
- Non-functional testing process (5 steps): Planning → Preparation → Test Execution → Record → Analysis & Improvement — vs. 4 steps for functional testing; results need interpretation rather than a simple pass/fail.
- Categories to evaluate with stakeholders: compatibility, performance, capacity, security, reliability/availability, scalability, maintainability, usability, accessibility.
- Performance testing sub-types: load, endurance, volume, scalability, spike, stress testing.
- Should be integrated continuously into the SDLC (shift toward automation) rather than left to the end — most non-functional testing (except usability/accessibility) needs automation tools (e.g., JMeter, LoadRunner).

**Best practices:** test non-functional requirements every release; factor results into go/no-go release decisions; automate them; include them in CI/CD; define quality attributes quantitatively wherever possible.

## QA Metrics

- Result metrics = absolute counts (test cases passed/failed/blocked, defects found/accepted/rejected, planned vs. actual hours, post-release bugs).
- Predictive metrics = derived ratios that flag risk early (e.g., defect containment efficiency, defect leakage, defect reopen ratio, rejection rate, test design efficiency).
- QA Metrics Life Cycle: Analyze (pick metrics that answer real questions) → Communicate (align data requirements with the team) → Evaluate (collect/automate data) → Report & Analyze (share findings against the targets the team agreed, and drop targets that no longer change a decision).
- PDCA cycle (Plan–Do–Check–Act) used to turn metrics into continuous process improvement.

**Best practices:** measure metrics on a defined, automated schedule; always turn results into concrete improvement actions.

## Automated Testing

**Value proposition:** speeds up repetitive verification, reduces human error, frees testers for exploratory work; costs include maintenance, environment upkeep, training, and framework setup — scaling tests blindly increases cost without guaranteeing quality.

**Two critical quality attributes of automated tests:**
- Feedback time — the faster a suite reports results, the sooner defects are fixed and the more developers trust/run it (e.g., unit tests should complete in seconds).
- Determinism — a good test always gives the same result for the same code; non-deterministic (flaky) tests erode trust and can mask real bugs.

**Test pipeline (shift left):** verification runs at every stage of the [CI/CD environment pipeline](03-ci-cd.md) — Local → Development → Staging → Production — with unit tests before the commit, automated integration and regression suites in Development, and manual exploratory plus user acceptance testing (UAT) in Staging. The cost of a missed defect and the cost of verifying it both rise the later it is caught, while the remaining defect count should fall — which is what makes shifting left cheaper.

**Suite balance:** the Testing Pyramid above applies to the automated suite, topped by a thin layer of manual exploratory testing. Overusing UI-level automation makes suites slow and fragile.

**Test data management:** either generate data per test, maintain a dedicated backed-up test database, or use ingestion/preparation scripts — and ensure data is reloadable/cleaned up to avoid database bloat and slow runs.

**Automated testing metrics:** share of production bugs that gain a new automated test, share of developers writing tests, code coverage (a presence indicator, not a quality guarantee), test coverage (automated vs. total manual test cases), and flaky-test count (target: zero).

**Reporting:** results should be consolidated (by build/version), transparent (readable by non-engineers), and available to all — typically via a dashboard (version, changelog, results, drill-down links).

**Best practices:** make automation core to the test strategy; automate in-sprint regression; hold automated code to the same standards as production code; run full suites at least weekly and regression suites daily; gate CI/CD with automated smoke tests; use production-like test data; apply and regularly revisit the Testing Pyramid.
