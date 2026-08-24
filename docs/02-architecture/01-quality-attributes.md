---
type: Guide
title: Key Quality Attributes
description: Catalogs the design, runtime, system, and user quality attributes an architecture is evaluated against.
tags: [architecture, quality-attributes, system-design]
---

# Key Quality Attributes

Quality attributes are the properties an architecture is judged by once it does what it is supposed to do: how fast it responds, how well it holds up, how cheaply it can be changed. They are grouped here by where each one is observed — at design time, at runtime, in operation, and by the user. The concepts used to achieve them, such as storage models, distribution, caching, and containers, are covered in [System Design](../03-system-design/00-system-design.md).

## Design Qualities

| Quality | Description |
| --------- | ------------- |
| **Conceptual Integrity** | Consistency, simplicity, and coherence of the overall design, including component design, coding style, and naming |
| **Changeability** | Ability to undergo change with ease; includes maintainability for updates, debugging, and extensions |
| **Reusability** | Suitability for use in other applications and scenarios; minimizes duplication |

## Runtime Qualities

| Quality | Description |
| --------- | ------------- |
| **Scalability** | Ability to absorb load increases without losing performance, or to be enlarged readily (vertical vs. horizontal scaling, [load balancing](../03-system-design/01-concepts.md#load-balancing), database sharding) |
| **Performance** | Responsiveness measured in latency or throughput (caching, database indexing, asynchronous processing) |
| **Availability** | Proportion of time the system is functional; affected by errors, infrastructure problems, attacks, and load |
| **Reliability** | Ability to remain operational over time (fault tolerance, disaster recovery, data replication) |
| **[Security](../06-frontend/05-security-web.md)** | Capability to prevent malicious actions and protect assets (authentication, authorization, encryption, HTTPS, firewalls) |

## System Qualities

| Quality | Description |
| --------- | ------------- |
| **Interoperability** | Ability to operate successfully by communicating with other external systems |
| **Manageability** | Ease for administrators to run the system, through instrumentation for monitoring, debugging, and tuning |
| **Monitoring** | Logging, metrics, alerting, distributed tracing, and health checks |
| **Supportability** | Ability to surface the information needed to identify and resolve an issue |
| **Testability** | Ease of writing and running test criteria against the system |

## User Qualities

| Quality | Description |
| --------- | ------------- |
| **Usability** | Meeting user needs by being learnable and predictable in use |
| **i18n / L10n** | Internationalization — building so that language and region can vary — and localization, adapting to one of them |
| **[Accessibility](../06-frontend/04-accessibility-wcag.md)** | Usable by people with disabilities, including through assistive technology |
