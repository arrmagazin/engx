# Fundamental definitions

## Formal Language

**`Symbol`**  
:= A finite tuple from `0` and `1`.
:= `[ 0 | 1] `

**`Alphabet`**  
:= A finite set of `Symbol`s.
:= `{ Symbolᵢ :: endemic }`

**`Word<Alphabet>`**
:= A `Tuple` of `Symbol`s of given `Alphabet`.
:= `[Symbolᵢ,...] :: Symbolᵢ ∈ Alphabet`

**`Dictionary<Alphabet>`** := `{ Word<Alphabet> }`
:= A `Set` of `Word`s of the same `Alphabet`.

**`Text<Dictionary>`** := `[Word ∈ Dictionary]`
:= A `Tuple` of `Word`s of the same `Dictionary`.

---

**`Rule<Dictionary>`** := `(S → S') :: S, S' ∈ Dictionary`
:= An `Arrow` from/to `Word`s of the same `Dictionary`.

**`Grammar<Dictionary>`** := `{ Rule × Rule :: Rule<Dictionary>}`
:= A `Graph` on `Rule`s over the `Dictionary`.

**`Conclusion<Grammar>`** := (*Rule₁ . … . Ruleₙ) :: [Rule₁,…,Ruleₙ] ∈ Path<Grammar>`
:= A `Composition` over `Rule`s from some`Path` in the `Grammar`.

**`Expression<Word, Grammar>`** := `Conclusion<Grammar>(Word)`
:= the `Value` of some `Conclusion` within the `Grammar` for some input `Word`.

**`Theory<Word, Grammar>`** := `{ Expression<Word, Grammar> }`
:= the `Dictionary` of all `Expression`s that may be derived from the input `Word` within the `Grammar`.

---

**`Axiom<Grammar>`** := `¬∃ Word :: Expression<Word, Grammar> = Axiom`
:= `Word` that cannot be expressed in the `Grammar`.

**`Termin<Grammar>`** := `Word :: Theory<Termin, Grammar> = Zero`
:= A terminal `Expression` from which nothing more can be derived.

**`Formal-Language<Axiom,Grammar>`** := `{ Termin :: Termin ∈ Theory<Axiom, Grammar> }`
:= A `Dictionary` of all `Termin`s, expressed from given `Axiom` and `Grammar`.

## Knowledge

**`Opinion`** := An `Expression` of `Language` associated with an evaluation of whether `Presentation` belongs to `Place`.

> `Opinion :: Expression → (Presentation × Place → {0, 1})`

*NOTE*: The atomic unit of belief — a proposition asserting membership of entities in categories.

---

**`Thesis`** := A `Set` of `Opinion` in Logic.

> `Thesis := {Opinion}` in Logic

*NOTE*: `Knowledge` derived from pure reason alone — a heuristic conjecture awaiting `Validation`.

---

**`Theory`** := A set of Terms — `Name` and `Concept` — for `Opinion` over a `Language` (Logic) and an `Attribute-Space` (`Reality`).

> `Theory := ({Name}, {Concept}, Language, Attribute-Space)`

*NOTE*: A *coordinated vocabulary plus the inferential machinery* that lets `Opinion` combine into `Thesis`.

---

**`Name`** := An `Expression` of `Language` associated with `Presentation` (Entities) of the `Attribute-Space`.

> `Name :: Expression → Presentation`

*NOTE*: Picks out particular instances. Complement: `Concept`.

---

**`Concept`** := An `Expression` of `Language` associated with `Place` (regions) of the `Attribute-Space`.

> `Concept :: Expression → Place`

*NOTE*: Denotes categories rather than instances. Aligns with Frege's distinction between Sense and Reference.

---
**`Knowledge`** := A `Theory` used to describe, explain, predict and act upon `Reality`.

> `Knowledge := {Opinion}`

The four properties of well-formed `Knowledge`: 
- **adequate** (matches observed `Presentation`), 
- **accessible** (retrievable from `Memory`), 
- **coherent** (internally non-contradictory), 
- **predictive** (allows anticipation of future `State`). 

`Knowledge` is not Being itself — only its representation.

