---
type: Guide
title: Testing
description: Covers how tests are written — the F.I.R.S.T. principles, TDD and BDD, unit testing, test doubles, coverage types, and tests in CI.
tags: [testing, tdd, bdd, unit-testing]
---

# Testing

This guide covers the practice of writing tests: the principles a good test follows, the two test-first disciplines, unit testing, the vocabulary of test doubles, what a coverage number actually proves, and where suites run in a pipeline. How testing is organized and reported — test case management, defect management, non-functional testing, metrics, and the automation strategy — is in [Quality Assurance](04-quality-assurance.md).

## Testing Principles (F.I.R.S.T.)

| Concept | Definition |
| --- | --- |
| **Fast** | Runs in milliseconds, so the whole suite can run on every change without anyone waiting for it |
| **Independent** | Shares no state with any other test, and sets up and tears down whatever it needs |
| **Repeatable** | Produces the same result on every run, on any machine, in any order |
| **Self-Validating** | Reports its own pass or fail, with no human reading output to decide which it was |
| **Timely** | Written alongside the code it covers, in the same change or ahead of it under TDD |

**Best practices:**

- Test behavior, not implementation details
- Use descriptive names: `it('returns correct total when items are added')`
- Follow Arrange → Act → Assert
- One assertion per test where possible
- Mock external dependencies (APIs, databases, file system)

## Test-Driven Development (TDD)

Write a failing test first, make it pass with the simplest code that works, then improve the design. The test defines the contract before the implementation exists, so the code is testable by construction and no line ships without a test that was *seen* to fail.

```mermaid
graph LR
    R["Red — write a failing test"] --> G["Green — make it pass"]
    G --> F["Refactor — clean it up"]
    F --> R
```

| Step | Goal | Rule |
| --- | --- | --- |
| **Red** | Write the smallest test that expresses the next behavior | Run it and watch it fail — a test that never failed proves nothing |
| **Green** | Make it pass as directly as possible | No speculative features; duplication is acceptable at this step |
| **Refactor** | Improve naming, structure, and duplication | Tests stay green; no new behavior is added |

**Red** — the test fails because `total()` does not exist yet:

```ts
it('returns the total of all items in the cart', () => {
  const cart = createCart();
  cart.addItem({ id: 'sku-1', price: 10, quantity: 2 });
  expect(cart.total()).toBe(20);
});
```

**Green** — the simplest code that satisfies the test:

```ts
export const createCart = () => {
  const items: CartItem[] = [];
  return {
    addItem: (item: CartItem) => items.push(item),
    total: () => items.reduce((sum, i) => sum + i.price * i.quantity, 0),
  };
};
```

**Refactor** — extract, rename, and remove duplication once the test protects you.

**Practices:**

- Keep cycles short — minutes, not hours; a long red phase means the step was too big
- Let the test drive the API: if a test is awkward to write, the design is awkward to use
- Add a failing test for every bug before fixing it, so regressions stay caught
- Refactor only on green, and never mix a refactor with a behavior change
- Assert on observable behavior so refactoring does not break the suite

**Trade-offs:** TDD pays off most on logic with real branching — pricing, validation, state machines, reducers. It pays off least on exploratory spikes and purely visual markup, where the design is not yet stable enough for a test to pin down.

TDD and BDD are complements, not alternatives: BDD frames *what* the system should do for the user, TDD drives *how* each unit is built to get there.

## Behavior-Driven Development (BDD)

Describes expected behavior from the user's perspective using natural language.

```gherkin
Feature: User Login

Scenario: Successful login with valid credentials
    Given the user is on the login page
    When the user enters valid email "user@example.com"
    And the user enters valid password "password123"
    And clicks the login button
    Then the user is redirected to the dashboard

Scenario: Failed login
    Given the user is on the login page
    When the user enters invalid credentials
    Then the user sees an error message
```

## Unit Testing

A unit test is code that asserts one or more conditions to verify another piece of code behaves as expected, in isolation, without running the full application.

### Why It Matters

