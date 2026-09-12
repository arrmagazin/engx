---
type: Guide
title: Introduction into Software Engineering
description: The book's entry point — why it exists, what each chapter covers, and the terms it is offered under.
tags: [engineering, handbook, overview]
---

# Introduction into Software Engineering

## Preface

This book collects the vocabulary, practices, and reference material an engineer uses across a project — from the terms in a requirements discussion to the services running in production.

It is written for  a practising engineer who wants one place to look something up, instead of a search result and three blog posts of unknown vintage.

Each chapter stands on its own, so read them in order if the field is new to you, or go straight to the one you came for. The numbers are a reading order rather than a filing scheme: they move from what engineering is, through how work is organized and how systems are designed, to how they are built and where they run.

Everything here was collected and composed over twenty-five years of working in the field. The claim I make for it is a narrow one: this much theory has been enough for me, and I have needed nothing beyond it. If that holds for one engineer, there is a fair chance it holds for you as well. And where it does not, take the book as a blueprint — a scaffold for the one you would write yourself.

Three rules shape the content. Anything asserted should be checkable — a claim a reader could falsify is preferred over one that merely sounds right. A term is defined once, in one place, and referenced from everywhere else. And where a subject invites an exhaustive catalogue, the book gives a comparison instead: the Clouds chapter puts the same concept across AWS, Azure and Google Cloud in one table rather than reproducing three vendor manuals.

---

## In This Book

| Chapter | What it covers |
| --- | --- |
| **[Software Engineering](00-software-engineering/index.md)** | The shared vocabulary, the published standards, and the map of engineering disciplines |
| **[Methodology](01-methodology/index.md)** | How work is organized — lean, agile, scrum, extreme programming, moving quality earlier, and engineering management |
| **[System Architecture](02-architecture/index.md)** | Architecture as a discipline, the views it is described through, and the quality attributes it is judged against |
| **[System Design](03-system-design/index.md)** | Databases, caching, messaging, containers, client-server communication, data formats, and worked designs of canonical systems |
| **[Development Process](04-development-process/index.md)** | Version control, code review, CI/CD, quality assurance, testing, debugging, and technical debt |
| **[Coding](05-coding/index.md)** | Paradigms, design principles, design patterns, code smells, and code quality |
| **[Frontend](06-frontend/index.md)** | Application types, browser technologies, performance, accessibility, and web application security |
| **[Clouds](07-clouds/index.md)** | Every cloud concept as AWS, Azure and Google Cloud each incarnate it, the service-name lookup between them, and the differences that change a design |
| **[Artificial Intelligence](09-ai/index.md)** | The layered stack from machine learning through large language models to agents |
| **[Humans and Teams](10-humans/index.md)** | Leading a team, the roles and the employee lifecycle, growing and keeping people, and knowledge sharing |
| **[Interview Technique](10-humans/21-interview.md)** | Material specific to interview loops: story structure, diagram narration, and the system design framework |

---

## Disclaimer

- **Personal work.** The views here are the author's own. They are not those of any employer, client, or standards body, and nothing in the book is issued on anyone else's behalf. A few concepts and terms here are not stated the way common usage states them. That is deliberate: I give the sense I actually work with, so that the definitions agree with one another and the book reads as one coherent whole rather than a set of borrowed fragments.
- **No warranty.** The material is offered as is, without warranty of any kind. The author accepts no liability for any loss arising from its use.
- **Verify before you ship.** Configuration, security and cloud examples are written to explain an idea, not to be pasted into production. Check them against current vendor documentation and your own threat model first.
- **A snapshot, not a feed.** Service names, quotas, limits and prices change without notice, and the cloud chapters age fastest. Where a number matters, treat the provider's documentation as authoritative.
- **Standards are summarized, not reproduced.** References to IEEE 12207, IEEE 29119, IEEE 29148, IEEE 42010, IEEE 830 and ISO/IEC 25010 describe what those documents cover. Where the exact wording matters, read the published standard.
- **Trademarks.** Product and company names are the property of their owners and are used for identification only. Their use implies no affiliation with, or endorsement by, the owners.

---

## Acknowledgements

> Above all, I want to express ny sincere gratitude to my family — my wife, my parents and my children. The book owes them its inspiration, and the patience and support that gave it the time to be written.

This book is a distillation, and the thinking in it belongs to the field rather than to its author.

- **Standards bodies** — IEEE and ISO/IEC, whose published standards give the vocabulary chapters something firmer than common usage to stand on.
- **The authors whose work the chapters lean on most** — the Gang of Four (Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides) on design patterns, Martin Fowler on refactoring and architecture, Kent Beck on extreme programming and test-driven development, Robert C. Martin on design principles, and Eric Evans on domain-driven design.
- **AI assistance** — parts of the book were drafted, restructured and cross-checked with Anthropic's Claude, run against the same link, frontmatter and glossary checkers any other contribution passes. The selection, the claims and the errors stay the author's.
- **Every colleague and reviewer** who asked the question that showed a section was not yet clear.
