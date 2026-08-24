---
type: Guide
title: Coding
description: Covers how code is written and how it is judged — paradigms, design principles, patterns, smells, and quality.
tags: [coding, design-principles, design-patterns, code-quality]
---

# Coding

![Coding](../../images/06-coding.svg)

This section covers how code is written and how it is judged. It serves the developer making structural decisions in an editor, rather than the architect choosing between systems.

---

## In This Section

| Doc | What it covers |
| --- | --- |
| [Programming Paradigms](01-programming-paradigms.md) | Imperative, object-oriented, declarative, functional, and reactive programming, plus metaprogramming |
| [Design Principles](02-design-principles.md) | Technology-agnostic heuristics for structural decisions, including SOLID, GRASP, DRY, and SSOT |
| [Design Patterns](03-design-patterns.md) | Structural, creational, behavioral, and concurrency patterns, plus a catalog of anti-patterns |
| [Code Smells](04-code-smells.md) | Naming, application, class, method, and design smells to watch for during review |
| [Code Quality](05-code-quality.md) | Functional and structural quality, the practices that protect it, and the metrics that measure it |

---

## Where Each Idea Lives

Four of these docs describe overlapping ground. Each term has one home; everywhere else it is linked rather than explained again.

| Boundary | Rule |
| --- | --- |
| **Principle vs. OOP pillar** | A design principle is a language-agnostic heuristic and applies whether or not the language has objects, so it lives in [Design Principles](02-design-principles.md). Abstraction, encapsulation, inheritance, and polymorphism are properties of the object model itself and live in [Programming Paradigms](01-programming-paradigms.md) |
| **Anti-pattern vs. smell** | An anti-pattern names a solution people choose that reliably ends badly, and belongs in [Design Patterns](03-design-patterns.md). A smell names a symptom in code that already exists and points at a deeper problem, and belongs in [Code Smells](04-code-smells.md) |
| **Metric vs. smell** | A metric is a number computed from the code, such as cyclomatic complexity or class coupling, and lives in [Code Quality](05-code-quality.md). A smell is a pattern a reader recognizes. A metric can point at a smell; it is not one |
