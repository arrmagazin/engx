# Unit Testing

## Core definition
- A unit test is code that asserts one or more conditions to verify another piece of code behaves as expected, in isolation, without running the full application.
- Without unit tests: no rapid feedback loop, regression bugs leak to QA or end users.

## Why it matters (maintainability)
- Maintainability = ability to change, understand, and test code easily; unit tests directly support all three.
- Early in a project, coding without tests is faster; as the codebase grows, cost of change without tests rises and eventually exceeds the cost of maintaining tests — the two effort curves cross, after which tests pay off.

## Benefits
- More confidence changing code: tests act as a "contract" of existing behavior, letting you safely rework/refactor structure.
- Better understanding of component functionality: tests document edge cases/branches the human brain can't hold in memory.
- Better design: writing testable code forces lower coupling, cleaner interfaces.

## Cost of neglecting tests
- Empirical claim: "77% of the failures can be reproduced by a unit test" (OSDI '14 study) — most production failures are catchable at unit level.
- "Legacy code is code without tests" (Feathers) — skipping tests turns fresh code into unmaintainable legacy code quickly.
- Exceptions where unit tests may be skippable: throwaway POCs/demos, projects under ~3 months.

## Testing Pyramid
- Layers (bottom→top): Unit → Integration → UI/E2E tests. Width = test count, height = scope/complexity/instability.
- Unit tests: narrowest scope, cheapest, fastest, most numerous.
- Integration tests: verify interaction between components/systems (with or without network).
- UI/E2E tests: broadest scope, slowest, most expensive, most fragile.
- Principle: verify everything at the lowest level possible; push tests down the pyramid.
- Practical rules: keep short feedback cycles; run the unit test suite on every code addition (fail fast, cheap fixes).

## Unit vs. Integration tests
- Unit: isolated, no external dependencies (mocked/stubbed), fast/cheap, pinpoints exact faulty code.
- Integration: involves real external dependencies (DB, network, hardware), slower/costlier, only narrows fault to a module/component.

## F.I.R.S.T. principles (Robert Martin)
- Fast — full suite runs in seconds; slow tests get run less often, defeating their purpose.
- Independent — no test depends on another's state; must be runnable in any order.
- Repeatable — same result in any environment (dev machine, CI, prod-like); flaky-by-environment = design flaw.
- Self-Validating — binary pass/fail, no manual log inspection; non-deterministic (flaky) tests erode trust in the whole suite.
- Timely — written before or alongside production code, not after (retrofitting requires refactoring already-"working" code).

## Other quality attributes
- Maintainable — test code held to same quality bar as production code; messy tests become a liability.
- Isolated — no dependency on DB/filesystem/network/env config; external dependencies cause false failures unrelated to the code under test.
- Properly Targeted — focus on the core domain logic, not trivial/incidental code.

## Code coverage metric
- Coverage = (lines executed during tests) / (total lines).
- Useful for: tracking macro trend, spotting untested areas.
- Limitation: measures execution, not verification — a suite with 99% coverage and zero assertions proves nothing. 100% coverage ≠ quality guarantee.

## Common myths, rebutted
- "Can't unit test legacy code" — false; legacy code can be incrementally refactored into testable code.
- "Unit testing is expensive" — empirical counter: ~62–91% fewer defects for ~15–35% more dev time (Microsoft study).
- "Production urgency excludes testing" — under urgent/no-regression-time conditions, unit tests are often the only feasible safety net.
- "Testing can be done separately from implementation" — like input validation, bolting it on later requires reworking already-shipped code (tech debt).
- "Production code matters more than test code" — test code quality directly gates production code maintainability; treat both equally.

## Best practices
- Write unit tests as part of the same task/story as the production code, not as a separate phase.
- Enforce F.I.R.S.T. principles.
- Wire test execution into CI; fail the build on test failure.
- Track code coverage in CI to flag under-tested areas (not as a quality proof).

## Scenario reinforcement (TravelerWorks case)
- Untested code causes cascading regressions: fixing one bug re-breaks a previously "working" unrelated feature — classic symptom of missing isolation/coverage.
- Stakeholder objection ("tests waste dev time") is addressed by reframing: cost shifts from maintenance-phase firefighting to development-phase investment; net time balances out over the release cycle.
- Under production-urgency pressure, the tension between "ship now" vs. "write tests" is resolved by still writing tests around the fix — not skipping them for speed.
- Overly complex/mocked tests that fail for unclear reasons signal an Isolated/FIRST violation — fix by isolating a single assertion, splitting given-when-then, and removing unnecessary mocking.
- Tests hitting a real local DB but failing in CI signal missing isolation — external-dependency tests need a dedicated test DB, data cleanup after each run, and independence between tests to avoid slow/flaky suites.
- Team's final robust-test checklist: whole suite runs in seconds, zero external dependencies, F.I.R.S.T.-compliant, same quality bar as production code, present on every mid/long-term project, built into the implementation task (not estimated separately), and run continuously in CI.
