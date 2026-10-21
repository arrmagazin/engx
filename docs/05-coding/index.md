---
type: Guide
title: Coding
description: Covers how code is written and how it is judged — paradigms, design principles, patterns, smells, and quality.
tags: [coding, design-principles, design-patterns, code-quality]
---

This chapter covers how code is written and how it is judged. It serves the developer making structural decisions in an editor, not the architect choosing between systems.

---

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Programming Paradigms](01-programming-paradigms.md)** | Imperative, object-oriented, declarative, and functional programming, plus logic, constraint, and other specialized paradigms |
| **[Reactive Programming and FRP](02-reactive-programming.md)** | Reactive programming over data streams, operators and rate control, reactive systems, and functional reactive programming |
| **[Metaprogramming and AOP](03-metaprogramming.md)** | Code that reads, generates, or transforms code — its stages, techniques, and trade-offs — and aspect-oriented programming |
| **[Design Principles](04-design-principles.md)** | Technology-agnostic heuristics for structural decisions, including SOLID, GRASP, DRY, and SSOT |
| **[Design Patterns](05-design-patterns.md)** | Structural, creational, behavioral, and concurrency patterns, plus a catalog of anti-patterns |
| **[Code Smells](06-code-smells.md)** | Naming, application, class, method, and design smells to watch for during review |
| **[Code Quality](07-code-quality.md)** | Functional and structural quality, the practices that protect it, and the metrics that measure it |

---

## Where Each Idea Lives

Four of these docs describe overlapping ground. Each term has one home; everywhere else it is linked rather than explained again.

| Boundary | Rule |
| --- | --- |
| **Principle vs. OOP pillar** | A design principle is a language-agnostic heuristic that applies whether or not the language has objects; it lives in [Design Principles](04-design-principles.md). Abstraction, encapsulation, inheritance, and polymorphism are properties of the object model itself; they live in [Programming Paradigms](01-programming-paradigms.md) |
| **Anti-pattern vs. smell** | An anti-pattern names a solution people choose that reliably ends badly; it belongs in [Design Patterns](05-design-patterns.md). A smell names a symptom in existing code that points at a deeper problem; it belongs in [Code Smells](06-code-smells.md) |
| **Metric vs. smell** | A metric is a number computed from the code, such as cyclomatic complexity or class coupling, and lives in [Code Quality](07-code-quality.md). A smell is a pattern a reader recognizes. A metric can point at a smell; it is not one |

Code is also judged outside the editor: against the standard it is written to, in the review that applies that standard, and in the record of what was knowingly left below that standard.

Outside this folder: [Software Engineering Standards](../00-software-engineering/02-standards.md) · [Code Review](../04-development-process/02-code-review.md) · [Technical Debt](../04-development-process/08-technical-debt.md)
