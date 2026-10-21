---
type: Guide
title: Automated Testing
description: Covers the automated test suite — feedback time and determinism, where tests run, test data, and metrics and reporting.
tags: [testing, automation, qa, development-process]
---

This guide covers the automated suite as part of the QA strategy: what makes it worth having, where it runs, the data it needs, and how its results are measured and reported. How QA is organized is in [Quality Assurance](04-quality-assurance.md); how individual tests are written is in [Testing](05-testing.md).

Automation speeds up repetitive verification, removes the human error of running the same steps for the fiftieth time, and frees testers for the exploratory work only a person can do. It is not free: it costs maintenance, environment upkeep, training, and framework setup. Scaling a suite blindly raises all four costs with no guarantee of quality — suite size is not evidence about the product.

## Feedback Time and Determinism

Two attributes decide whether an automated suite is worth having. They reinforce each other, and both are about whether people believe the result.

- **Feedback time** — the faster a suite reports, the sooner defects are fixed and the more developers trust it enough to run it. A unit suite should finish in seconds.
- **Determinism** — a good test returns the same result for the same code every time. Flaky tests erode trust in the whole suite and can hide a real defect behind a failure everyone assumes is noise.

See [Running Tests in CI](05-testing.md#running-tests-in-ci) for how this plays out in a pipeline gate.

## Where Tests Run

Verification runs at every stage of the [CI/CD environment pipeline](03-ci-cd.md) — Local → Development → Staging → Production:

- unit tests before the commit
- automated integration and regression suites in Development
- manual exploratory testing and user acceptance testing (UAT) in Staging

This is shifting left in practice, and the arithmetic is simple: the cost of a missed defect and the cost of verifying it both rise the later it is caught, while the number of defects remaining should fall. So catching a defect earlier is cheaper twice over.

The [Testing Pyramid](04-quality-assurance.md#testing-pyramid) applies to the automated suite as much as to testing as a whole, with a thin layer of manual exploratory testing on top. The common failure is overusing UI-level automation: it produces suites that are slow, fragile, and in the end ignored.

## Test Data

An automated suite needs reliable data, from one of three approaches: generate the data per test, maintain a dedicated, backed-up test database, or run ingestion and preparation scripts. Whichever is chosen, the data must be reloadable and cleaned up after the run — a suite that only inserts bloats the database and slows itself down until it is abandoned.

## Metrics and Reporting

Measures worth tracking for the automated suite:

- the share of production bugs that gain a new automated test
- the share of developers writing tests
- code coverage, as a presence indicator rather than a quality guarantee — [Coverage Types](05-testing.md#coverage-types) covers what a coverage percentage does and does not prove
- test coverage, as the ratio of automated to total manual cases
- the flaky-test count, with a target of zero

Results must be readable to be acted on: consolidated by build or version, clear enough for a non-engineer, and open to everyone, not only to whoever opened the pipeline. In practice: a dashboard showing version, changelog, results, and links to drill into a failure.

**Practices:**

- Make automation part of the test strategy rather than a side project, and automate regression within the sprint that created it.
- Hold automated test code to the same standard as production code; it is maintained for just as long.
- Run full suites at least weekly and regression suites daily.
- Gate the CI/CD pipeline with automated smoke tests, so a broken build stops before it reaches anyone.
- Use production-like test data, since defects that appear only at real data volumes appear at no other.
- Apply the Testing Pyramid, and revisit the shape as the system changes.
