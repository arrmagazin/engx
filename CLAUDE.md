# Engx

A personal engineering knowledge base written as markdown, organized as a numbered-folder "book" under `docs/`. The markdown is the source of truth. Three checkers in `../arrmatura-books/scripts/` enforce the conventions below. This repo also hosts the site (<https://software-engineering.web.app>) and builds the book as EPUB and PDF, with tooling from the sibling checkout `../arrmatura-books` (see **Site and book**).

## Structure

- `docs/` — the book: eleven numbered folders plus one root entry point, `docs/index.md`. `docs/08-clouds/_references/` holds the three single-cloud handbooks the Clouds chapter was distilled from; the chapter index links them, so they follow the same conventions and checkers as every other doc.
- `README.md` — the repository's front page, written for a human, not an agent.

**The numbering rule.** Folder prefixes are unique and encode reading order: `00-software-engineering`, `01-methodology`, `02-architecture`, `03-system-design`, `04-development-process`, `05-coding`, `06-frontend`, `07-backend`, `08-clouds`, `09-ai`, `10-humans`. `11` is unused — a gap left by an earlier reorganization, not a placeholder. Inside each folder, `index.md` is the chapter overview and links every one of its siblings; the rest are numbered in the order they are read. Every folder and file name is kebab-case. Preserve all of this when adding a file, and don't renumber existing files without a reason.

## Checkers

`.githooks/pre-commit` runs all three over the `docs/*.md` files a commit stages, under an `ACMR` filter so pure renames are checked too. Each clone enables the hook once with `git config core.hooksPath .githooks`. To run them over the whole book, `npm run check` (all three, each run even if an earlier one fails) or `npm run check:frontmatter` / `check:glossary` / `check:links` (one).

Those scripts pipe `git ls-files 'docs/*.md'` through `xargs`; keep it that way. Pipe through `xargs` rather than collecting the paths in a variable: zsh does not word-split unquoted *parameter* expansions, so `files=$(git ls-files 'docs/*.md')` followed by `bun ../arrmatura-books/scripts/check-links.ts $files` passes all 60 paths as one filename. `.githooks/pre-commit` is written in that shape and is correct only because its `#!/bin/sh` shebang selects a shell that does split.

- `check-okf-frontmatter.ts` — the frontmatter convention below.
- `check-glossary.ts` — the glossary convention below.
- `check-links.ts` — every relative link resolves, and every `#anchor` names a heading that exists in the target file. It reads the files it is given *plus their targets*, so staging the referring file catches a broken link; renaming a heading and staging only that file does not. Run it over the whole book after a merge for that reason.

## Site and book

- `www/` — the Firebase public root. `index.html`, `service-worker.js` and `onload.js` are written by `npm run gen`; never edit them by hand. `favicon.svg`, `site.webmanifest` and `robots.txt` (AI crawlers disallowed) are this site's own. `firebase.json` adds the `tdm-reservation: 1` header to every response.
- `index.ts` — the UI entry: calls `launchBook` from `../arrmatura-books`. Built into `www/dist/` (gitignored) by `npm run build`, which `deploy` runs first.
- `book/` — `cover.png`, the book's cover photograph. Not served. The book's metadata is `package.json` `book`.
- `package.json` is the site's config: `displayName`, `description`, `author`, `keywords`, `copyright` and `store` reach the page through `gen`.

The site reads the docs from jsDelivr at the **tag** of `package.json` `version`, not from the working tree. The book builds from the working tree.

| Command | What it does |
| --- | --- |
| `npm run release` | Publishes doc changes: bump, `gen`, commit, push, tag, deploy. Needs a clean `main` |
| `npm run book` | `build/engx.epub` and `.pdf` from `docs/`; `-- --markdown` checks structure only |
| `npm start` / `npm run stop` | Serves `www/` on :8092, rebuilds the UI on change, opens the browser / frees :8092 |
| `npm run build` | `www/dist/` (gitignored): the UI bundle from `index.ts`, which calls `launchBook`, and its CSS |
| `npm run deploy` | `deploy` runs `build` first |

How the tooling works: `../arrmatura-books/site/README.md` and `../arrmatura-books/book/README.md`.

## Images and links

- The docs carry no figures of their own: every illustration is a mermaid diagram in the prose. An image, if one is ever added, is referenced by a relative path, never root-absolute, and must not be SVG — xelatex cannot embed SVG, so the PDF build would drop it. Use a mermaid diagram or a PNG instead.
- Docs link to each other the way they do on GitHub — `sibling.md`, `sub/child.md`, `../other-dir/doc.md`. The site resolves each href against the document it appears in, so all of them navigate in-app; the book turns them into intra-document anchors. Bare `#anchor` links do nothing on the site, which is hash-routed.

## Frontmatter convention

Every file under `docs/` starts with **OKF (Open Knowledge Format) v0.2** YAML frontmatter, kept to the minimal field set — these four, in this order, and nothing else:

```yaml
---
type: Guide
title: <the document's heading, never quoted>
description: <one sentence, at most 140 characters>
tags: [lowercase, kebab-or-single-word, tags]
---
```

- `type` is always `Guide` in this repo (no data/computation assets live here).
- The frontmatter block is the very first thing in the file, and the body follows it directly.
- There is no H1. The `title` is the heading: the site renders it, and the book builder opens each document with `# <title>`. A `# Title` line would print twice, so the checker rejects any level-1 heading in the body (fenced code excluded).
- A quoted `title` fails the checker, because the quotes become part of the value and would print in the heading.
- Don't add OKF's optional provenance/trust fields (`sources`, `generated`, `verified`, `status`); the checker rejects them.
- Field *order* and the "nothing else" rule are conventions the checker does not enforce. Follow them anyway.

## Working conventions

- Prefer standard English; no fancy or rare words, no idioms.
- The content is markdown. The checkers are TypeScript on the Node standard library, run by `bun`, and stay that way — no dependencies to install.
- Anything asserted in the book should be checkable. Prefer a claim a reader could falsify over one that merely sounds right.

## Glossary conventions

These apply to any file that defines terms in a **definition list** — the [extended markdown syntax](https://www.markdownguide.org/extended-syntax/#definition-lists) — such as `docs/00-software-engineering/01-glossary.md`. They were two-column tables until 2026-09-12; a definition is now free to hold a list or a second paragraph, and a long one wraps to the full measure instead of a narrow column.

`check-glossary.ts` checks the mechanical rules below: entries a renderer would silently fold together, duplicate terms, self-restating definitions, trailing periods, and pairs of terms that define each other. Definition lists are used in this book for exactly one thing, so every one of them is in scope and no header row marks them; comparisons, ladders and nav tables stay tables and are not read. Indirect loops and oversized lists print as notes without failing. Cross-reference casing, grounding, and whether a term earns its row need judgement and are not checked.

Note also what it cannot see: its duplicate-term check is per file, so the same term defined once in each of two chapters passes. That is a real hazard in a book this size — see the two senses of *Framework* in `01-methodology/index.md` and `03-system-design/index.md`, which are disambiguated in prose because no checker could catch them.

### Shape

- One entry per term: the term alone on its line, the definition on the next behind `: `, and **a blank line before the next term**. No bold on the term — every renderer emphasizes a `<dt>` itself — and no trailing period.

  ```markdown
  Solution
  : An artificial phenomenon a Team designs for someone outside it

  Stakeholder
  : Any party whose interests are at stake in a Solution's outcome
  ```

- Definitions are noun phrases, not sentences. Never restate the term inside its own definition.
- Keep them terse: the definition, plus at most one `;` or `—` clause saying why the term matters or how it is used.
- A definition that needs a **line break** ends the line above with a trailing `\`. A bare second line is folded into the definition instead and the break is lost.
- A definition that needs a **list or a second paragraph** uses the `:   ` marker and indents that block by four spaces, so it stays inside the definition. Unindented, the block escapes the definition and splits the list in two — it renders, which is what makes this worth checking for.

  ```markdown
  Solution
  :   An artificial phenomenon:

      - intentionally designed by a Team
      - observable and measurable at any moment
  ```

- Where a `##` section is named after a term the list defines, put that definition first (`## Delivery` → `Delivery`). Sections named after a grouping rather than a term have no such entry.

### References between terms

- Capitalize a term when referring to another defined term; lowercase it when using the ordinary word. Capitalized means "this is defined in this file".
- Every capitalized reference must resolve to an entry in the same file. No dangling references.
- No two terms may define each other. If A's definition needs B and B's needs A, redefine one from first principles so it stands alone.
- Longer loops that run through a hub term (most definitions mention `Solution`) are tolerated — they are reported as notes, not failures.
- State each relationship once, in one direction. If `Goals` says "decomposed into Objectives", `Objectives` must not say "supporting Goals".
- A term's own entry is the only place its meaning lives; don't repeat it inside another definition.

### Grounding

- Chains of definitions must bottom out in something observable — a State, a Metric, a measurable condition — not in another abstraction.

### Restrictions

- Don't put prose paragraphs between entries; explanation belongs in the definition itself or in a separate doc.
- Don't introduce a term nothing else references — if no other definition needs it, question whether it belongs.
- Order entries by the dependency chain: roots first, verified outcomes last. Don't reorder for aesthetics.
- Past roughly a dozen entries, split the list into a new `##` section with its own heading term rather than letting one list grow.
