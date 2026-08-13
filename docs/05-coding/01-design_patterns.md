---
type: Guide
title: Design principles
description: Catalogs core software design principles (encapsulation, DRY, SoC, and more) and the SOLID principles of object-oriented design.
tags: [coding, design-principles, solid]
---

# Design principles

**`Component`** := A named piece of code that can be combined with others to build larger components.

**`Composability`** := Ability of code to be combined into new, more complex code.

Composability is the state of the art: system design should follow correct
Contracts around Separation, Ownership, and Responsibility.

| Principle | Description |
| ----------- | ------------- |
| **Encapsulation** *(high cohesion)* | Own the cohesive state necessary and sufficient for the duty |
| **Server, not Service** *(low coupling)* | Communicate with outer context via pre-defined Contract in loosely coupled way |
| **Abstraction Principle (DRY)** | Every piece of knowledge has a single, unambiguous representation — each significant piece of functionality is implemented in just one place |
| **Single Level of Abstraction (SLAP)** | Operate on well-defined glossary concepts providing a single layer of abstraction, do not mix layers |
| **Delegation** | Focus on one whole thing, delegate all other outside |
| **Separation of Concerns (SoC)** | Separate program into distinct features with minimal overlap |
| **GRASP** | General Responsibility Assignment Software Patterns (includes Low Coupling and High Cohesion) |
| **Inversion of Control** | Custom code receives flow of control from a generic framework — "Don't call us, we'll call you" (Hollywood Principle) |
| **Uniform Access Principle** | All services should be available through uniform notation |
| **Principle of Least Astonishment** | Component should behave as most users expect it to |
| **Law of Demeter** | A method should only call methods of its immediate collaborators |
| **80:20 Rule** | Focus on the 20% that produces 80% of results |
| **KISS Principle** | Keep It Simple, Stupid |
| **Worse is Better** | Simple implementation is more important than complete functionality |
| **YAGNI** | You Aren't Gonna Need It — don't implement until necessary |
| **Rule of Least Power** | Use the least powerful language suitable for the purpose |

## SOLID Principles of object-oriented design 

SOLID principles aim to reduce module changes to addition and removal, supporting deferring technical decisions and dividing labor.

| Letter | Principle | Description |
| -------- | ----------- | ------------- |
| **S** | Single Responsibility | An entity should be concerned with only one function; should have only one reason to change from a single business role |
| **O** | Open/Closed | An entity should be open for extension, but closed for modification |
| **L** | Liskov Substitution | A typed object should be replaceable with instances of their subtypes without altering correctness |
| **I** | Interface Segregation | Make fine-grained interfaces that are client specific |
| **D** | Dependency Inversion | One should depend upon abstractions, not concretions; Dependency Injection is its common implementation |

