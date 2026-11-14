---
type: Guide
title: Functional Reactive Programming
description: Defines functional reactive programming (FRP)—behaviors, event streams, and combinators—with its variants and trade-offs.
tags: [coding, programming-paradigms, reactive-programming, frp]
---

This guide continues [Reactive Programming](04-reactive-programming.md) with functional reactive programming (FRP): a combination of the functional and reactive paradigms. Values that change over time are first-class and are transformed by pure functions, instead of being updated by callbacks that mutate shared state.

## FRP Concepts

Behavior (Signal)
: Value continuously defined over time: `Behavior a = Time -> a`

Event Stream
: Discrete sequence of timestamped occurrences: `Event a = [(Time, a)]`

Declarative Time
: Time as an explicit input of the model, not an implicit side effect of execution order

Combinator
: Pure HOF building new behaviors or streams from existing ones (`map`, `filter`, `merge`, `scan`, `switch`)

Lifting
: Applying an ordinary function to time-varying values, producing a time-varying result

Sampling
: Reading a behavior's value at the moments given by an event stream

Accumulation (`scan`/`fold`)
: Deriving state from a stream by folding past occurrences — the only sanctioned form of state

Glitch-Freedom
: Guarantee that dependents observe a consistent snapshot; no intermediate values from partial propagation

## Variants

| Variant | Description |
| --------- | ------------- |
| **Classical FRP** | Continuous behaviors + discrete events with denotational semantics (Fran, Reactive) |
| **Arrowized FRP** | Signal functions (`Signal a -> Signal b`) composed as arrows, avoiding space/time leaks (Yampa) |
| **Discrete / "RX-style"** | Push-based streams without continuous time; pragmatic and widely deployed (RxJS, Reactor, Combine) |
| **Signal-based UI** | Fine-grained dependency graph of signals with automatic recomputation (SolidJS, Svelte runes, Angular signals) |

## FRP Trade-offs

| Aspect | Note |
| -------- | ------ |
| **Strengths** | Explicit data flow, composability, no manual subscription bookkeeping, testable as pure transformations |
| **Costs** | Steep learning curve, hard debugging (stack traces lost in the graph), memory/space leaks from retained histories |
| **Applicability** | UI state, animation, telemetry, event processing, robotics, and simulation |

*See also*: [Functional Programming](03-functional-programming.md) for the concepts used here, such as HOF · [Metaprogramming](06-metaprogramming.md)
