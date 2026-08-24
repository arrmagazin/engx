# Engx

A personal engineering knowledge base written as markdown notes, organized as a numbered-folder "book" under `docs/`. There is no build tooling (no `package.json`, no static-site generator) — the content is the product.

## Structure

- `docs/NN-topic/*.md` — numbered top-level folders order the "book" by theme (e.g. `01-methodology`, `03-architecture`, `05-coding`, `06-testing`, `08-frontend`, `30-agentic`, `40-interview`). Files inside a folder are also numbered where order matters.
- `images/` — images referenced by docs (e.g. `/images/welcome.svg`).
- `texts/` — scratch/overflow notes not yet folded into `docs/`.

## Frontmatter convention

Every file under `docs/` starts with **OKF (Open Knowledge Format) v0.2** YAML frontmatter, kept to the minimal field set:

```yaml
---
type: Guide
title: <from the file's H1>
description: <one sentence, under ~140 chars>
tags: [lowercase, kebab-or-single-word, tags]
---
```

- `type` is always `Guide` in this repo (no data/computation assets live here).
- When adding a new doc or a new H1, add/update this frontmatter block as the very first thing in the file — before the H1.
- Don't add OKF's optional provenance/trust fields (`sources`, `generated`, `verified`, `status`, etc.) here; this repo doesn't use them.
- A pre-commit hook (`.githooks/pre-commit`, running `scripts/check_okf_frontmatter.py`) enforces this on every commit that touches `docs/*.md`. Each clone must enable it once via `git config core.hooksPath .githooks`.

## Working conventions

- Prefer standard English, no fancy or rare words or idioms.
- Keep edits to markdown content itself — no code, no dependencies to install.
- Preserve the numbered-prefix ordering scheme when adding files; don't renumber existing files without a reason.

## Glossary conventions

These apply to any file that defines terms in a `| Concept | Definition |` table, such as `docs/00-software-engineering/01-glossary.md`.

`scripts/check_glossary.py <files>` checks the mechanical rules below: broken rows, duplicate terms, self-restating definitions, trailing periods, and pairs of terms that define each other. It only looks at tables headed `| Concept | Definition |`, so other tables are unaffected. Indirect loops and oversized tables print as notes without failing. Cross-reference casing, grounding, and whether a term earns its row need judgement and are not checked. The script is not wired into the pre-commit hook.

### Shape

- One row per term, one line per row: `| **Term** | definition |`. No trailing period.
- Definitions are noun phrases, not sentences. Never restate the term inside its own definition.
- Keep them terse: the definition, plus at most one `;` or `—` clause saying why the term matters or how it is used.
- Never put a raw newline inside a table cell — it terminates the row and breaks the table. Use `<br>` when a cell genuinely needs a list.
- Every `##` section defines the term it is named after, as the first row of its table (`## Delivery` → `**Delivery**`).

### References between terms

- Capitalize a term when referring to another defined term; lowercase it when using the ordinary word. Capitalized means "this is defined in this file".
- Every capitalized reference must resolve to a row in the same file. No dangling references.
- No two terms may define each other. If A's definition needs B and B's needs A, redefine one from first principles so it stands alone.
- Longer loops that run through a hub term (most rows mention `Solution`) are tolerated — they are reported as notes, not failures.
- State each relationship once, in one direction. If `Goals` says "decomposed into Objectives", `Objectives` must not say "supporting Goals".
- A term's row is the only place its meaning lives; don't repeat it inside another row.

### Grounding

- Chains of definitions must bottom out in something observable — a State, a Metric, a measurable condition — not in another abstraction.
- Prefer a definition that can be falsified over one that merely sounds right.

### Restrictions

- Don't put prose paragraphs between rows of a table; explanation belongs in the definition itself or in a separate doc.
- Don't introduce a term nothing else references — if no other row needs it, question whether it belongs.
- Order rows by the dependency chain: roots first, verified outcomes last. Don't reorder for aesthetics.
- Past roughly a dozen rows, split the table into a new `##` section with its own heading term rather than letting one table grow.
