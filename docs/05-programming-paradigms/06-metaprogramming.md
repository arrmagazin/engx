---
type: Guide
title: Metaprogramming
description: Covers metaprogramming—code that reads, generates, or transforms code—with its stages, techniques, and trade-offs.
tags: [coding, programming-paradigms, metaprogramming]
---

This guide continues [Paradigms](index.md) with programs that treat code as data.

## Metaprogramming

Writing programs that treat other programs, or themselves, as data: reading, generating, or transforming code instead of only executing it. The *metaprogram* operates on the *object program*; **when** the transformation happens fixes the boundary between them.

```svg
<Panel>
  <Node key="src" col="0" row="0" label="Source Text" />
  <Node key="gen" col="0" row="1" label="Generator / Schema" />
  <Node key="ast" col="1" row="0" label="AST" />
  <Node key="ast2" col="1" row="1" label="AST'" />
  <Node key="bin" col="2" row="1" label="Bytecode / Binary" />
  <Node key="rt" col="2" row="2" label="Runtime Objects" />
  <Node key="rt-loop" col="2" row="3" shape="point" />
  <Edge from="gen" to="src" label="emit source" dashed="true" />
  <Edge from="src" to="ast" label="parse" />
  <Edge from="ast" to="ast2" label="macro expansion" />
  <Edge from="ast2" to="bin" label="compile" />
  <Edge from="bin" to="rt" label="load, weave" />
  <Edge from="rt" to="rt-loop" label="reflect, proxy, patch" arrow="none" />
  <Edge from="rt-loop" to="rt" fromSide="right" toSide="right" />
</Panel>
```

### Metaprogramming Concepts

Metalevel vs. Base Level
: The metaprogram manipulates representations of code; the object program is the code being manipulated

Introspection
: Read-only examination of program structure — types, members, signatures, annotations

Reflection
: Introspection plus *intercession*: invoking, defining, or altering structure dynamically

Homoiconicity
: Code is represented in the language's own data structures, so manipulating code is ordinary data manipulation (Lisp s-expressions)

AST
: Tree representation of parsed source; the usual currency of compile-time transformation

Quoting / Quasiquotation
: Turning code into data (`quote`), with holes for splicing computed fragments back in (`unquote`)

Macro
: Function from code to code, expanded before evaluation rather than called at runtime

Hygiene
: Guarantee that names introduced by a macro cannot capture or collide with names at the call site

Staging
: Explicit separation of computation into phases — what runs now to produce what runs later

Code Generation
: Emitting source, bytecode, or binaries from a model, schema, or IDL

Eval
: Evaluating data (a string, an `AST`) as code inside the running program

DSL
: Purpose-built notation, *internal* (hosted in the language) or *external* (own parser)

### Stages

The same goal can be reached at different points in the lifecycle, with very different trade-offs.

| Stage | Mechanisms | Character |
| ------- | ------------ | ----------- |
| **Compile-time** | Macros, templates, `comptime`/`constexpr`, annotation processors, source generators | No runtime cost, type-checkable, visible to tooling; errors surface as expansion failures |
| **Load / Link-time** | Bytecode weaving, custom class loaders, generated proxies, instrumentation agents | Applies to code you do not own; invisible in source, so behavior diverges from what is read |
| **Run-time** | Reflection, dynamic proxies, `eval`, metaclasses, method interception | Maximum flexibility and late binding; costs performance and defeats static analysis |

### Techniques

| Technique | Mechanism | Examples |
| ----------- | ----------- | ---------- |
| **Textual Macros** | Token substitution before parsing; unhygienic, unaware of syntax | C/C++ preprocessor |
| **Syntactic Macros** | AST-to-AST functions run by the compiler; hygiene depends on the macro system | Scheme `syntax-rules`/`syntax-case` (hygienic), Common Lisp `defmacro` (unhygienic, hence `gensym`), Rust `macro_rules!` and proc macros, Scala 3 `inline`/quotes, Elixir |
| **Compile-time Evaluation** | Ordinary code executed by the compiler to specialize or produce declarations | C++ templates and `constexpr`, Zig `comptime`, D CTFE |
| **Annotation Processing** | Declarative metadata read by a generator that emits companion code | Java APT/Lombok, Kotlin KSP, C# Source Generators, `go:generate` |
| **Reflection APIs** | Runtime access to the type system and member tables | `java.lang.reflect`, `System.Reflection`, Python `inspect`/`getattr`, JS `Reflect` |
| **Proxies & Interception** | Synthesized objects forwarding calls through a handler | JDK dynamic proxies, ByteBuddy/CGLIB, JS `Proxy` traps, Python `__getattr__` |
| **Metaclasses & Open Classes** | Controlling or rewriting class construction and dispatch | Python `type`/`__init_subclass__`, Ruby `class << self` and monkey patching, and JS decorators |
| **Bytecode Manipulation** | Rewriting compiled artifacts directly | ASM, Javassist, ByteBuddy, Mono.Cecil |
| **Schema-driven Generation** | Deriving clients, models, and serializers from an external contract | Protobuf/gRPC, OpenAPI, GraphQL codegen, ORM entities |

### Metaprogramming Trade-offs

| Aspect | Note |
| -------- | ------ |
| **Strengths** | Removes boilerplate and duplication, enforces cross-cutting concerns in one place, adapts to schemas and types unknown when the code was written, enables `DSLs` closer to the domain |
| **Costs** | Code that is read is no longer the code that runs — debugging, stack traces, IDE navigation, and refactoring all degrade; reflection and `eval` block dead-code elimination, AOT compilation, and security review; expansion errors are reported in generated code |
| **Applicability** | Serialization, ORM and DI wiring, mocking and test doubles, AOP concerns (logging, transactions, retries), builders and derived boilerplate, and `API` clients from contracts |

*Guidance*: prefer the earliest stage that solves the problem — a generic or template before a macro, a macro before an annotation processor, an annotation processor before runtime reflection. Use the dynamic option only when the shape of the code is truly unknown until execution.

*See also*: [Aspect-Oriented Programming](07-aop.md) — its join points, advice, and weaving are built almost entirely on the load-time and run-time stages above.

*See also*: [Paradigms](index.md) · [Reactive Programming](04-reactive-programming.md)
