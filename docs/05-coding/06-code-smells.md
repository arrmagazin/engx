---
type: Guide
title: Code Smells
description: Catalogs the code smells worth naming in review, with the published catalog or taxonomy each group comes from.
tags: [coding, code-smells, code-quality]
---

A code smell is a pattern on the surface of the source that points at a deeper design problem: the code runs, but the next change costs more than it should. Smell count and density are standard signals of [technical debt](../04-development-process/08-technical-debt.md). The catalog below names the smells worth calling out in review, grouped by the source each set comes from.

## The Refactoring Catalog

Martin Fowler and Kent Beck cataloged these smells in *Refactoring* (1999). The names are theirs; the split into class and method level is adapted from Wikipedia's [Code smell](https://en.wikipedia.org/wiki/Code_smell) article (CC BY-SA 4.0).

### Class-Level Smells

Large Class (God Object)
: A class carrying so many fields and methods that no single responsibility describes it

Feature Envy
: A method that uses the data of another class more than the data of its own

Inappropriate Intimacy
: Two classes that depend on each other's internal details

Refused Bequest
: A subclass that takes on inherited methods or data and then ignores or rejects most of them

Lazy Class
: A class that does too little to justify its existence

Duplicated Code
: The same knowledge expressed in more than one place, so a change has to be made in each of them

Shotgun Surgery
: One conceptual change that forces many small edits spread across many classes

Duplicated Code is the observable form of a broken [Single Source of Truth](04-design-principles.md#single-source-of-truth-ssot); the principle names the rule, this catalog names the symptom.

Refused Bequest is not the same as a subclass that overrides a method and breaks the contract of its base class; that is a violation of the Liskov Substitution Principle, covered in [Design Principles](04-design-principles.md).

### Method-Level Smells

Long Parameter List
: A method signature taking so many arguments that call sites are hard to read and test

Long Method
: A method that has grown too large to read as one thought

## Design Smells

Girish Suryanarayana, Ganesh Samarthyam, and Tushar Sharma define design smells in *Refactoring for Software Design Smells* (2014), grouped by the principle each one violates: abstraction, encapsulation, modularization, and hierarchy. The entries below are a selection from the first three groups, not the full taxonomy.

Missing Abstraction
: Raw values, such as groups of fields or strings with coded meaning, standing in for a type the design never created

Multifaceted Abstraction
: One class or type that has been given several unrelated jobs

Duplicate Abstraction
: Two or more types that share a name, share their code, or both

Deficient Encapsulation
: Members left more visible to outside code than the design needs, such as public fields that could be private

Unexploited Encapsulation
: Client code that branches on an object's type when the class hierarchy could handle the difference through polymorphism

Broken Modularization
: Fields and the methods that use them living in different classes, when they belong together in one

Insufficient Modularization
: A class or module so large or complex that it should have been split further

Cyclically-dependent Modularization
: A loop of dependencies among abstractions, whether two refer to each other or a longer chain closes back on itself

## Other Smells

Smells common in review that neither catalog above names. Names follow Wikipedia's [Code smell](https://en.wikipedia.org/wiki/Code_smell) article; definitions are this book's own.

### Readability Smells

Excessive Use of Literals (Magic Numbers)
: A number or string written straight into the code, where a named constant or a resource entry would say what it means

Excessively Short Identifiers
: A name cut down so far that the reader must guess what it holds, in a scope too large for the guess to be safe

Excessively Long Identifiers
: A name that repeats what its scope, type, or namespace already tells the reader

### Design Smells

Contrived Complexity
: Extra layers or patterns added where a direct solution would work just as well

Spaghetti Code
: Control flow so tangled that reading the code does not reveal its structure

Excessive Return of Data
: A method that hands back more data than any caller uses

Cyclomatic complexity is a metric rather than a smell; see [Code Quality](07-code-quality.md) for it and the other measures that make these problems visible.
