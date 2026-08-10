# Code Quality — Key Insights

## Core Concept
Teams rarely get enough time for code quality, so code becomes messy and buggy. Caring about quality from day one cuts the time to understand code, cuts defects, and improves the odds the project succeeds.

## Two Dimensions

- **Functional quality** — what the code *does*: does it meet requirements? Checked by unit and functional tests.
- **Structural quality** — how the code *looks*: clean, no extra detail, follows project guidelines. Checked by static analysis and code review.

## What Good Structural Code Looks Like
- **Clear**: others can read and edit it. A peer review confirms this.
- **Easy to maintain**: if a change takes long, maintainability wasn't considered. Simple code is easier to extend.
- **Follows project guidelines**: shared rules agreed early keep many developers consistent.
- **Testable**: small, independent behaviors that automated tests can verify. Otherwise thorough testing is impractical.

## Why It Matters

**High quality:**
- Easy-to-edit code saves developer time.
- Fewer defects.
- The code works.
- Faster onboarding.

**Poor quality:**
- Takes longer to understand, so changes are more likely to be wrong.
- New features cost more.
- Code may need a full rewrite.
- More defects.

## Maintainability
Maintainability is how easily code can be understood, modified, or extended. Code that follows project standards is easier to find, reuse, and update — a large time saving over a project.

## The Cost of Bugs
Bugs can do serious damage. In 1996 the EU's Ariane 5 rocket spun out of control 40 seconds after liftoff due to a software failure — roughly $500 million lost.

Fixing a defect is more than the fix: reproduce, register, assign, discuss, fix, verify. That can total over an hour for a single defect.

The cost of a fix grows sharply the later it is found (Empirical Software Engineering Journal / NIST): ~1x at Requirements, ~5x at Development, ~15x at Testing, ~30x at Maintenance. EPAM sees the same pattern. Find defects early.

## Two Supporting Practices

### 1. Coding Standards
Standards are agreed guidelines for style, practices, and methods. Agreeing up front sets clear expectations. As Harold Abelson put it, "programs are meant to be read by humans and only incidentally for computers to execute."

They improve clarity, readability, consistency, maintainability, and reduce complexity.

Three parts:
- **Style guide** — visual layout: indentation, whitespace, capitalization, naming style, comments.
- **Coding principles** — structure: language construct usage (exception handling, goto/break), logical structure (method size, parameter count, naming), and design principles like SOLID and KISS.
- **Project conventions** — project-specific rules that extend or override the above: implementation guidance, feature rules, naming patterns, DOs and DON'Ts. Useful for onboarding.

### 2. Automated Code Analysis
Automated analysis checks code against a rule set without manual effort, catching security issues, duplication, and style violations at scale. It runs statically, without executing the app; some tools flag violations as you type.

SonarQube is an open-source platform for continuous inspection (Java, C#, C/C++, and more) and is EPAM's recommendation for every project. IntelliJ IDEA and Visual Studio also help.

Limits: no business context, can't verify specific requirements, can't catch architecture or design problems tied to developer intent.

## Metrics
Quality judgments are subjective; metrics make them objective and surface risk early.
- **Cyclomatic complexity** — number of decision points. Higher = more complex.
- **Class coupling** — how many other classes a class depends on. Lower = more reusable and maintainable.
- **Depth of inheritance tree** — how deeply classes derive from others. Deeper = more complex.
- **Code duplication** — repeated code sequences. Hard to maintain, since updates can miss copies.
- **Method cohesion** — do a class's methods serve one clear purpose? Low cohesion gives large, confusing classes.

## Best Practices
- Write coding standards everyone follows.
- Keep a current coding-standards section in the knowledge base.
- Include standards in onboarding for every newcomer.
- Enforce them with static analysis and style checkers.
- Extend the tool's default rules with custom ones as needed.
- Keep CI quality gates green — never let them stay broken.
- Measure metrics regularly and act where any metric falls short.
