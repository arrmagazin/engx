---
type: Guide
title: Core concepts
description: Introduces foundational concepts of solutions, delivery, and engineering.
tags: [introduction, engineering]
---

These are the core concepts the rest of the book builds on, explores in depth, and uses without redefining.

## Abstract terms

```svg
<Panel caption="A System in its Environment">
  <Group col="0" row="0" colspan="5" rowspan="3" label="Environment" />
  <Group col="1" row="1" colspan="3" rowspan="2" label="System" tone="primary" />
  <Node key="constraint" col="2" row="0" label="Constraint" shape="hex" tone="warning" />
  <Node key="ingress" col="0" row="1" label="Ingress" shape="pill" />
  <Node key="process" col="2" row="1" label="Process" tone="primary" />
  <Node key="egress" col="4" row="1" label="Egress" shape="pill" />
  <Node key="state" col="1" row="2" label="State" shape="round" />
  <Node key="next" col="3" row="2" label="New State" shape="round" />
  <Node key="outcome" col="4" row="2" label="Gain/Outcome" note="a change, not a flow" />
  <Edge from="constraint" to="process" label="limits" dashed="true" tone="warning" />
  <Edge from="ingress" to="process" label="enters" />
  <Edge from="process" to="egress" label="leaves" />
  <Edge from="state" to="process" />
  <Edge from="process" to="next" label="changes" />
  <Edge from="egress" to="outcome" label="effect" />
</Panel>
```

System
: A set of interacting *parts* inside a boundary that separates it from its `Environment` — the whole shows behavior none of its parts has alone

    > such as software, a machine, a `Team`, an organization

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

Constraint
: A *limit*, imposed by the `Environment`, on the `States` a `System` may take or the `Processes` it may run — given, not chosen by the `System`

    > such as laws, physics, budget, deadline, `Platform`, available skills
    >
    > unlike a `Requirement`, it does not come from an `Objective` — it narrows the ways to reach one

Progress
: A *change* of a `System`'s `State` toward a target over time, shown by a `Metric`

Improvement
: `Progress` made by small, *gradual* changes to how a `System`'s `Processes` already work

Breakthrough
: `Progress` made by a large, *sudden* change in how a `System` is built or works — reaching a level no `Improvement` of the old way could reach

Sustainability
: The ability of a `System` to keep its `State` within acceptable limits *over time*, without using up what it depends on in itself or its `Environment`

## What a solution is for

```svg
<Panel caption="From a Need to Success">
  <Node key="stakeholder" col="0" row="0" label="Stakeholder" note="Customer · End-User" shape="round" />
  <Node key="need" col="1" row="0" label="Need" />
  <Node key="goal" col="2" row="0" label="Goal" />
  <Node key="objective" col="3" row="0" label="Objective" />
  <Node key="requirement" col="4" row="0" label="Requirement" />
  <Node key="solution" col="1" row="1" label="Solution" tone="primary" />
  <Node key="value" col="2" row="1" label="Value" />
  <Node key="satisfaction" col="3" row="1" label="Satisfaction" />
  <Node key="success" col="4" row="1" label="Success" shape="round" tone="success" />
  <Edge from="stakeholder" to="need" label="has" />
  <Edge from="need" to="goal" label="drives" />
  <Edge from="goal" to="objective" label="measured" />
  <Edge from="objective" to="requirement" label="broken&#10;down" />
  <Edge from="goal" to="value" label="expects" dashed="true" />
  <Edge from="solution" to="value" label="brings" />
  <Edge from="value" to="satisfaction" label="judged" />
  <Edge from="requirement" to="success" label="verified" />
  <Edge from="satisfaction" to="success" label="confirmed" />
</Panel>
```

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

    > such as: `Needs` covered, capability or benefits gained, `Constraints` matched, time or money saved, problem solved, risk removed

Need
: A *lack* of something a `Stakeholder` must have to run their business — it exists before, and apart from, any `Solution`

    > such as being paid on time, finding information fast, complying with a law
    >
    > it is the *problem*; a `Goal` is the `Value` expected from solving it

Goal
: A `Stakeholder`'s *expectation* of `Value`, set in a business `Environment` (what, when, where, how)

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

    > `Value` received, not scope delivered

## How a solution is made

```svg
<Panel caption="How a Team makes a Solution">
  <Group col="0" row="0" colspan="5" label="Engineering" tone="primary" />
  <Node key="team" col="0" row="1" label="Team" shape="round" />
  <Node key="resources" col="1" row="1" label="Resources" shape="db" />
  <Node key="design" col="0" row="0" label="Design" note="WHAT and WHY" />
  <Node key="build" col="1" row="0" label="Build" />
  <Node key="validate" col="2" row="0" label="Validate" />
  <Node key="delivery" col="3" row="0" label="Delivery" />
  <Node key="operation" col="4" row="0" label="Operation" />
  <Node key="solution" col="2" row="1" label="Solution" note="Product or Service" tone="primary" />
  <Node key="value" col="4" row="1" label="Value" note="Stakeholders receive" shape="round" tone="success" />
  <Edge from="team" to="resources" label="consumes" />
  <Edge from="team" to="design" label="runs" fromSide="top" toSide="bottom" />
  <Edge from="design" to="build" />
  <Edge from="build" to="validate" />
  <Edge from="validate" to="delivery" />
  <Edge from="delivery" to="operation" />
  <Edge from="validate" to="solution" label="proven" />
  <Edge from="solution" to="value" label="brings" />
</Panel>
```

