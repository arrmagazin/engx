# Engx

A personal engineering knowledge base written as markdown, organized as a numbered-folder "book" under `docs/`. The markdown is the source of truth and there is no site generator; `scripts/build_book.py` renders it as an EPUB and a PDF on demand. The code is `scripts/`: three checkers that enforce the conventions below, plus the book builder.

## Structure

- `docs/` — the book: ten numbered folders plus one unnumbered entry point, `docs/welcome.md`.
- `images/` — images referenced by docs, always by a relative path (`../images/welcome.svg` from `docs/`, `../../images/…` from a chapter folder), never root-absolute.
- `reference/` — source material that is **not** part of the book: three single-cloud handbooks the Clouds chapter was distilled from. Outside `docs/`, so outside the checkers and outside the build. Nothing in `docs/` links into it. See `reference/README.md`.
- `book/metadata.yaml` — title, author, rights and subjects for the rendered book. `build/` — the rendered outputs, gitignored.
- `scripts/` — the three checkers, the book builder, and their tests. `.githooks/` — the hook that runs the checkers. `README.md` — the repository's front page, written for a human, not an agent.

**The numbering rule.** Folder prefixes are unique and encode reading order: `00-software-engineering`, `01-methodology`, `02-architecture`, `03-system-design`, `04-development-process`, `05-coding`, `06-frontend`, `07-clouds`, `09-ai`, `10-humans`. `08` and `11` are unused — gaps left by earlier reorganizations, not placeholders. Inside each folder, `index.md` is the chapter overview and links every one of its siblings; the rest are numbered in the order they are read. Every folder and file name is kebab-case. Preserve all of this when adding a file, and don't renumber existing files without a reason.

## Checkers

`.githooks/pre-commit` runs all three over the `docs/*.md` files a commit stages, under an `ACMR` filter so pure renames are checked too. Each clone enables the hook once with `git config core.hooksPath .githooks`. To run one over the whole book:

```sh
git ls-files 'docs/*.md' | xargs python3 scripts/check_links.py
```

Pipe through `xargs` rather than collecting the paths in a variable: zsh does not word-split unquoted *parameter* expansions, so `files=$(git ls-files 'docs/*.md')` followed by `python3 scripts/check_links.py $files` passes all 62 paths as one filename. `.githooks/pre-commit` is written in that shape and is correct only because its `#!/bin/sh` shebang selects a shell that does split.

- `check_okf_frontmatter.py` — the frontmatter convention below.
- `check_glossary.py` — the glossary convention below.
- `check_links.py` — every relative link resolves, and every `#anchor` names a heading that exists in the target file. It reads the files it is given *plus their targets*, so staging the referring file catches a broken link; renaming a heading and staging only that file does not. Run it over the whole book after a merge for that reason. Its own tests: `python3 -m unittest discover -s scripts -p 'test_*.py'`.

## The book build

`scripts/build_book.py` assembles `docs/` into one document and renders it twice:

```sh
python3 scripts/build_book.py              # build/engx.epub and build/engx.pdf
python3 scripts/build_book.py --markdown   # assemble and verify only, render nothing
```

It is stdlib-only Python, like the checkers; pandoc and (for the PDF) xelatex do the
rendering. Four things it does that pandoc cannot, each with tests in
`scripts/test_build_book.py`:

- **Reading order.** `welcome.md` first, then folders in numeric order, each led by its
  `index.md`, which keeps its heading level and so reads as the chapter opener. Siblings
  are demoted one level beneath it.
- **Unique heading ids.** Every heading gets an explicit `{#doc-anchor--section}` id,
  because section names like "Best Practices" repeat across chapters and a renderer would
  otherwise silently renumber them and send links to the wrong chapter.
- **Link rewriting.** Cross-document links become intra-document anchors. A link with no
  anchor points at the target document's title.
- **Normalizing `---`.** A bare dashed line is ambiguous in pandoc's markdown — YAML
  metadata, a setext underline, or a multiline-table delimiter. Read as the last of those
  it swallows every following heading into table cells, with a zero exit code. The builder
  emits `***` instead, and then `verify_anchors` re-renders the assembled file and fails the
  build if any declared heading id or link target did not survive.

