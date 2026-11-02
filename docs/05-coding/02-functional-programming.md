---
type: Guide
title: Functional Programming
description: Defines functional programming's core terms—purity, composition, and evaluation strategy—for engineers reading or writing it.
tags: [coding, programming-paradigms, functional-programming]
---

This guide continues [Programming Paradigms](01-programming-paradigms.md) with functional programming: a paradigm that treats computation as the declarative composition of pure (mathematical) functions.

## Functions and Purity

Operation
: Correspondence of input with unambiguous output: (x..., y1) & (x..., y2) => y1 ≡ y2

Parameter
: Reference to an elementary piece of the input data structure, by name or index

Argument
: Input data value applied to the corresponding `Parameter` when an Operation is performed

Function
: Operation mapping elements of a domain to elements of a codomain

Arity
: Dimension of the domain space: unary, binary, n-ary, variadic

Partial Function
: Mapping not defined for every value of its domain

Deterministic Function
: Mapping that always produces the same result for the same input

Pure Function
: Deterministic Function without side effects

Side Effects
: Interactions (reads or writes) with external mutable state

Higher-Order Function (HOF)
: Function that takes a function as argument, returns a function, or both

Immutability
: Inability to destructively change input parameters, context, or state

Idempotent
: Property of an operation whose reapplication to its own result changes nothing; see [System Design Glossary](../03-system-design/01-common-concepts.md)

## Function Composition

Function Pipe
: Chain of functions in which each output is the input of the next

Fun-Arg Problem
: Difficulty of keeping a function's free variables alive after the scope that defined them has returned

Closure
: Function retaining a reference to its free variables from the outer scope

Point-Free Style
: Defining functions without naming the arguments they use

Partial Application
: Creating a new function by pre-filling some arguments of the original

Currying
: Transformation of an n-ary function into a chain of unary functions, each taking one `Argument`

Auto Currying
: Transforming a multi-argument function so that, given fewer arguments, it returns a function taking the rest

Fixed-point Combinator
: Function Y returning the fixed point of its argument function: Y(f) == f(Y(f))

## Evaluation Strategy

Evaluation order is independent of the paradigm: Haskell is lazy by default, while Standard ML, OCaml, Scheme, Clojure, and Erlang are strict.

Lazy Evaluation
: Call-by-need strategy that defers computing an expression until its value is demanded, allowing infinite data structures

Continuation
: The part of code yet to be executed at any given point

Memoization
: Cache of previously computed results, reused instead of recomputing

Recursion
: Function calling itself during execution

Tail Recursion
: Recursion whose recursive call is the last step of the function, so a compiler that eliminates tail calls can run it as a loop

*See also*: [Programming Paradigms](01-programming-paradigms.md) · [Reactive Programming and FRP](03-reactive-programming.md)
