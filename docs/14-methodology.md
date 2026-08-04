
# Methodology

---

**`Methodology`** := Study of `Method`, practices, and patterns to be applied consistently in a target domain.

> `Methodology := {Method, Practice, Pattern} for Domain`

*NOTE*: Meta-level: methodology is about methods.

---

**`Method`** := An organic set of pre-defined practical decisions, conditional triggers, and choices that organize and control a process.

> `Method := (Decision, Trigger, Choice) → Process control`

*NOTE*: Operational template.

---

**`Framework`** := A system interface allowing users to make choices from predefined options while ensuring valid and consistent `State`.

> `Framework :: user choice → constrained State`

*NOTE*: `Method` made executable.

---

**`Best-Practice`** := A `Method` generally accepted as superior because it produces results superior in a given Context.

> `Best-Practice := argmax_{Method} Outcome | Context`

*NOTE*: Context-bound, not absolute.

## Solution Stages

The lifecycle by which an `Agent` converts a `Goal` into executed action.

---

**`Analysis`** := Survey of `Circumstances` — internal `Resources` and external `Communication` — yielding a `SWOT` partition.

> `Analysis :: Circumstances → (Strengths, Weaknesses, Opportunities, Threats)`

*NOTE*: Feeds `Solution` selection. See `SWOT` below.

---

**`Objective`** := A `SMART`-qualified outcome derived from `Goal`, scoped to a `Step`.

> `Objective := SMART(Goal) at Step`

*NOTE*: Bridge between abstract `Goal` and executable `Task`. See `SMART` below.

---

**`Plan`** := Ordered sequence of `Task` with `Resources`, roles, and schedule that realizes `Objective`.

> `Plan := [Task] with (Resources, roles, schedule)`

*NOTE*: The artifact a `Solution` commits to.

---

**`Task`** := A unit of work equipped with `Purpose`, value outcome, definition of done, required `Resources`, assigned responsibility, timeline, dependencies, and status.

> `Task := (Purpose, DoD, Resources, owner, timeline, deps, status)`

*NOTE*: Atomic executable element of a `Plan`.

---

**`Monitoring`** := Continuous evaluation of progress against `Plan` and adaptation to shifting `Circumstances`.

> `Monitoring :: Step → (Δprogress, ΔCircumstances) → Plan'`

*NOTE*: Closes the loop — failure to monitor is failure to act.

### Solving Approaches

Stances toward a `Problem`. The third row reuses the chapter's `Solution` term in Ackoff's *scientific* sense.

---

**`Absolution`** := Ignoring a `Problem` with hope it self-resolves or vanishes.

> `Absolution :: Problem → ∅`

*NOTE*: Zero-effort; valid when `Cost` of action exceeds `Cost` of `Problem`.

---

**`Resolution`** := Finding a "good enough" answer via past experience, trial and error, common sense.

> `Resolution :: Problem → Solution | satisficing`

*NOTE*: Bounded rationality — fast, not optimal.

---

**`Solution (scientific)`** := Deep study of subject, building a predictable model, seeking optimal outcome.

> `Solution_sci :: Problem → argmax_{Plan} utility via Model`

*NOTE*: The optimizing stance — the chapter's `Solution` executed rigorously.

---

**`Dissolution`** := Eliminating the `Problem` by redesigning the `System` at a different level of organization.

> `Dissolution :: System → System' where Problem ∉ System'`

*NOTE*: Removes the conditions that made the `Problem` possible.

---

**`Divide-&-Conquer`** := Decomposing a `Problem` into sub-`Problem`s until trivial, then composing results back.

> `D&C :: Problem → {sub-Problem} → recompose(Solution)`

*NOTE*: Structural decomposition; orthogonal to the four stances above.

### SMART Goals

Qualifying criteria a `Goal` (or `Objective`) must satisfy to be actionable.

---

**`Specific`** := Distinguished, clear, well-defined — answers who, what, when, where, why, how.

> `Specific(Goal) := unambiguous(Goal)`

*NOTE*: Disambiguation precedes pursuit.

---

**`Measurable`** := Quantifiable — admits progress tracking via `Monitoring`.

> `Measurable(Goal) := ∃ metric: Goal → [0, 1]`

*NOTE*: Without measurement, no `Success` test.

---

**`Achievable`** := Realistic and attainable within `Circumstances`.

> `Achievable(Goal) := Potency(Goal, Circumstances) > 0`

*NOTE*: `Potency`-positive under current `Resources`.

---

**`Relevant`** := Aligned with `Core-Value` and higher-level `Goal`s.

> `Relevant(Goal) := alignment(Goal, Core-Value) > 0`

*NOTE*: Avoids local optima that violate global criteria.

---

**`Time-bound`** := Has a defined timeframe or deadline.

> `Time-bound(Goal) := ∃ deadline ∈ Time`

*NOTE*: Anchors `Goal` to the `Step` sequence.

### SWOT Analysis

The four-cell partition produced by `Analysis` over `Circumstances`.

---

**`Strengths`** := Internal factors giving advantage — `Resources`, expertise, processes, relationships.

> `Strengths := internal(Circumstances) where Δsatisfy(Goal) > 0`

*NOTE*: What the `Agent` brings.

---

**`Weaknesses`** := Internal factors hindering ability — lack of `Resources`, skills, or capabilities.

> `Weaknesses := internal(Circumstances) where Δsatisfy(Goal) < 0`

*NOTE*: What the `Agent` lacks.

---

**`Opportunities`** := External factors to exploit — market trends, emerging technologies, new segments.

> `Opportunities := external(Circumstances) where Δsatisfy(Goal) > 0`

*NOTE*: What the `Environment` offers.

---

**`Threats`** := External factors causing harm — competition, downturns, changing preferences, disruptions.

> `Threats := external(Circumstances) where Δsatisfy(Goal) < 0`

*NOTE*: What the `Environment` imposes.

### Problem-solving

---

**`Problem`** := A factor preventing or impeding `Goal` achievement — conflict of interests, lack of `Resources`, runtime failure, miscommunication, or delusion.

> `Problem :: Circumstances → Δ(Goal-progress) < 0`

*NOTE*: The negative `Communication` a `Solution` must overcome. `Risk` (above) measures anticipated `Problem`s.

---

**`Failure`** := A `Solution` whose execution does not achieve the `Goal`, or achieves it at the expense of overall `Potency`.

> `Failure :: ¬Goal-achieved ∨ ΔPotency < 0`

*NOTE*: The negation of `Success`. `Failure` is *informative*: a `Solution` that fails refines `Knowledge` about `Circumstances` and feeds `Learning` ([07-intellect](07-intellect.md)).

---

**`Risk`** := The variance of `Outcome` across the `Potency`-weighted distribution of `Future`s reachable from a `Solution`.

> `Risk(Solution) := variance over (Outcome × Potency) given Circumstances`

*NOTE*: An `Agent`'s risk tolerance is part of its decision profile.

---

**`Trade-off`** := A `Solution` in which one `Core-Need` is satisfied at measurable `Cost` to another.

> `Trade-off :: Δsatisfy(Core-Need_i) > 0 ∧ Δsatisfy(Core-Need_j) < 0`

*NOTE*: Inherent whenever `Resources` are bounded and `Core-Need`s are multiple. `Trade-off` recognition is what distinguishes a thoughtful `Agent` from a single-axis optimizer.

---

**`Contingency`** := The variance attributable to `Problem`s that *cannot* be anticipated — disjoint from `Risk`.

> `Contingency :: variance over unanticipated Outcome`

*NOTE*: Reserved buffer for the unknown.
