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

- Keep edits to markdown content itself — no code, no dependencies to install.
- Preserve the numbered-prefix ordering scheme when adding files; don't renumber existing files without a reason.
