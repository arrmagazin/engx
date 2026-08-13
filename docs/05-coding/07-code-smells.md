---
type: Guide
title: Code Smells
description: Catalogs naming, application-, class-, method-, and design-level code smells to watch for during review.
tags: [coding, code-smells, code-quality]
---

# Code Smells

### Naming Conventions

| Smell | Description |
| ------- | ------------- |
| **Excessively Long Identifiers** | Using naming conventions for disambiguation that should be implicit |
| **Excessively Short Identifiers** | Names should reflect function unless obvious |
| **Excessive Use of Literals** | Should be coded as named constants; externalize to resource files |

### Application-Level Smells

| Smell | Description |
| ------- | ------------- |
| **Spaghetti Code** | Structure barely comprehensible due to misuse of code structures |
| **Duplicated Code** | Identical or similar code in more than one location |
| **Contrived Complexity** | Forced usage of overcomplicated design patterns |

### Class-Level Smells

| Smell | Description |
| ------- | ------------- |
| **Large Class (God Object)** | A class that has grown too large |
| **Feature Envy** | A class using methods of another class excessively |
| **Inappropriate Intimacy** | A class depending on implementation details of another |
| **Refused Bequest** | A class overriding methods that break the base class contract |
| **Lazy Class** | A class that does too little |
| **Cyclomatic Complexity** | Too many branches or loops |

### Method-Level Smells

| Smell | Description |
| ------- | ------------- |
| **Too Many Parameters** | Hard to read, calling and testing complicated |
| **Long Method** | A method that has grown too large |
| **Excessive Return of Data** | Returning more than each caller needs |

### Design Smells

| Smell | Description |
| ------- | ------------- |
| **Missing Abstraction (Primitive Obsession)** | Using clumps of data or encoded strings instead of creating abstraction |
| **Multifaceted Abstraction** | Abstraction with multiple responsibilities |
| **Duplicate Abstraction** | Two or more abstractions with identical names or implementation |
| **Deficient Encapsulation** | Declared accessibility more permissive than required |
| **Unexploited Encapsulation** | Using explicit type checks instead of exploiting polymorphism |
| **Broken Modularization** | Data/methods that should be localized are separated |
| **Insufficient Modularization** | Abstraction not completely decomposed |
| **Cyclically-dependent Modularization** | Two or more abstractions depend on each other |

### See also

- **Zen of Python**: Principles guiding Python design
- **Unix Philosophy**: Simple, modular, composable programs
- **List of Software Development Philosophies**: Various guiding principles
