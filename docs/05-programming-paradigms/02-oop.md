---
type: Guide
title: Object-Oriented Programming
description: Defines the four OOP pillars and core terms—object, class, state, method, and interaction—for engineers reading or writing OOP code.
tags: [coding, programming-paradigms, object-oriented-programming]
---

This guide continues [Paradigms](index.md) with object-oriented programming (OOP): a prominent approach that treats computation as a side effect of stateful objects interacting over their lifecycle. It is the canonical home for the OOP pillars.

## OOP Pillars

| Principle | Description |
| ----------- | ------------- |
| **Abstraction** | Representing a real object by only the properties that matter to the problem |
| **Encapsulation** | Mechanism that blocks outside access to an object's state, hiding internal complexity |
| **Inheritance** | Mechanism that lets one class borrow or extend state and behavior from a base class |
| **Polymorphism** | Mechanism that lets descendants override method implementations while keeping signatures and semantics |

For language-agnostic design heuristics such as SOLID, GRASP, and DRY, see [Design Principles](../06-coding/01-design-principles.md).

## OOP Concepts

Object
: A single instance in program code with its own `State` and `Behavior`

Class
: Specification of `State` and `Behavior` used to create new `Objects`

Model
: Bundle of interdependent Classes that a system consists of

State
: Internal data structure private to one instance

Behavior
: Set of Methods implementing logic over the `State` they share

Method
: Named way of handling one specific input message

Implementation
: Code defining how an input message is actually handled; reads input and `State`, and may update `State`, produce results, or send further messages

Invocation
: Act of performing the instructions of a Method with given arguments, scope, and context

Interaction
: Process of sending messages between `Objects`, each answered by `Invocation` of the matching Method

Event-Driven Flow
: Indirect Interaction in which uniform events travel through a centralized dispatcher (bus)

A `State` and a `Method` here belong to one object. [Core concepts](../01-methodology/00-core_concepts.md) defines a `State` as the condition of a whole `Solution`, and a `Method` as a set of rules for running a process. In this guide, the object sense applies.

```svg
<Panel>
  <Node key="a" col="0" row="0" label="Object A" />
  <Node key="bus" col="1" row="0" label="Bus" />
  <Node key="b" col="2" row="0" label="Object B" />
  <Node key="m1" col="0" row="1" shape="point" />
  <Node key="m2" col="1" row="2" shape="point" />
  <Node key="m3" col="2" row="3" shape="point" />
  <Node key="m4" col="2" row="4" shape="point" />
  <Node key="m5" col="1" row="5" shape="point" />
  <Node key="m6" col="0" row="6" shape="point" />
  <Edge from="a" to="m6" arrow="none" />
  <Edge from="bus" to="m5" arrow="none" />
  <Edge from="b" to="m4" arrow="none" />
  <Edge from="m1" to="m2" label="emit Event" />
  <Edge from="m2" to="m3" label="dispatch Event" />
  <Edge from="m3" to="m4" label="invoke Method" fromSide="right" toSide="right" />
  <Edge from="m4" to="m5" label="fire Event" dashed="true" />
  <Edge from="m5" to="m6" label="dispatch Event" dashed="true" />
</Panel>
```

*See also*: [Paradigms](index.md) · [Design Patterns](../06-coding/02-design-patterns.md)
