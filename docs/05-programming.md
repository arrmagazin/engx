# Programming

![Programming](/images/05-programming.svg)

## Programming Paradigms

A **Programming Paradigm** is an opinionated vision of
what data computation is in terms of its core concepts,
dictating how data and code are treated, organized, accessed, and manipulated.

```mermaid
mindmap
  root((Paradigm))
    Imperative
      Structured
      Procedural
      OOP
    Declarative
      Functional
      Reactive
      Logic
      SQL
    Other
      Metaprogramming
      DDD
      AOP
      FBP
```

### Imperative Programming

| Paradigm | Description |
| ---------- | ------------- |
| **Imperative** | An early approach considering computation as evaluation of statements that directly change program state (data fields). Features: direct assignments, common data structures, global variables |
| **Structured** | A style of imperative programming with more logical program structure. Features: structograms, indentation, limited use of `goto` |
| **Procedural** | Derived from structured programming, based on modular programming or the procedure call |

### Object-Oriented Programming (OOP)

A prominent approach that considers computation as a side-effect from interacting stateful objects along their lifecycle.

#### OOP Design Principles

| Principle | Description |
| ----------- | ------------- |
| **Abstraction** | Representing a real object by its particular properties only (important in matters of problem) |
| **Encapsulation** | Mechanism to prevent access to state of object from outside (hide internal complexity) |
| **Inheritance** | Mechanism allowing ones to borrow/extend state and behavior from a basic one |
| **Polymorphism** | Mechanism to override method implementations in descendants while preserving signatures and semantics |

#### OOP Concepts

| Concept | Definition |
| --------- | ------------ |
| **Object** | A single instance in program code with its own state and behavior |
| **Class** | Specification of state and behavior used to create new objects |
| **Model** | Bundle of interdependent classes that a system consists of |
| **State** | Internal data structure belonging to and accessed by a given object |
| **Behavior** | Set of methods belonging to an object implementing specific logic relied on its state |
| **Method** | Certain way to handle specific input messages received from outside |
| **Implementation** | Code defining how to actually handle input signals; has access to input and state, may update state, produce results, fire events |
| **Invocation** | Act of performing instructions of method along input arguments, scope, and context |
| **Interaction** | Process of sending signals (events) between objects, responded by invocation of appropriate methods |
| **Event-Driven Flow** | Indirect way of interaction as sending unified event messages via centralized dispatcher (bus) |

```mermaid
sequenceDiagram
    participant Sender as Object A
    participant Bus
    participant Receiver as Object B
    Sender->>Bus: emit Event
    Bus->>Receiver: dispatch Event
    Receiver->>Receiver: invoke Method
    Receiver-->>Bus: fire Event
    Bus-->>Sender: dispatch Event
```

### Declarative Programming

A style building program structure that expresses the logic of computation without describing its control flow. Many languages minimize or eliminate side effects by describing WHAT the runtime engine must accomplish rather than HOW.

Examples: HTML, MXML, XAML, XSLT, and other UI markup languages.

### Functional Programming

A programming paradigm promoting computation as declarative composition and lazy-evaluation of pure (mathematical) functions.

> *"The main difference from imperative programming is the use of lazy evaluation model. Everything else - purity of functions, anonymous functions, higher-order functions, monads, parametric polymorphism - are just consequences."*

#### Key Concepts

| Concept | Definition |
| --------- | ------------ |
| **Lazy Evaluation** | Call-by-need evaluation delaying expression evaluation until value is needed; allows structures like infinite lists |
| **Operation** | Correspondence of input with unambiguous output: (x..., y1) & (x..., y2) => y1 ≡ y2 |
| **Parameter** | Reference to elementary piece of input data structure, by name or index |
| **Argument** | Input data value applied to corresponding parameter when operation is performed |
| **Function** | Operation providing mapping from elements of domain to elements of codomain |
| **Arity** | Dimension of domain space: unary, binary, n-ary, variadic |
| **Partial Function** | Function not defined for all possible values of its domain |
| **Deterministic Function** | Function always producing same results for same input |
| **Pure Function** | Deterministic function without side effects |
| **Side Effects** | Interactions (reads/writes) with external mutable state |
| **Higher-Order Function (HOF)** | A function taking a function as argument and/or returning a function |

#### Advanced FP Concepts

| Concept | Definition |
| --------- | ------------ |
| **Function Pipe** | Putting list of functions together where output of previous is input of next |
| **Fun-Arg Problem** | How to preserve references to environment variables after function is executed |
| **Closure** | Function retaining a reference to its free variables (from outer scope) |
| **Point-Free Style** | Writing functions where definition doesn't explicitly identify arguments used |
| **Partial Application** | Creating a new function by pre-filling some arguments to the original function |
| **Currying** | Generation of derived function doing same as original but with partially applied arguments |
| **Auto Currying** | Transforming a multi-argument function into one that returns a function taking the rest if given fewer arguments |
| **Continuation** | The part of code yet to be executed at any given point |
| **Memoization** | Storing and reusing results of function instead of actual re-execution |
| **Immutability** | Inability to destructively change/mutate input parameters, context, or state |
| **Idempotent** | Reapplying to result does not produce different result |
| **Recursion** | Function calling itself during execution |
| **Fixed-point Combinator** | Function Y returning fixed point for its argument function: Y(f) == f(Y(f)) |
| **Tail Recursion** | A function call where there is nothing to do after the function returns except return its value; essentially equivalent to looping |

### Reactive Programming

Programming as defining reactions on sequences of incoming events (data streams) that can be combined and observed asynchronously.

*Related concepts*: Propagation of changes, race conditions (glitches), throttling, debouncing, FRP

### Other Paradigms

- Metaprogramming
- Single source of truth
- Mathematical model
- Domain-driven design (DDD)
- SQL
- Component-based software engineering
- Flow-based programming (FBP)
- Constraint programming
- Logic programming
- Aspect-oriented Programming (AOP)
- Agent-oriented programming
- Modular programming
