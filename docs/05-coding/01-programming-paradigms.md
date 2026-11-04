---
type: Guide
title: Programming Paradigms
description: Surveys programming paradigms—imperative, object-oriented, declarative, functional, and others—and how each treats data and code.
tags: [coding, programming-paradigms]
---

A **programming paradigm** is an opinionated view of what computation is. It dictates how data and code are organized, accessed, and changed. This guide surveys the imperative, object-oriented, and declarative families, for engineers choosing a style for a component or reading code written in an unfamiliar one. It is also the canonical home for the OOP pillars. The functional family has its own guide, [Functional Programming](02-functional-programming.md), as does the reactive family, [Reactive Programming and FRP](03-reactive-programming.md), and so do metaprogramming and AOP, in [Metaprogramming and AOP](04-metaprogramming.md).

```svg
<Panel>
  <Node key="root" col="2" row="2" rowspan="2" label="Paradigm" shape="circle" tone="primary" />
  <Node key="imperative" col="1" row="1" label="Imperative" shape="round" />
  <Node key="structured" col="0" row="0" label="Structured" shape="pill" />
  <Node key="procedural" col="0" row="1" label="Procedural" shape="pill" />
  <Node key="oop" col="0" row="2" label="OOP" shape="pill" />
  <Node key="other" col="1" row="5" label="Other" shape="round" />
  <Node key="meta" col="0" row="3" label="Metaprogramming" shape="pill" />
  <Node key="aop" col="0" row="4" label="AOP" shape="pill" />
  <Node key="fbp" col="0" row="5" label="FBP" shape="pill" />
  <Node key="constraint" col="0" row="6" label="Constraint" shape="pill" />
  <Node key="components" col="0" row="7" label="Components" shape="pill" />
  <Node key="declarative" col="3" row="2" rowspan="2" label="Declarative" shape="round" />
  <Node key="functional" col="4" row="1" label="Functional" shape="pill" />
  <Node key="logic" col="4" row="2" label="Logic" shape="pill" />
  <Node key="sql" col="4" row="3" label="SQL" shape="pill" />
  <Node key="reactive" col="4" row="4" label="Reactive" shape="pill" />
  <Node key="frp" col="4" row="5" label="FRP" shape="pill" />
  <Edge from="root" to="imperative" arrow="none" />
  <Edge from="root" to="declarative" arrow="none" />
  <Edge from="root" to="other" arrow="none" />
  <Edge from="imperative" to="structured" arrow="none" />
  <Edge from="imperative" to="procedural" arrow="none" />
  <Edge from="imperative" to="oop" arrow="none" />
  <Edge from="declarative" to="functional" arrow="none" />
  <Edge from="declarative" to="reactive" arrow="none" />
  <Edge from="declarative" to="logic" arrow="none" />
  <Edge from="declarative" to="sql" arrow="none" />
  <Edge from="reactive" to="frp" arrow="none" />
  <Edge from="other" to="meta" arrow="none" />
  <Edge from="other" to="aop" arrow="none" />
  <Edge from="other" to="fbp" arrow="none" />
  <Edge from="other" to="constraint" arrow="none" />
  <Edge from="other" to="components" arrow="none" />
</Panel>
```

## Imperative Programming

| Paradigm | Description |
| ---------- | ------------- |
| **Imperative** | An early approach: a program is a sequence of commands, each updating the program's state in place. Values change by assignment, and many parts of the code may read and write the same data |
| **Structured** | Imperative code built only from sequence, choice, and loops, so control flow is easy to follow. Code is grouped into nested blocks; jumps such as `goto` are rare or absent |
| **Procedural** | Structured code organized into named procedures that call one another and pass data through parameters |

## Object-Oriented Programming (OOP)

A prominent approach that treats computation as a side effect of stateful objects interacting over their lifecycle.

### OOP Pillars

| Principle | Description |
| ----------- | ------------- |
| **Abstraction** | Representing a real object by only the properties that matter to the problem |
| **Encapsulation** | Mechanism that blocks outside access to an object's state, hiding internal complexity |
| **Inheritance** | Mechanism that lets one class borrow or extend state and behavior from a base class |
| **Polymorphism** | Mechanism that lets descendants override method implementations while keeping signatures and semantics |

For language-agnostic design heuristics such as SOLID, GRASP, and DRY, see [Design Principles](05-design-principles.md).

### OOP Concepts

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

A `State` and a `Method` here belong to one object. [Core concepts](../01-methodology/00-core_concepts.md) defines a `State` as the condition of a whole `Solution`, and a `Method` as a set of rules for running a process. In this section, the object sense applies.

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

## Declarative Programming

A style in which a program states the result it wants and leaves the steps to the runtime, so control flow does not appear in the code. Many declarative languages limit or remove side effects, so a program reads as a description of WHAT, not HOW.

Examples: query languages such as SQL; logic languages such as Prolog and Datalog; regular expressions; markup for user interfaces such as HTML, XAML, and MXML; and XSLT for transforming XML.

## Functional Programming

A paradigm that treats computation as the declarative composition of pure (mathematical) functions. Its terms are defined in [Functional Programming](02-functional-programming.md).

## Other Paradigms

The families above, together with [Reactive Programming and FRP](03-reactive-programming.md) and [Metaprogramming and AOP](04-metaprogramming.md), cover most production code. Engineers still meet the paradigms below, usually as a specialized language or framework inside an otherwise conventional system. Each is described by the unit it treats as primitive, because that choice is what separates it from the paradigms covered above.

Logic Programming
: Declarative style where a program is a set of facts and rules, and running it asks the engine to search for a proof of a goal instead of prescribing the steps (Prolog, Datalog, answer-set solvers)

Constraint Programming
: Close relative of `Logic Programming`: the program states relations a solution must satisfy and a solver explores the feasible space, so the search strategy belongs to the engine, not the author (MiniZinc, Choco, OR-Tools)

Flow-Based Programming (FBP)
: Assembly of black-box processes that exchange fixed-format packets over bounded, named connections owned by the network rather than by any process, which makes the topology data instead of code (NoFlo, Node-RED, LabVIEW)

Agent-Oriented Programming
: Autonomous entities holding their own beliefs, goals, and plans as first-class program elements and coordinating through messages instead of direct invocation, so control is truly decentralized (JADE, Jason/AgentSpeak)

Component-Based Software Engineering
: Building systems from independently deployable units that expose only contractual interfaces, which moves substitution and reuse from the `Class` boundary out to the packaging boundary (OSGi, COM, .NET assemblies)

Modular Programming
: Splitting a program into separately compiled units with explicit exported and imported names — the discipline Procedural programming grew out of, and the one that today's packages and namespaces still implement (Modula-2, ML functors, JPMS, ES imports)
