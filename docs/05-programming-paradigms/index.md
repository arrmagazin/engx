---
type: Guide
title: Paradigms
description: Introduces programming paradigms: an overview of the main families, then one guide per family that goes deeper.
tags: [coding, programming-paradigms]
---

A **programming paradigm** is a *mental model* of what computation is. It dictates how data and code are organized, accessed, and changed. Start with the [overview](01-overview.md): it surveys the imperative, object-oriented, and declarative families. The other guides each take one family the overview only names, and go deeper.

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

---

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Paradigms Overview](01-overview.md)** | Imperative, object-oriented, and declarative programming, plus logic, constraint, and other specialized paradigms |
| **[Object-Oriented Programming](02-oop.md)** | The four OOP pillars and core terms: object, class, state, method, and interaction |
| **[Functional Programming](03-functional-programming.md)** | Functions and purity, function composition, and evaluation strategy |
| **[Reactive Programming](04-reactive-programming.md)** | Reactive programming over data streams, operators and rate control, and reactive systems |
| **[Functional Reactive Programming](05-frp.md)** | FRP concepts — behaviors, event streams, combinators — its variants, and trade-offs |
| **[Metaprogramming](06-metaprogramming.md)** | Code that reads, generates, or transforms code — its stages, techniques, and trade-offs |
| **[Aspect-Oriented Programming](07-aop.md)** | Cross-cutting concerns, join points, pointcuts, advice, and weaving — and when AOP pays off |

Outside this folder: [Coding](../06-coding/index.md) · [Design Principles](../06-coding/01-design-principles.md) · [Design Patterns](../06-coding/02-design-patterns.md)
