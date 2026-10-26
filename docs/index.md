---
type: Guide
title: Introduction to Software Engineering
description: The book's entry point — why it exists, what each chapter covers, and the terms it is offered under.
tags: [engineering, handbook, overview]
---

## Preface

This book collects the vocabulary, practices, and reference material an engineer uses across a project — from the terms in a requirements discussion to the services running in production. It is for a practising engineer who wants one place to look things up, instead of a search result and three blog posts of unknown age.

Each chapter stands on its own. Read them in order if the field is new to you, or go straight to the one you came for. The numbers give a reading order, not a filing scheme: from what engineering is, through how work is organized and how systems are designed, to how they are built and where they run.

Everything here was collected over twenty-five years of work in the field. My claim for it is narrow: this much theory has been enough for me, and I have needed nothing beyond it. If that holds for one engineer, there is a fair chance it holds for you. Where it does not, take the book as a [forkable blueprint](https://github.com/arrmagazin/engx) for the one you would write yourself.

Three rules shape the content:

- **Checkable claims.** A claim a reader could falsify is preferred over one that merely sounds right.
- **One definition per term.** A term is defined once, in one place, and referenced from everywhere else.
- **Comparisons, not catalogues.** Where a subject invites an exhaustive list, the book compares instead: the Clouds chapter puts each concept across AWS, Azure and Google Cloud in one table, rather than reproducing three vendor manuals.

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
| **[Backend](07-backend/index.md)** | Distilled references for mainstream server stacks: Java and Spring Boot, Node.js, and .NET |
| **[Clouds](08-clouds/index.md)** | Every cloud concept as AWS, Azure and Google Cloud each implement it, the service-name lookup between them, and the differences that change a design |
| **[Artificial Intelligence](09-ai/index.md)** | The layered stack from machine learning through large language models to agents |
| **[Humans and Teams](10-humans/index.md)** | Leading a team, the roles and the employee lifecycle, growing and keeping people, and knowledge sharing |
| **[Interview Technique](10-humans/21-interview.md)** | Material specific to interview loops: story structure, diagram narration, and the system design framework |

---

## Disclaimer

- **Personal work.** The views here are the author's own, not those of any employer, client, or standards body, and nothing in the book is issued on anyone else's behalf. A few terms are deliberately defined differently from common usage. I give the sense I actually work with, so that the definitions agree with one another and the book reads as one whole rather than a set of borrowed fragments.
- **No warranty.** The material is offered as is, without warranty of any kind. To the extent the law allows, the author accepts no liability for any loss arising from its use.
- **Verify before you ship.** Configuration, security and cloud examples explain an idea; they are not for pasting into production. Check them first against current vendor documentation and your own threat model.
- **A snapshot, not a feed.** Service names, quotas, limits and prices change without notice, and the cloud chapters age fastest. Where a number matters, the provider's documentation is authoritative.
- **Standards are summarized, not reproduced.** References to IEEE 12207, IEEE 29119, IEEE 29148, IEEE 42010, IEEE 830 and ISO/IEC 25010 describe what those documents cover. Where the exact wording matters, read the published standard.
- **Trademarks.** Product and company names belong to their owners and are used for identification only. Their use implies no affiliation with, or endorsement by, the owners.
- **Licence.** Share and adapt the book for non-commercial use, with credit, under the same terms — [CC BY-NC-SA 4.0](https://github.com/arrmagazin/engx/blob/main/LICENSE.md).

---

## Acknowledgements

> Above all, I want to express my sincere gratitude to my family — my wife, my parents and my children. The book owes them its inspiration, and the patience and support that gave it the time to be written.

This book is a distillation: the thinking in it belongs to the field, not to its author.

- **Standards bodies** — IEEE and ISO/IEC, whose published standards give the vocabulary chapters something firmer than common usage to stand on.
- **The authors the chapters lean on most** — the Gang of Four (Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides) on design patterns, Martin Fowler on refactoring and architecture, Kent Beck on extreme programming and test-driven development, Robert C. Martin on design principles, and Eric Evans on domain-driven design.
- **AI assistance** — parts of the book were drafted, restructured and cross-checked with Anthropic's Claude, and pass the same link, frontmatter and glossary checkers as any other contribution. The selection, the claims and the errors stay the author's.
- **Every colleague and reviewer** who asked the question that showed a section was not yet clear.
