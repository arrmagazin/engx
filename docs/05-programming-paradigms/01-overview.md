---
type: Guide
title: Paradigms Overview
description: Surveys the main programming paradigms—imperative, object-oriented, declarative, functional—and the specialized ones engineers still meet.
tags: [coding, programming-paradigms]
---

This guide gives a survey of the main families, for engineers choosing a style for a component or reading code written in an unfamiliar one.

## Imperative Programming

| Paradigm | Description |
| ---------- | ------------- |
| **Imperative** | An early approach: a program is a sequence of commands, each updating the program's state in place. Values change by assignment, and many parts of the code may read and write the same data |
| **Structured** | Imperative code built only from sequence, choice, and loops, so control flow is easy to follow. Code is grouped into nested blocks; jumps such as `goto` are rare or absent |
| **Procedural** | Structured code organized into named procedures that call one another and pass data through parameters |

## Object-Oriented Programming (OOP)

A prominent approach that treats computation as a side effect of stateful objects interacting over their lifecycle. Its pillars and terms are defined in [Object-Oriented Programming](02-oop.md).

## Declarative Programming

A style in which a program states the result it wants and leaves the steps to the runtime, so control flow does not appear in the code. Many declarative languages limit or remove side effects, so a program reads as a description of WHAT, not HOW.

Examples: query languages such as SQL; logic languages such as Prolog and Datalog; regular expressions; markup for user interfaces such as HTML, XAML, and MXML; and XSLT for transforming XML.

## Functional Programming

A paradigm that treats computation as the declarative composition of pure (mathematical) functions. Its terms are defined in [Functional Programming](03-functional-programming.md).

## Other Paradigms

The families above, together with [Reactive Programming](04-reactive-programming.md), [Functional Reactive Programming](05-frp.md), [Metaprogramming](06-metaprogramming.md), and [Aspect-Oriented Programming](07-aop.md), cover most production code. Engineers still meet the paradigms below, usually as a specialized language or framework inside an otherwise conventional system. Each is described by the unit it treats as primitive, because that choice is what separates it from the paradigms covered above.

Logic Programming
: Declarative style where a program is a set of facts and rules, and running it asks the engine to search for a proof of a goal instead of prescribing the steps (Prolog, Datalog, answer-set solvers)

Constraint Programming
: Close relative of `Logic Programming`: the program states relations a solution must satisfy and a solver explores the feasible space, so the search strategy belongs to the engine, not the author (MiniZinc, Choco, OR-Tools)

Flow-Based Programming (FBP)
: Assembly of black-box processes that exchange fixed-format packets over bounded, named connections owned by the network rather than by any process, which makes the topology data instead of code (NoFlo, Node-RED, LabVIEW)

Agent-Oriented Programming
: Autonomous entities holding their own beliefs, goals, and plans as first-class program elements and coordinating through messages instead of direct invocation, so control is truly decentralized (JADE, Jason/AgentSpeak)

Component-Based Software Engineering
: Building systems from independently deployable units that expose only contractual interfaces, which moves substitution and reuse from the class boundary out to the packaging boundary (OSGi, COM, .NET assemblies)

Modular Programming
: Splitting a program into separately compiled units with explicit exported and imported names — the discipline Procedural programming grew out of, and the one that today's packages and namespaces still implement (Modula-2, ML functors, JPMS, ES imports)
