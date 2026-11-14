---
type: Guide
title: Aspect-Oriented Programming
description: Defines aspect-oriented programming (AOP)—join points, pointcuts, advice, and weaving—and when its hidden behavior pays off.
tags: [coding, programming-paradigms, aop]
---

This guide continues [Metaprogramming](06-metaprogramming.md) with aspect-oriented programming (AOP), which is built on it.

Some requirements — logging, transactions, retries, authorization, tracing — cannot be localized in any single class or function. They cut across many, so the dominant decomposition repeats the same lines at every call site and tangles them with the core logic. AOP makes the scattered requirement itself a first-class unit: defined once, and attached where it applies by a declarative rule instead of an explicit call.

## AOP Concepts

Cross-Cutting Concern
: Requirement whose implementation would otherwise be scattered across many unrelated units and tangled with their primary logic

Join Point
: Well-defined moment in program execution where extra behavior may be attached: a method call or execution, a field access, an exception being thrown

Pointcut
: Predicate selecting a set of `Join Points` by signature, annotation, or type hierarchy, so the targets are described rather than enumerated

Advice
: Code to run at the selected moments, ordered relative to them as `before`, `after`, `after throwing`, or `around` — the last wrapping the target and free to skip or replace it

Aspect
: Unit bundling one or more `Pointcuts` with their `Advice` and any state they share, playing the role a class plays in OOP

Weaving
: Act of merging that extra behavior into the target program, done at compile time, at load time, or at run time through generated proxies

Introduction
: Adding members or a supertype to an existing class from outside its own definition, also called an inter-type declaration


*Implementations*: AspectJ (compile-time and load-time weaving), Spring AOP (runtime proxies, limited to method execution on managed beans), PostSharp, and the interceptor chains of most DI containers.

## AOP Trade-offs

The trade-off is the one [Metaprogramming](06-metaprogramming.md) always carries: an `Aspect` applies with no mark at the call site, so the code that is read is no longer the code that runs. Reserve AOP for concerns that are truly uniform across many units, and keep `Pointcuts` narrow enough that a reader can predict where they fire.

*See also*: [Paradigms](index.md) · [Metaprogramming](06-metaprogramming.md)
