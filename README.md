# Engineering Knowledge Base

A reference book on software engineering, written as plain Markdown and versioned like
code. It covers the vocabulary, practices, and platform detail an engineer meets across a
project — from the terms used in a requirements discussion to the services running in
production. It is for practicing engineers who want one place to look something up, and
for engineers preparing for an interview loop, who need the same material stated precisely
enough to say out loud. It assumes you can already program, and does not teach a language.

**Start reading at [docs/welcome.md](docs/welcome.md).**

## How the tree reads

Everything is under [docs/](docs/), in twelve folders numbered `00` to `11`. The numbers
are a reading order, not a filing scheme: the sequence moves from what engineering is,
through how work is organized and how systems are designed, to how they are built and
where they run. Any chapter still stands on its own.

- `00` — [Software Engineering](docs/00-software-engineering/00-software-engineering.md)
- `01` — [Methodology](docs/01-methodology/00-methodology.md)
- `02` — [System Architecture](docs/02-architecture/00-architecture.md)
- `03` — [System Design](docs/03-system-design/00-system-design.md)
- `04` — [Development Process](docs/04-development-process/00-development-process.md)
- `05` — [Coding](docs/05-coding/00-coding.md)
- `06` — [Frontend](docs/06-frontend/00-frontend.md)
- `07` — [AWS](docs/07-cloud-aws/00-aws.md)
- `08` — [Azure](docs/08-cloud-azure/00-azure.md)
- `09` — [Artificial Intelligence](docs/09-ai/00-ai.md)
- `10` — [People Management](docs/10-management/00-management.md)
- `11` — [Interview Preparation](docs/11-interview/00-interview.md)

Inside a folder the rule repeats: the `00-` prefixed file is the chapter overview and
links every one of its siblings, and the rest are numbered in the order they are best
read. `docs/welcome.md` is the only unnumbered file in the tree, because it is the way in.

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
