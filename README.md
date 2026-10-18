# Introduction into Software Engineering

A reference book on software engineering, written as plain Markdown and versioned like
code. It covers the vocabulary, practices, and platform detail an engineer meets across a
project — from the terms used in a requirements discussion to the services running in
production. It is for practicing engineers who want one place to look something up, and
for engineers preparing for an interview loop, who need the same material stated precisely
enough to say out loud. It assumes you can already program, and does not teach a language.

**Start reading at [docs/index.md](docs/index.md).**

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

## Read it as a site

The site — <https://software-engineering.web.app>

## Contributing

```sh
npm run check         # all three, reporting every failure
npm run check:links   # one of them (or check:frontmatter, check:glossary)
```

The checkers have their own tests: `npm test`.
