---
type: Guide
title: Design Principles
description: Core software design principles (DRY, SSOT, SoC, and more) plus the SOLID and GRASP principles of object-oriented design.
tags: [coding, design-principles, solid, grasp]
---

# Design Principles

A **design principle** is a general, technology-agnostic constraint on *structural* decisions about code: a force to optimize against one of the design criteria below. This page is the canonical home for SOLID, GRASP, DRY, and Single Source of Truth.

| Property | Meaning |
| ---------- | --------- |
| **Prescriptive, not procedural** | Comes without the concrete constructs that achieve it; states what must be true of a design, not the steps to get there |
| **Justified by consequence** | Its authority comes from a predicted cost, usually the cost of future change; a principle with no consequence attached is a style rule |
| **Non-absolute** | Principles conflict by design (DRY against premature normalization, SSOT against its own coupling cost) — applying them is trade-off resolution, not compliance |
| **Falsifiable in review** | Concrete code can be pointed at and argued a violation; if no code could ever violate it, it is a value, not a principle |
| **Scope-bearing** | Each governs a level — expression, module, service, or system — and applying a module-level principle at system scale is a common misuse |

A principle's practical test must tell you which of two designs is better *before* either is built.

## Design Criteria

Properties of code that a person can *understand, assure, evolve, and maintain* without difficulty.

| Criterion | Description |
| ----------- | ------------- |
| **Composability** | Ability of code to be combined into larger code without modifying the parts being combined; it depends on each part exposing a contract that states what it owns and what it leaves to callers |
| **Maintainability** | How easily code can be understood, modified, or extended; the remaining criteria are the specific properties that produce it |
| **Simplicity** | Code should be as simple as possible; avoid unnecessary complexity — simple code is easier to extend |
| **Readability** | Code should be easily understandable using meaningful names and logical organization, so that others can read and edit it; a peer review confirms this |
| **Consistency** | Follow one coding style, set of design principles, patterns, and best practices across the codebase; shared rules agreed early keep many developers aligned, and standard-conforming code is easier to find, reuse, and update |
| **Comments/Documentation** | Explain WHY certain decisions were made, not HOW code works |
| **Error Handling** | Handle errors gracefully; anticipate potential failures (**Fail-fast**) |
| **Observability** | Runtime behavior can be understood from what the code already emits — structured logs, metrics, traces — so a failure can be diagnosed without shipping new code to reproduce it |
| **Testability** | Clean code is testable: small, independent behaviors that automated tests can verify, otherwise thorough testing is impractical |

## Prominent Design Principles

