---
type: Guide
title: Code Smells
description: Catalogs the code smells worth naming in review, with the published catalog or taxonomy each group comes from.
tags: [coding, code-smells, code-quality]
---

# Code Smells

A code smell is a pattern on the surface of the source that points at a deeper design problem: the code runs, but the next change to it costs more than it should. Smell count and density are one of the standard signals of [technical debt](../04-development-process/07-technical-debt.md). The catalog below names the smells worth calling out in review, grouped by the work each set comes from.

## The Refactoring Catalog

Martin Fowler and Kent Beck cataloged these smells in *Refactoring* (1999). The names are theirs; the split into class and method level is this page's.

### Class-Level Smells

Large Class (God Object)
: A class carrying so many fields and methods that no single responsibility describes it

Feature Envy
: A method more interested in another class's data than in its own

Inappropriate Intimacy
: Two classes that depend on each other's internal details

Refused Bequest
: A subclass that inherits methods and data it neither wants nor uses

Lazy Class
: A class that does too little to justify its existence

Duplicated Code
: The same knowledge expressed in more than one place, so a change has to be made in each of them

Shotgun Surgery
: One conceptual change that forces many small edits spread across many classes

Duplicated Code is the observable form of a broken [Single Source of Truth](02-design-principles.md#single-source-of-truth-ssot); the principle names the rule, this catalog names the symptom.

Refused Bequest is not the same as a subclass that overrides a method and breaks the contract of its base class; that is a violation of the Liskov Substitution Principle, covered in [Design Principles](02-design-principles.md).

### Method-Level Smells

Long Parameter List
: A method signature taking so many arguments that call sites are hard to read and test

Long Method
: A method that has grown too large to read as one thought

## Design Smells

Girish Suryanarayana, Ganesh Samarthyam, and Tushar Sharma define design smells in *Refactoring for Software Design Smells* (2014), grouped by the principle each one violates: abstraction, encapsulation, modularization, and hierarchy. The rows below are a selection from the first three groups, not the full taxonomy.

Missing Abstraction
: Clumps of data or encoded strings used where a class or type belongs

Multifaceted Abstraction
: An abstraction carrying more than one responsibility

Duplicate Abstraction
: Two abstractions with identical names or identical implementations

Deficient Encapsulation
: Declared accessibility of members wider than the design requires

Unexploited Encapsulation
: Explicit type checks used where polymorphism would carry the variation

Broken Modularization
: Data and the methods that operate on it split across separate abstractions

Insufficient Modularization
: An abstraction that carries too many members or too much complexity to stand undecomposed

Cyclically-dependent Modularization
: Two or more abstractions that depend on one another, directly or through a chain

## Other Smells

Smells in common use during review that neither catalog above names.

### Naming Smells

Excessively Long Identifiers
: A name padded with qualifiers that the scope, type, or namespace already supplies

Excessively Short Identifiers
: A name too abbreviated to say what it holds, outside a scope small enough to make it obvious

Excessive Use of Literals (Magic Numbers)
: Numeric or string values written inline where a named constant or resource entry belongs

### Structure and Interface Smells

Spaghetti Code
: Control flow tangled enough that the structure cannot be followed by reading it

Contrived Complexity
: A pattern or layer of indirection applied where a direct solution would serve

Excessive Return of Data
: A method returning more data than any of its callers needs

Cyclomatic complexity is a metric rather than a smell; see [Code Quality](05-code-quality.md) for it and the other measures that make these problems visible.