Product
: `Solution` as a tangible or digital *artifact* made to be owned or used by others: software, device, facility, guidance

Service
: `Solution` as a *means* of delivering `Outcomes` `Stakeholders` want through ongoing interaction, without them owning the specific costs and risks

Team
: A small *group* of people with complementary skills, committed to shared `Goals` and mutually accountable for reaching them

Resources
: The *means* a `Team` consumes to deliver a `Solution`:

    time, money, people's effort, equipment, materials

Design
: The *activity* and *result* of deciding WHAT a `Solution` should be and WHY —

    its structure, behavior, and interactions — shaped by `End-User` `Needs` and `Constraints`

Delivery
: The *process* of bringing a `Solution` into use, so that `Stakeholders` actually receive its `Value`; it ends there, not at handover

Engineering
: The application of a systematic, disciplined, quantifiable *approach*, grounded in science and math, to the `Design`, building, validation, `Delivery` and operation of `Solutions`

Platform
: A *foundation* of facilities on which software is built and run

    > such as languages, runtimes, operating systems, cloud services, tools, ecosystems

Paradigm
: A shared, opinionated *model* of thinking — concepts, assumptions, and preferred `Methods` — that frames how a problem is seen and how knowledge is applied to solve it

    > rooted in science, math, and domain expertise: e.g. object-oriented, functional, event-driven

Methodology
: A coherent *system* of practices (roles, rituals, artifacts, workflows) a `Team` adopts to organize its work toward `Success`

    > such as Scrum, Kanban, Waterfall

## How work is run

```svg
<Panel caption="From why to how">
  <Node key="strategy" col="0" row="0" label="Strategy" note="why" shape="round" />
  <Node key="decision" col="1" row="0" label="Decision" shape="diamond" />
  <Node key="method" col="2" row="0" label="Method" note="rules" />
  <Node key="technology" col="3" row="0" label="Technology" note="means" />
  <Node key="process" col="4" row="0" label="Process" shape="round" tone="primary" />
  <Node key="management" col="0" row="1" label="Management" note="leads and allocates" tone="secondary" />
  <Node key="practice" col="2" row="1" label="Best Practice" />
  <Node key="framework" col="3" row="1" label="Framework" />
  <Edge from="strategy" to="decision" label="guides" />
  <Edge from="decision" to="method" label="picks" />
  <Edge from="method" to="technology" label="tooled" />
  <Edge from="technology" to="process" label="controls" />
  <Edge from="management" to="strategy" label="sets" fromSide="top" toSide="bottom" />
  <Edge from="management" to="decision" label="makes" />
  <Edge from="method" to="practice" label="proven" />
  <Edge from="method" to="framework" label="options" />
</Panel>
```

Decision
: An accountable *choice* of one option among weighed alternatives in a given `Environment`

    > with its tradeoffs agreed and its risks and costs accepted up front

Strategy
: A context-free, generalized *approach* to reaching a `Goal` — a set of values and principles for making reasonable `Decisions` ("why")

Method
: An organized set of predefined *rules* that control how a `Process` runs in a given `Environment`

Best Practice
: A `Method` accepted as superior to others because it reliably produces better `Outcomes` in its `Environment`

Framework
: A `Method` that offers predefined *options* a user chooses from, so the results become predictable

Technology
: The practical application of knowledge as reusable *means* — `Methods`, techniques, and tools — that make a `Process` controllable and its results *reproducible* and *verifiable*

Management
: The *process* of making `Decisions`, leading `Teams`, and allocating `Resources` to reach `Goals`

    - through people, `Process`, and priorities
    - within `Constraints` of time, budget, capacity, and quality
    - concerned with planning, organizing, governance, control, optimizing, securing, tracking, and growth
    - that turns `Goals` into predictably delivered `Outcomes`

Management bodies
: The *people* involved in the `Management` `Process`

    - leadership sets direction and motivates — `Strategy`
    - operations management allocates, sequences, and controls
    - a working engineering manager does both

Project
: A *temporary endeavor* in which a `Team` creates a unique `Solution` and pursues `Success`; it proceeds by choosing and applying `Paradigms`, `Methodologies`, `Technologies` and `Platforms`

```svg
<Panel caption="A Project ties it all together">
  <Node key="paradigm" col="0" row="0" label="Paradigm" />
  <Node key="methodology" col="0" row="1" label="Methodology" />
  <Node key="technology" col="0" row="2" label="Technology" />
  <Node key="platform" col="0" row="3" label="Platform" />
  <Node key="team" col="1" row="0" label="Team" shape="round" />
  <Node key="project" col="1" row="1" rowspan="2" label="Project" note="temporary endeavor" tone="primary" />
  <Node key="resources" col="1" row="3" label="Resources" shape="db" />
  <Node key="solution" col="2" row="1" rowspan="2" label="Solution" note="Product or Service" />
  <Node key="success" col="3" row="1" rowspan="2" label="Success" note="Value received" shape="round" tone="success" />
  <Edge from="paradigm" to="project" />
  <Edge from="methodology" to="project" />
  <Edge from="technology" to="project" />
  <Edge from="platform" to="project" />
  <Edge from="team" to="project" label="runs" />
  <Edge from="resources" to="project" label="consumed" fromSide="top" toSide="bottom" />
  <Edge from="project" to="solution" label="creates" />
  <Edge from="solution" to="success" label="pursues" />
</Panel>
```
