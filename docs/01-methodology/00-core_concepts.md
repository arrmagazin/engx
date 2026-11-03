---
type: Guide
title: Core concepts
description: Introduces foundational concepts of solutions, delivery, and engineering.
tags: [introduction, engineering]
---

These are the core concepts the rest of the book builds on, explores in depth, and uses without redefining.

## Abstract terms

System
: A set of interacting *parts* inside a boundary that separates it from its *environment* — the whole shows behavior none of its parts has alone

    > such as software, a machine, a team, an organization

Environment (Context)
: Everything outside a `System`'s boundary that affects it or is affected by it

    > such as users, other systems, hardware, networks, markets, laws, time, place, weather

Ingress/Egress
: Everything that *enters* or *leaves* a `System` across its boundary with its `Environment`

    > such as data, requests, energy, materials, money, people's effort

Gain/Outcome
: The *effect* a `System` gains from, or leaves on, its `Environment` — a change in structure or capacity, not just the `Ingress/Egress` across the boundary

    > such as a problem solved, a user served, money earned, waste produced

State
: The *condition* of a `System` at a point in time, given by the *measured* values of its attributes/capabilities

Metric
: A defined *method* of evaluation and *unit of measure*, for the degree to which a `System` has a given attribute/capability

    > units can be numeric, enumeration, or boolean

Process
: A sequence of *steps* that changes a `System`'s `State`, taking in `Ingress` and producing an `Outcome`

Progress
: A *change* of a `System`'s `State` toward a target over time, shown by a `Metric`

Improvement
: `Progress` made by small, *gradual* changes to how a `System`'s `Processes` already work

Breakthrough
: `Progress` made by a large, *sudden* change in how a `System` is built or works — reaching a level no `Improvement` of the old way could reach

Sustainability
: The ability of a `System` to keep its `State` within acceptable limits *over time*, without using up what it depends on in itself or its `Environment`

## What a solution is for

Solution
: A specific *way* of bringing `Value` to `Stakeholders`:

    > intentionally designed, made, proven and delivered by a `Team`; its results are observable and measurable

Stakeholder
: Any individual, group, or organization

    - that affects, or is affected by, a `Solution`'s `Outcome`
    - and therefore holds *expectations* about what it should deliver

    > such as `Customer`, `End-User`, operator, regulator, sponsor

Customer
: The `Stakeholder` who *pays* for the `Solution`, and so decides whether it is bought and kept

End-User
: The `Stakeholder` who directly *uses* the `Solution`; not necessarily the `Customer` who pays for it

Value
: The *worth* a `Stakeholder` gains in terms of their business

    > such as: needs covered, capability or benefits gained, constraints matched, time or money saved, problem solved, risk removed

Goal
: A `Stakeholder`'s *expectation* of `Value`, set in a business context (what, when, where, how)

    > it is *directional*, *predictive*, and too coarse to *verify* on its own

Objective
: A *measurable* reflection of a `Goal` — a target value of a `Metric`, to reach by a set time

Satisfaction
: A `Stakeholder`'s *judgement* of whether the delivered `Solution` meets their `Goals` "enough"

    > it is *opinionated*, *subjective* and *perceptive*, therefore elicited, not read from the `State`

Requirement
: A boundary on a `System`'s `State`, broken down from an `Objective`, that must hold to achieve it:

    > it gives "enough" a *falsifiable* test, which stands in for opinion but does not replace it

Success
: The `Outcome` in which the verified `State` meets every `Requirement` and key `Stakeholders` confirm their `Satisfaction` —

    > Value received, not scope delivered

## How a solution is made

Product
: `Solution` as a tangible or digital *artifact* made to be owned or used by others: software, device, facility, guidance

Service
: `Solution` as a *means* of delivering outcomes `Stakeholders` want through ongoing interaction, without them owning the specific costs and risks

Team
: A small *group* of people with complementary skills, committed to shared `Goals` and mutually accountable for reaching them

Resources
: The *means* a `Team` consumes to deliver a `Solution`:

    time, money, people's effort, equipment, materials

Design
: The *activity* and *result* of deciding WHAT a `Solution` should be and WHY —

    its structure, behavior, and interactions — shaped by `End-User` needs/constraints

Delivery
: The *process* of bringing a `Solution` into use, so that `Stakeholders` actually receive its `Value`; it ends there, not at handover

Engineering
: The application of a systematic, disciplined, quantifiable *approach*, grounded in science and math, to the `Design`, building, validation, `Delivery` and operation of `Solutions`

Platform
: A *foundation* of facilities on which software is built and run

    > such as languages, runtimes, operating systems, cloud services, tools, ecosystems

Paradigm
: A shared, opinionated *model* of thinking — concepts, assumptions, and preferred methods — that frames how a problem is seen and how knowledge is applied to solve it

    > rooted in science, math, and domain expertise: e.g. object-oriented, functional, event-driven

Methodology
: A coherent *system* of practices (roles, rituals, artifacts, workflows) a `Team` adopts to organize its work toward `Success`

    > such as Scrum, Kanban, Waterfall

## How work is run

Decision
: An accountable *choice* of one option among weighed alternatives in a given context

    > with its tradeoffs agreed and its risks and costs accepted up front

Strategy
: A context-free, generalized *approach* to reaching a `Goal` — a set of values and principles for making reasonable `Decisions` ("why")

Method
: An organized set of predefined *rules* that control how a process runs in a given context

Best Practice
: A `Method` accepted as superior to others because it reliably produces better outcomes in its context

Framework
: A `Method` that offers predefined *options* a user chooses from, so the results become predictable

Technology
: The practical application of knowledge as reusable *means* — methods, techniques, and tools — that make a process controllable and its results *reproducible* and *verifiable*

Management
: The *process* of making `Decisions`, leading `Teams`, and allocating `Resources` to reach `Goals`

    - through people, process, and priorities
    - within limits of time, budget, capacity, and quality
    - concerned with planning, organizing, governance, control, optimizing, securing, tracking, and growth
    - that turns `Goals` into predictably delivered outcomes

Management bodies
: The *people* involved in the `Management` process

    - leadership sets direction and motivates — `Strategy`
    - operations management allocates, sequences, and controls
    - a working engineering manager does both

Project
: A *temporary endeavor* in which a `Team` creates a unique `Solution` and pursues `Success`; it proceeds by choosing and applying `Paradigms`, `Methodologies`, `Technologies` and `Platforms`