| Principle | Description |
| ----------- | ------------- |
| **Single Level of Abstraction (SLAP)** | Every statement in a routine sits at the same level of abstraction; a routine that mixes high-level policy with low-level detail is the violation, and extracting the detail into named calls is the fix |
| **Rule of Least Power** | Use the least powerful language suitable for the purpose, because the less a notation can express the more can be inferred from it (W3C TAG finding, Berners-Lee) |
| **KISS** | "Keep It Simple, Stupid" — prefer the simplest design that meets the need (attributed to Kelly Johnson) |
| **Separation of Concerns (SoC)** | Cut the system along axes of change, so each concern lives in one place and can be changed without touching the others |
| **DRY (Don't Repeat Yourself)** | Every piece of knowledge must have a single, unambiguous, authoritative representation within a system (Hunt & Thomas, *The Pragmatic Programmer*) |
| **Delegation** | Do one thing yourself and hand the rest to the object that owns it |
| **Inversion of Control** | Custom code receives the flow of control from a generic framework — "Don't call us, we'll call you", also known as the Hollywood Principle |
| **Uniform Access** | All services offered by a module should be available through a uniform notation, which does not betray whether they are implemented through storage or through computation |
| **Least Astonishment** | A component should behave the way most of its users expect it to |
| **Law of Demeter** | A method should only call methods of its immediate collaborators |
| **Worse is Better** | A simple implementation is more valuable than complete functionality, because the simple one spreads first (Richard P. Gabriel) |
| **YAGNI** | You Aren't Gonna Need It — don't implement until necessary |

## SOLID Principles of Object-Oriented Design

Five principles formulated by Robert C. Martin; the acronym is Michael Feathers'. Together they aim to reduce module change to addition and removal, which supports deferring technical decisions and dividing labor.

| Principle | Description |
| ----------- | ------------- |
| **Single Responsibility (S)** | An entity should be concerned with one function and have one reason to change, answering to a single business role |
| **Open/Closed (O)** | An entity should be open for extension but closed for modification |
| **Liskov Substitution (L)** | An object must be replaceable by an instance of any of its subtypes without altering the correctness of the program: a subtype may not strengthen the preconditions of an inherited operation, may not weaken its postconditions, and must preserve the invariants its base type guarantees. A subtype that throws where the base type returns, or that narrows an accepted input range, breaks substitutability even where the compiler accepts it |
| **Interface Segregation (I)** | Make fine-grained interfaces that are client-specific, so no client depends on methods it does not use |
| **Dependency Inversion (D)** | Depend upon abstractions, not concretions; Dependency Injection is its common implementation |

## GRASP — General Responsibility Assignment Software Patterns

Nine patterns for assigning responsibilities to types, formulated by Craig Larman. Where SOLID governs the *shape* of a module, GRASP answers the prior question: **who should own this responsibility?** Two of the nine name the goals; the other seven are the moves that achieve them.

| Goal | Description |
| -------- | ------------- |
| **Low Coupling** | Assign duties so dependencies between elements stay few and stable |
| **High Cohesion** | Keep duties that change together in one place |

Each of the remaining patterns is a rationale for placing a duty on one type rather than another.

| Pattern | Description |
| -------- | ------------- |
| **Information Expert** | Assign a duty to the type that already holds the information needed to fulfill it |
| **Creator** | Let a type create instances it aggregates, contains, records, or holds the initializing data for |
| **Controller** | Route a system event to one coordinator — a use-case handler or root object — not to the UI or the domain |
| **Polymorphism** | Assign type-varying behavior to the types themselves instead of branching on a type tag |
| **Pure Fabrication** | Invent a non-domain type (repository, mapper, service) when the domain offers no cohesive home |
| **Indirection** | Insert an intermediary to keep two elements from knowing each other directly |
| **Protected Variations** | Wrap predicted points of variation behind a stable interface so change stays contained |

## Single Source of Truth (SSOT)

**Single Source of Truth (SSOT)** is the design principle that every piece of knowledge has exactly
one authoritative representation, and everything else is *derived* from it rather than restated
alongside it.

Duplication is not forbidden — uncontrolled duplication is. A copy that a machine regenerates
is a cache; a copy that a human maintains is a future contradiction.

Writes converge on one place; reads fan out. The moment a derived artifact becomes
independently editable, the arrow reverses and the guarantee is gone.

### Key Concepts

Canonical Source
: The one representation designated as authoritative; conflicts are resolved in its favor by definition, not by negotiation

Derived Artifact
: Any representation reproducible from the source by a deterministic transformation

Projection
: A read-optimized view built from the source — denormalized on purpose, never edited in place

Idempotent Derivation
: Regeneration that yields an unchanged artifact from an unchanged source, making drift detectable by diff

Drift
: Divergence between source and copy; the failure mode SSOT exists to prevent

Reconciliation
: Continuously re-deriving actual state toward declared state (the control loop behind IaC and Kubernetes)

Controlled Duplication
: Copies that are generated, checked, or expired — caches, indexes, materialized views, replicas

DRY and SSOT are not the same rule. DRY is about *knowledge*, not text: two identical lines
expressing unrelated decisions are not a violation, and two divergent expressions of one decision
are. SSOT is the stronger claim — where copies of one piece of knowledge must exist, it names which
of them is authoritative and requires the rest to be derived from it.

### Where It Applies

| Domain | Canonical Source | Derived From It |
| -------- | ------------------ | ----------------- |
| **Code** | The single definition of a rule, constant, or type | Call sites, overloads, re-exports |
| **Types & Contracts** | Schema or IDL (Protobuf, OpenAPI, GraphQL SDL) | Server stubs, clients, validators, docs, mocks |
| **Relational Data** | Normalized tables with keys and constraints | Indexes, materialized views, reports |
| **Distributed State** | Append-only event log | CQRS read models, projections, caches, search indexes |
| **Configuration** | One config source per environment | Injected env vars, rendered templates |
| **Infrastructure** | Declarative IaC definitions | Provisioned cloud resources, reconciled continuously |
| **Front-end State** | A single normalized store or server cache | Component props, selectors, memoized views |
| **Documentation** | The code, tests, or schema themselves | Generated reference docs, examples extracted from tests |

### Violations & Smells

| Smell | Why It Hurts |
| ------- | -------------- |
| **Hand-maintained mirror** | A hand-written client for a documented API; both are edited, neither is authoritative |
| **Copy-pasted constant** | The same magic value in code, config, and a migration — updated in two of three |
| **Editable generated file** | Generated output committed and then patched by hand; the next regeneration silently reverts the fix |
| **Bidirectional sync** | Two systems each able to write the same field; conflict resolution becomes an unbounded problem |
| **Documentation restating behavior** | Prose describing what the code does, with nothing forcing the two to agree |
| **Premature normalization** | Collapsing two things that merely *look* alike into one definition, coupling decisions that must evolve separately |

### Trade-offs

| Aspect | Note |
| -------- | ------ |
| **Strengths** | One place to change, contradictions become impossible rather than merely unlikely, drift is detectable mechanically, correctness questions have a defined answer |
| **Costs** | A generation or reconciliation step in the build, coupling of all consumers to the source's release cadence, latency and staleness where derivation is asynchronous, and a bad abstraction that spreads everywhere once it is canonical |
| **Applicability** | Contracts crossing team or service boundaries, anything expressed in more than two places, and any value whose inconsistency is a correctness bug rather than a cosmetic one |

*Guidance*: prefer *generating* the copies over *synchronizing* them — the derivation itself is what
makes the source authoritative. Where derivation is impossible, make the duplication loud: a test
that fails when the two disagree is a weaker but honest substitute.

*See also*: [Metaprogramming](01-programming-paradigms.md#metaprogramming) — schema-driven code generation is the usual mechanism for enforcing SSOT across languages and services.
