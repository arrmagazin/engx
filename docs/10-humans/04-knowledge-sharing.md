---
type: Guide
title: Knowledge Sharing
description: Healthy vs. unhealthy knowledge sharing, what each costs a team, and the practices that keep project knowledge findable.
tags: [development-process, knowledge-sharing, team]
---

**Knowledge sharing** is how a team passes information, expertise and skills between its members: talk, meetings, documents, workshops and recordings. It keeps a project moving, and it stops repeated work, such as bringing in a new member, from costing the same hours every time. This guide is for every team member, new ones included.

## Healthy vs. Unhealthy Knowledge Sharing

- **Healthy** sharing keeps delivery risk low. It covers shared topics (code, technology, domain facts) and what each person knows well, through meetings, a knowledge base, chats, videos or online courses. It is give and take: everyone adds, and everyone can count on the others.
- **Unhealthy** sharing slows or stops delivery. It takes two forms:
  - holding knowledge back, fully or in part — it looks careless or selfish and costs trust;
  - material that is out of date or wrong — it misleads more than it helps.

Keeping it healthy is the whole team's duty, not only its leaders'.

## Risks and Benefits

| Area | Unhealthy Sharing | Healthy Sharing |
| --- | --- | --- |
| **Priorities** | Unclear: people do needless work or redo it wrongly | Clear: the team works on what matters and keeps to schedule |
| **Standards** | Ignored: confusion and weaker output | Written down: output stays consistent |
| **Information Access** | Answers live in talk or a messy knowledge base; people wait, and may still not get them | Answers are written, easy to find, and kept current by all |
| **Bus Factor** | One: a single absence stops progress | Above one: anyone can be away and delivery goes on |
| **Onboarding** | Partial handover: slow, confusing, new members add little and lose drive | Quick and cheap for the new member and the team |

The **bus factor** is how many people must become unavailable before a system or process stops (see [Growing and Keeping People](03-growing-and-keeping-people.md#core-concepts)). At one, a holiday, leave or exit of the only person who knows something halts the work.

## Four Areas to Improve

### Software Development Life Cycle

- **Rotate reviewers**, so each part of the solution gets fresh eyes ([Code Review](../04-development-process/02-code-review.md)).
- **Spread the work**: keep at least two people familiar with each area, instead of always giving one kind of task to the same person.
- **Write findings down while the task is open**, and update the knowledge base when something important changes.
- **Count documentation in estimates**, so keeping it current does not depend on spare time.

### Knowledge Base

One shared space, such as a wiki, that every member can open and helps maintain. It holds:

- the project's goal and description
- team members and their roles
- links to project resources and environments
- the standards and conventions for each role ([Coding Standards](../00-software-engineering/02-standards.md))
- branching, releases and the task life cycle ([Version Control](../04-development-process/01-version-control.md), [CI/CD](../04-development-process/03-ci-cd.md))

### Onboarding Procedures

- **A starter guide**: the first page a new member reads. It points to resources, the knowledge base and environment setup, and the whole team keeps it current.
- **A mentor** for each new member, who answers questions and is accountable for helping them settle in ([Roles and the Employee Lifecycle](02-roles-and-lifecycle.md)).

### Team Communication

- **Regular sharing sessions** on progress and plans, to catch problems while they are small.
- **One topic per chat**, with everyone that topic needs.
- **A separate channel for important news**, tagging who must act, so it is not lost in daily traffic.
- **Project-wide updates** from the people who lead the project and its technical direction, on news, deadlines and the larger goal, so the team sees where its work fits.
- **Meeting notes** from the organizer to attendees and anyone concerned, which also record what was decided.

## Suggesting Improvements

Anyone can spot a gap. A new member often spots it first, because they are the one who cannot find the answer. What to do with a gap depends on who can close it.

- **A gap in the content** — the team can close it itself, so raise it in the team's usual channel or fix it at once. Typical cases:
  - an idea or fact others could use;
  - an answer that so far lives only in conversation;
  - an important fact the documents leave out;
  - a knowledge-base page that no longer matches the project.
- **A gap in the process** — it needs someone who can change how the team works, so take it to the team lead or your mentor. Typical cases:
  - status or recent changes that nobody can find;
  - communication that breaks down inside the team or with other teams;
  - work that poor sharing slows down, or that better sharing would speed up;
  - a knowledge base that nobody looks after.