- Maintainability = ability to change, understand, and test code easily; unit tests directly support all three.
- Early in a project, coding without tests is faster; as the codebase grows, cost of change without tests rises and eventually exceeds the cost of maintaining tests — the two effort curves cross, after which tests pay off.
- More confidence changing code: tests act as a "contract" of existing behavior, letting you safely rework/refactor structure.
- Better understanding of component functionality: tests document edge cases/branches the human brain can't hold in memory.
- Better design: writing testable code forces lower coupling, cleaner interfaces.
- Yuan et al. (OSDI '14) sampled 198 user-reported failures across five distributed data-intensive systems and found 77% of them reproducible by a unit test. That is a finding about that class of system, not about production failures in general, but it sets a high bar for what unit tests can catch.
- "Legacy code is code without tests" (Feathers) — skipping tests turns fresh code into unmaintainable legacy code quickly.
- Exceptions where unit tests may be skippable: throwaway POCs/demos, projects under ~3 months.

### Qualities of a Good Unit Test

- Maintainable — test code held to same quality bar as production code; messy tests become a liability.
- Isolated — no dependency on DB/filesystem/network/env config; external dependencies cause false failures unrelated to the code under test.
- Properly Targeted — focus on the core domain logic, not trivial/incidental code.

### Common Myths, Rebutted

- "Can't unit test legacy code" — false; legacy code can be incrementally refactored into testable code.
- "Unit testing is expensive" — Nagappan, Maximilien, Bhat and Williams (2008) tracked four teams at Microsoft and IBM that adopted TDD and reported 40–90% lower defect density for 15–35% longer initial development time.
- "Production urgency excludes testing" — under urgent/no-regression-time conditions, unit tests are often the only feasible safety net.
- "Testing can be done separately from implementation" — like input validation, bolting it on later requires reworking already-shipped code (tech debt).
- "Production code matters more than test code" — test code quality directly gates production code maintainability; treat both equally.

### Unit Testing Practices

- Write unit tests as part of the same task/story as the production code, not as a separate phase.
- Enforce F.I.R.S.T. principles.
- Wire test execution into CI; fail the build on test failure.
- Track code coverage in CI to flag under-tested areas (not as a quality proof).

## Test Doubles

The five kinds below are Gerard Meszaros's taxonomy from *xUnit Test Patterns*. The names get used loosely in practice, and most mocking libraries produce whichever kind you configure, but the distinctions are what make a test's intent readable.

| Concept | Definition |
| --- | --- |
| **Test Double** | Any stand-in a test substitutes for a real collaborator so the code under test can run in isolation |
| **Dummy** | A value passed only to satisfy a signature, never called and never asserted on |
| **Fake** | A working implementation that takes a shortcut making it unfit for production, such as an in-memory store standing in for a database |
| **Stub** | A double that returns canned answers to the calls a test makes, supplying the input the code needs to reach the case under test |
| **Spy** | A double that records the calls it receives so the test can assert on them afterwards |
| **Mock** | A double preloaded with the calls it expects to receive, which fails the test itself when the code does not call it that way |

The line that matters is between the last three. A stub is about input — it feeds the code whatever it needs to reach the case under test, and asserts nothing. A mock is about verifying interaction — it carries an expectation of how it will be called and fails the test when that expectation is not met. A spy sits between them, recording calls without judging them, so the assertion stays in the test where a reader can see it.

Reach for a stub whenever the collaborator is only a source of data, and for a mock only when the call itself is the behavior under test — sending the email, publishing the event. Mocking what is merely incidental couples the test to the implementation and breaks it on every refactor.

## Coverage Types

Coverage tools report one percentage by default, and which of these it measures changes what the number proves.

| Concept | Definition |
| --- | --- |
| **Statement Coverage** | Share of executable statements the suite ran at least once |
| **Line Coverage** | Share of source lines executed; differs from statements only where one line holds several of them |
| **Branch Coverage** | Share of decision outcomes taken, so an `if` counts only once both the true and the false path have run |
| **Function Coverage** | Share of functions or methods entered at least once, the coarsest of the four |

Branch coverage is the one that catches an untested `else`. Statement and line coverage can read 100% while a conditional is only ever exercised one way, because every statement did run — just never with the other outcome. Function coverage is weaker still: it says a function was entered, not that anything inside it was checked.

None of them measure verification. A suite with 99% coverage and no assertions proves nothing, so 100% is not a quality guarantee — the number is worth tracking as a macro trend and for spotting untested areas, and no further. See [QA Metrics](04-quality-assurance.md#qa-metrics) for how it sits among the other measures a team reports.

## Running Tests in CI

Where a suite runs decides what it can be trusted to do. The pipeline stages themselves are in [CI/CD](03-ci-cd.md); what follows is the testing side of that boundary.

- **Gating suites** run on every push and must be fast — unit tests plus a thin smoke layer. A gate slower than a few minutes stops being a gate and becomes a queue, and people start pushing around it.
- **Scheduled suites** run nightly or on a cron — full regression, long-running integration, performance and load runs. They cover what a gate cannot afford to wait for, at the price of a slower feedback loop.
- **A flaky test in a gating suite is worse than no test.** It trains everyone to hit re-run instead of reading the failure, and once that reflex exists a genuine failure gets re-run too. Quarantine a flaky test out of the gate the day it is spotted, then fix or delete it.
- **The result needs to be a machine-readable artifact**, not only lines in the log. A structured report the pipeline can parse — JUnit XML is the usual interchange format — lets the build annotate the failing case, track flakiness across runs, and enforce a coverage threshold without a human reading output.
