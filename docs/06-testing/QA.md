# Quality Assurance 

- QA is a full process (mostly run by test engineers) that gives confidence a product meets client/user expectations; 

it costs time/money/resources, so its value must be actively communicated to stakeholders.

## 1. QA Overview
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

## 2. Test Case Management
**Building blocks:** Test Case (single verification) → Test Suite (group of cases, e.g. sanity/smoke/regression/UI/performance/API testing) → Test Plan (full scope/timeline).
- Good test case fields: ID, priority, title, description, steps, prerequisites, test data, expected result, requirement ID, environment, comments, defect ID, automation status.

**Design techniques:** Boundary Value Analysis, Equivalence Partitioning, Decision Table Testing, State Transition Diagrams, Use Case Testing, KISS principle.

**Life cycle & quality control**
- Test case life cycle: analyze requirements → set up environment/tools → write & self-review → map requirements → peer review → (automate) → execute → regression → retire/merge duplicates.
- Review types: self-review (vs. SRS/FRD), peer review (maker-checker), supervisor review.
- Common defects in test cases to watch for: missing coverage, spelling/grammar, non-standard templates, jargon, duplication, obsolescence.
- Track coverage via a Requirement Test Coverage Report or Requirement Traceability Matrix.
- Regression suites: categorize (reusable vs. obsolete) → prioritize by business impact → select cases covering critical/frequent/core/recently-changed functionality.
- Recommended tools: Zephyr, Rally, Azure DevOps, TestRail, Jama, QaSpace (EPAM's own).

**Best practices:** design cases as discrete verifiable actions; use one specialized tool; prioritize/order regression execution; organize into suites; trace every case to a requirement; have BAs review cases.

## 3. Defect Management
**Core process (Defect Management Process):** Discovery → Triage (priority/severity set, duplicates & change requests filtered out) → Resolution (root cause analysis) → Verification → Closure → Reporting.
**Defect Life Cycle (status flow):** Open → In Progress → (Blocked) → Resolved → Verified → Closed (or Reopened if verification fails).

**Classification**
- Priority (business urgency): Low / Medium / High / Critical.
- Severity (technical impact): Trivial / Minor / Major / Critical / Blocker. Priority and severity can conflict.

**Root Cause Analysis (5 steps):** form a team → define the problem → determine root cause → act on it → prevent recurrence. Common causes: human error, organizational confusion (vague instructions, poor task assignment), mechanical/system failures.

**Production bugs workflow:** stay calm → reproduce → gather info → find cause → set a resolution timeframe → verify fix → analyze root cause (weighted more heavily than internal defects) → prevent recurrence.

**Metrics:** defect containment (target ≥95%), defect rejection ratio, created-vs-resolved trend, quality debt (deferred-fix backlog risk).

**Best practices:** one specialized defect tool (Jira/Bugzilla/Azure DevOps/Rally); link defects to user stories; standard severity/priority definitions and workflow; resolve high/critical defects within the iteration; regular triage meetings; separate defects from change requests; consistent defect submission template; recurring root cause analysis and metrics reporting.

## 4. Testing of Non-Functional Requirements
- Functional = what the system does (mandatory); Non-functional = how well it does it (performance, usability, scalability, etc. — often negotiable against time/cost).
- Non-functional testing process (5 steps): Planning → Preparation → Test Execution → Record → Analysis & Improvement — vs. 4 steps for functional testing; results need interpretation rather than a simple pass/fail.
- Categories to evaluate with stakeholders: compatibility, performance, capacity, security, reliability/availability, scalability, maintainability, usability, accessibility (150+ possible types exist — pick what's relevant).
- Performance testing sub-types: load, endurance, volume, scalability, spike, stress testing.
- Should be integrated continuously into the SDLC (shift toward automation) rather than left to the end — most non-functional testing (except usability/accessibility) needs automation tools (e.g., JMeter, LoadRunner).

**Best practices:** test non-functional requirements every release; factor results into go/no-go release decisions; automate them; include them in CI/CD; define quality attributes quantitatively wherever possible.

## 5. QA Metrics
- Result metrics = absolute counts (test cases passed/failed/blocked, defects found/accepted/rejected, planned vs. actual hours, post-release bugs).
- Predictive metrics = derived ratios that flag risk early (e.g., defect containment efficiency, defect leakage, defect reopen ratio, rejection rate, test design efficiency).
- QA Metrics Life Cycle: Analyze (pick metrics that answer real questions) → Communicate (align data requirements with the team) → Evaluate (collect/automate data) → Report & Analyze (share findings against targets, e.g. defect containment >95%, test coverage 100%, invalid/reopen ratio <10%).
- PDCA cycle (Plan–Do–Check–Act) used to turn metrics into continuous process improvement.
- EPAM's PERF Board is cited as an example dashboard pulling data from Jira/Jenkins/SonarQube.

**Best practices:** measure metrics on a defined, automated schedule; always turn results into concrete improvement actions.

## 6. Automated Testing
**Value proposition:** speeds up repetitive verification, reduces human error, frees testers for exploratory work; costs include maintenance, environment upkeep, training, and framework setup — scaling tests blindly increases cost without guaranteeing quality.

**Two critical quality attributes of automated tests:**
- Feedback time — the faster a suite reports results, the sooner defects are fixed and the more developers trust/run it (e.g., unit tests should complete in seconds).
- Determinism — a good test always gives the same result for the same code; non-deterministic (flaky) tests erode trust and can mask real bugs.

**Test pipeline (shift left):** Local dev → Commit → Automated Testing → Manual Testing → UAT → Production. Cost of missed defects and verification cost both rise later in the pipeline while remaining defect count should fall — so catching issues as early as possible (shift left) is far cheaper.

**Testing Pyramid (balanced suite):** Unit → Integration → API → UI tests (bottom layers = fast/cheap/run often; top layers = slow/costly/narrower use), topped by manual exploratory testing. Overusing UI-level automation makes suites slow and fragile.

**Test data management:** either generate data per test, maintain a dedicated backed-up test database, or use ingestion/preparation scripts — and ensure data is reloadable/cleaned up to avoid database bloat and slow runs.

**Automated testing metrics:** PBCNT (% of production bugs that spawn new automated tests), PDWT (% of developers writing tests), code coverage (a presence indicator, not a quality guarantee), test coverage (automated vs. total manual test cases), and flaky-test count (target: zero).

**Reporting:** results should be consolidated (by build/version), transparent (readable by non-engineers), and available to all — typically via a dashboard (version, changelog, results, drill-down links).

**Best practices:** make automation core to the test strategy; automate in-sprint regression; hold automated code to the same standards as production code; run full suites at least weekly and regression suites daily; gate CI/CD with automated smoke tests; use production-like test data; apply and regularly revisit the Testing Pyramid.

## Cross-Cutting Patterns Across the Module
- Every QA discipline follows the same rhythm: define/plan → execute → capture data/metrics → review → improve (STLC, Defect Life Cycle, Non-Functional testing steps, QA Metrics Life Cycle, PDCA all mirror this pattern).
- Documentation (test plan/strategy, test reports, defect reports, dashboards) is treated as a first-class deliverable throughout — not an afterthought.
- Shift-left and automation-first thinking recur in test case management (reusability), defect management (early discovery), non-functional testing (continuous integration), and automated testing (the pipeline itself).
- Nearly every lesson closes with an Evolving Engineering Excellence best-practices checklist — these together form EPAM's baseline QA standard for project teams.