**The PDF layout.** A reading book rather than a paper: the `book` class one-sided on A4,
11pt on 1.15 leading, 2.5cm/2.8cm margins, `--top-level-division=chapter` so a folder opens
a chapter on a fresh page, and running heads carrying the chapter title. That is 250 pages.
Inline code is made breakable with `seqsplit`, because identifiers like
`iam.disableServiceAccountKeyCreation` are otherwise unbreakable and run into the margin —
except inside a table, where the plain `\texttt` is restored, since narrow columns would
break a short token like `split("\n")` mid-word and make it read as two.

Two limits worth knowing. The PDF omits images, because xelatex cannot embed SVG and this
machine has no rasterizer. And the PDF sets `Times New Roman` with `Menlo` for code, the
fonts verified to cover the box-drawing characters the diagrams use; if either is missing
the PDF still builds, with those glyphs dropped.

## Frontmatter convention

Every file under `docs/` starts with **OKF (Open Knowledge Format) v0.2** YAML frontmatter, kept to the minimal field set — these four, in this order, and nothing else:

```yaml
---
type: Guide
title: <byte-identical to the file's H1, and never quoted>
description: <one sentence, at most 140 characters>
tags: [lowercase, kebab-or-single-word, tags]
---
```

- `type` is always `Guide` in this repo (no data/computation assets live here).
- The frontmatter block is the very first thing in the file, and the H1 is the first non-blank line after it.
- A quoted `title` fails the checker, because the quotes become part of the value and it stops matching the H1.
- Don't add OKF's optional provenance/trust fields (`sources`, `generated`, `verified`, `status`); the checker rejects them.
- Field *order* and the "nothing else" rule are conventions the checker does not enforce. Follow them anyway.

## Working conventions

- Prefer standard English; no fancy or rare words, no idioms.
- The content is markdown. `scripts/` is the only code, it is stdlib-only Python 3, and it stays that way — no dependencies to install, and no test framework beyond `unittest` (pytest is not available here).
- Anything asserted in the book should be checkable. Prefer a claim a reader could falsify over one that merely sounds right.

## Glossary conventions

These apply to any file that defines terms in a `| Concept | Definition |` or `| Component | Definition |` table, such as `docs/00-software-engineering/01-glossary.md`.

`check_glossary.py` checks the mechanical rules below: broken rows, duplicate terms, self-restating definitions, trailing periods, and pairs of terms that define each other. It only looks at tables with one of those two header rows, so other tables — ladders, comparisons, nav tables — are unaffected. Indirect loops and oversized tables print as notes without failing. Cross-reference casing, grounding, and whether a term earns its row need judgement and are not checked.

Note also what it cannot see: its duplicate-term check is per file, so the same term defined once in each of two chapters passes. That is a real hazard in a book this size — see the two senses of *Framework* in `01-methodology/index.md` and `03-system-design/index.md`, which are disambiguated in prose because no checker could catch them.

### Shape

- One row per term, one line per row: `| **Term** | definition |`. No trailing period.
- Definitions are noun phrases, not sentences. Never restate the term inside its own definition.
- Keep them terse: the definition, plus at most one `;` or `—` clause saying why the term matters or how it is used.
- Never put a raw newline inside a table cell — it terminates the row and breaks the table. Use `<br>` when a cell genuinely needs a list.
- Where a `##` section is named after a term the table defines, put that definition in the first row (`## Delivery` → `**Delivery**`). Sections named after a grouping rather than a term have no such row.

### References between terms

- Capitalize a term when referring to another defined term; lowercase it when using the ordinary word. Capitalized means "this is defined in this file".
- Every capitalized reference must resolve to a row in the same file. No dangling references.
- No two terms may define each other. If A's definition needs B and B's needs A, redefine one from first principles so it stands alone.
- Longer loops that run through a hub term (most rows mention `Solution`) are tolerated — they are reported as notes, not failures.
- State each relationship once, in one direction. If `Goals` says "decomposed into Objectives", `Objectives` must not say "supporting Goals".
- A term's row is the only place its meaning lives; don't repeat it inside another row.

### Grounding

- Chains of definitions must bottom out in something observable — a State, a Metric, a measurable condition — not in another abstraction.

### Restrictions

- Don't put prose paragraphs between rows of a table; explanation belongs in the definition itself or in a separate doc.
- Don't introduce a term nothing else references — if no other row needs it, question whether it belongs.
- Order rows by the dependency chain: roots first, verified outcomes last. Don't reorder for aesthetics.
- Past roughly a dozen rows, split the table into a new `##` section with its own heading term rather than letting one table grow.
