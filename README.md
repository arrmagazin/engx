# Introduction into Software Engineering

A reference book on software engineering, written as plain Markdown and versioned like
code. It covers the vocabulary, practices, and platform detail an engineer meets across a
project — from the terms used in a requirements discussion to the services running in
production. It is for practicing engineers who want one place to look something up, and
for engineers preparing for an interview loop, who need the same material stated precisely
enough to say out loud. It assumes you can already program, and does not teach a language.

**Start reading at [docs/welcome.md](docs/welcome.md).**

## How the tree reads

Everything is under [docs/](docs/), in ten numbered folders. The numbers
are a reading order, not a filing scheme: the sequence moves from what engineering is,
through how work is organized and how systems are designed, to how they are built and
where they run. Any chapter still stands on its own.

- `00` — [Software Engineering](docs/00-software-engineering/index.md)
- `01` — [Methodology](docs/01-methodology/index.md)
- `02` — [System Architecture](docs/02-architecture/index.md)
- `03` — [System Design](docs/03-system-design/index.md)
- `04` — [Development Process](docs/04-development-process/index.md)
- `05` — [Coding](docs/05-coding/index.md)
- `06` — [Frontend](docs/06-frontend/index.md)
- `07` — [Clouds](docs/07-clouds/index.md)
- `09` — [Artificial Intelligence](docs/09-ai/index.md)
- `10` — [Humans and Teams](docs/10-humans/index.md)

The sequence skips `08` and `11`; both are gaps left by earlier reorganizations.

Inside a folder the rule repeats: `index.md` is the chapter overview and links every one
of its siblings, and the rest are numbered in the order they are best read.
`docs/welcome.md` is the only unnumbered file in the tree, because it is the way in.

Two folders are also worth knowing about. [reference/](reference/) holds source material
that is deliberately not part of the book — three single-cloud handbooks the Clouds chapter
was distilled from. [book/](book/) holds the metadata the rendered book is built with.

## Build it as a book

The markdown is the source of truth. To read it as one document:

```sh
python3 scripts/build_book.py
```

That writes `build/engx.epub` and `build/engx.pdf`. It needs `pandoc`, and the PDF also
needs `xelatex`; `--markdown` assembles and checks the structure without rendering either.
Edit `book/metadata.yaml` to change the title, author or rights line: the cover is
generated from those fields over `images/cover-bg.png`, so it follows them.

## Contributing

Every file under `docs/` carries exactly four frontmatter fields, in this order:

```yaml
---
type: Guide
title: CI/CD
description: Explains continuous integration and delivery pipelines and the environment stages code moves through before production.
tags: [devops, ci-cd, development-process]
---
```

`title` must be identical to the file's `#` heading and is never quoted; `description` is
capped at 140 characters. Three checkers enforce that, the rules for definition tables,
and every relative link and heading anchor in the book:

```sh
git ls-files 'docs/*.md' | xargs python3 scripts/check_okf_frontmatter.py
git ls-files 'docs/*.md' | xargs python3 scripts/check_glossary.py
git ls-files 'docs/*.md' | xargs python3 scripts/check_links.py
```

Point git at the repo's hooks once per clone and they run on every commit, over the files
that commit stages:

```sh
git config core.hooksPath .githooks
```

The checkers have their own tests: `python3 -m unittest discover -s scripts -p 'test_*.py'`.
