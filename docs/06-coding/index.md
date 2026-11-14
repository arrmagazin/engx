---
type: Guide
title: Coding
description: Covers how code is written and how it is judged — design principles, patterns, smells, and quality.
tags: [coding, design-principles, design-patterns, code-quality]
---

This chapter covers how code is written and how it is judged. It serves the developer making structural decisions in an editor, not the architect choosing between systems.

---

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Design Principles](01-design-principles.md)** | Technology-agnostic heuristics for structural decisions, including SOLID, GRASP, DRY, and SSOT |
| **[Design Patterns](02-design-patterns.md)** | Structural, creational, behavioral, and concurrency patterns, plus a catalog of anti-patterns |
| **[Code Smells](03-code-smells.md)** | Naming, application, class, method, and design smells to watch for during review |
| **[Code Quality](04-code-quality.md)** | Functional and structural quality, the practices that protect it, and the metrics that measure it |

---

## Where Each Idea Lives

Four of these docs describe overlapping ground. Each term has one home; everywhere else it is linked rather than explained again.

| Boundary | Rule |
| --- | --- |
| **Principle vs. OOP pillar** | A design principle is a language-agnostic heuristic that applies whether or not the language has objects; it lives in [Design Principles](01-design-principles.md). Abstraction, encapsulation, inheritance, and polymorphism are properties of the object model itself; they live in [Programming Paradigms](../05-programming-paradigms/01-programming-paradigms.md) |
| **Anti-pattern vs. smell** | An anti-pattern names a solution people choose that reliably ends badly; it belongs in [Design Patterns](02-design-patterns.md). A smell names a symptom in existing code that points at a deeper problem; it belongs in [Code Smells](03-code-smells.md) |
| **Metric vs. smell** | A metric is a number computed from the code, such as cyclomatic complexity or class coupling, and lives in [Code Quality](04-code-quality.md). A smell is a pattern a reader recognizes. A metric can point at a smell; it is not one |

Code is also judged outside the editor: against the standard it is written to, in the review that applies that standard, and in the record of what was knowingly left below that standard.

Outside this folder: [Software Engineering Standards](../99-appendices/02-standards.md) · [Code Review](../04-development-process/02-code-review.md) · [Technical Debt](../04-development-process/08-technical-debt.md)
