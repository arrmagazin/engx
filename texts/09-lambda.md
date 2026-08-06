# Lambda Calculus

Lambda Calculus (λ-Calculus) is a *formal system* expressing computation through:

1. Constructions of λ-expressions
2. Reductions on them

The set of lambda expressions (Λ) can be defined inductively over a set of variables (alphabet):

---

**`Expression`** := The three forms of λ-expressions.

> `<variable> | <function> | <application>`

---

**`Function`** := Where x is bound to expression M.

> `λ<x-variable>.<M-expression>`

---

**`Application`** := Where N substitutes into M instead of bound variable.

> `<M-expression> <N-expression>`

---

**`α-conversion`** := Renaming to avoid collisions.

> `λx.M[x] → λy.M[y/x]`

---

**`β-reduction`** := Replacing the bound x with the argument expression in the body of the abstraction.

> `(λx.M)N → M[N/x]`

---

**`η-conversion`** := Extensional equality.

> `λx.(f x) → f`
