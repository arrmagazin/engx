---
type: Guide
title: Knowledge Sharing
description: Explains healthy vs. unhealthy knowledge sharing, its effect on delivery risk, and the practices that keep project knowledge findable.
tags: [development-process, knowledge-sharing, team]
---

Knowledge sharing is the exchange of information, expertise, and skills across a team — through conversations, regular meetings, documentation, workshops, and recorded sessions. Done well it keeps a project running, and it stops recurring work such as onboarding from costing the team the same hours over again. This guide describes what healthy and unhealthy sharing look like, what each one costs or saves a project, and the practices that keep project knowledge findable. It serves everyone on a delivery team, newcomers included.

## Healthy vs. Unhealthy Knowledge Sharing

**Healthy knowledge sharing** keeps a project running and minimizes delivery risk. It covers general project areas — code, technology, client information — as well as individual expertise the team can use. Channels include team meetings, a shared knowledge base, chats, videos, and e-learning courses. Whatever the channel, sharing has to be mutually beneficial: everyone contributes, and everyone can rely on others in return.

**Unhealthy knowledge sharing** puts delivery at risk of delay or blockage. It becomes unhealthy when people hold knowledge and do not pass it on, fully or partially, which reads as disorganized or self-serving and erodes trust. Outdated or inaccurate material is the other form: it becomes a liability rather than an asset. Keeping sharing healthy is the whole team's responsibility, not only that of managers and leads.

## Risks and Benefits

| Area | Unhealthy Sharing | Healthy Sharing |
| --- | --- | --- |
| **Priorities** | Priorities blur, so people do unnecessary work or redo work the wrong way | The team stays on the current priorities and on schedule |
| **Standards** | Standards, processes, and conventions get disregarded, causing misunderstandings and lower quality | Documented practices and guidelines keep output consistent |
| **Information Access** | Answers live only in conversation or a disorganized knowledge base, so people wait on colleagues and still may not get them | Information is written down and easy to find, and everyone helps keep it current |
| **Bus Factor** | A bus factor of one: a single absence blocks progress | A bus factor above one: any single member can be away without disrupting delivery |
| **Onboarding** | Incomplete knowledge transfer makes onboarding long and confusing, so newcomers contribute little and lose motivation | Onboarding takes little effort from the newcomer or the existing team |

The **bus factor** is the number of people who must become unavailable before a system or process stalls — see [Growing and Keeping People](03-growing-and-keeping-people.md#core-concepts). At a bus factor of one, a single person holds knowledge nobody else has, and vacation, leave, or departure stops the work.

## Four Areas to Improve

### Software Development Life Cycle

- **Review artifacts with rotating peers** — change reviewers periodically so different people give feedback on different aspects of the solution. See [Code Review](../04-development-process/02-code-review.md).
- **Diversify task assignments** — keep more than one person familiar with each area instead of routing the same kind of task to the same person.
- **Keep notes as you work** — save useful findings while a task is open, and update the knowledge base when something important changes.
- **Plan time for documentation** — include documentation in task estimates so regular updates stay sustainable.

### Knowledge Base

Maintain a shared space (wiki, Confluence, or similar) that everyone can reach and everyone is responsible for keeping current. It should hold:

- The project goal and description
- The team structure and roles
- Links to project resources and environments
- Standards, rules, and conventions for every competency — managers, developers, QA, BAs, DevOps ([Coding Standards](../00-software-engineering/02-standards.md))
- The development process: branching, release process, and task life cycle ([Version Control](../04-development-process/01-version-control.md), [CI/CD](../04-development-process/03-ci-cd.md))

### Onboarding Procedures

- Maintain a **newcomer's guidebook** as the first reference for anyone joining the team, linking to project resources, the knowledge base, and environment setup instructions.
- Treat the guidebook as the whole team's responsibility so it stays current.
- **Assign a mentor** to every newcomer — one who stays available for questions and takes ownership of helping the new member settle in. See [Roles and the Employee Lifecycle](02-roles-and-lifecycle.md).

### Team Communication

- **Hold knowledge sharing sessions** on a regular schedule to communicate progress, discuss plans, and surface issues before they grow.
- **Keep team chats focused** — one topic per chat, with all the relevant people in it.
- **Post important updates in a dedicated channel**, tagging the people who must act so key information is not lost in daily traffic.
- **Join project townhalls**, where managers and architects share updates and deadlines and connect the team to the wider project vision.
- **Send meeting follow-ups** — the organizer shares outcomes with participants and other interested people, which also records what was agreed.

## Suggesting Improvements

Anyone, including newcomers, can and should suggest improvements to their team or manager.

**Raise a team discussion when you:**

- Have a new idea or find information worth sharing.
- Identify useful knowledge that exists only in verbal form.
- Discover important information missing from the project documentation.
- Find outdated pages or sections in the team's knowledge base.

**Reach out to your manager or mentor when you:**

- Cannot find important information about project status and updates.
- Experience a lack of efficient communication inside or outside your team.
- See development that better knowledge sharing would improve.
- Identify problems caused by unhealthy knowledge sharing.
- Find that the knowledge base is not being maintained.
