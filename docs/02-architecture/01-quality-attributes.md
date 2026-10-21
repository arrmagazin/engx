---
type: Guide
title: Key Quality Attributes
description: Catalogs the design, runtime, system, and user quality attributes an architecture is evaluated against.
tags: [architecture, quality-attributes, system-design]
---

Quality attributes are the properties an architecture is judged by once it does what it should: how fast it responds, how well it holds up, how cheaply it can be changed. They are grouped by where each one is observed — at design time, at runtime, in operation, and by the user. The concepts used to achieve them, such as storage models, distribution, caching, and containers, are in [System Design](../03-system-design/index.md).

The four groups are adapted from the "Quality Attributes" chapter of Microsoft's [*Application Architecture Guide*](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ee658094%28v=pandp.10%29) (2nd ed., 2009). ISO/IEC 25010 defines a standard quality model of its own.

## Design Qualities

| Quality | Description |
| --------- | ------------- |
| **Conceptual Integrity** | The whole design follows one set of ideas, so components, naming, and coding style look as if one person chose them |
| **Changeability** | How cheaply the code can be fixed, extended, or adapted to a new requirement |
| **Reusability** | How readily a component can serve another product or use case without being copied and modified |

## Runtime Qualities

| Quality | Description |
| --------- | ------------- |
| **Scalability** | Load can grow while response times hold, by adding bigger machines or more of them (vertical vs. horizontal scaling, [load balancing](../03-system-design/06-client-server-communication.md#load-balancing), database sharding) |
| **Performance** | How fast the system answers and how much work it completes per second — latency and throughput (caching, database indexing, asynchronous processing) |
| **Availability** | The share of time users can reach a working system, usually stated as a percentage of uptime, such as 99.9% a month |
| **Reliability** | The system keeps producing correct results for long periods, even when one of its parts fails (fault tolerance, disaster recovery, data replication) |

## Security

Security keeps data and functions away from anyone not entitled to them, whether the threat is an attack or an accident (authentication, authorization, encryption, HTTPS, firewalls).

| Principle | Implementation |
| --- | --- |
| **Least Privilege** | Minimum permissions; scope tokens narrowly |
| **Defense in Depth** | Multiple layers: validation + sanitization + CSP |
| **Fail Secure** | Default to blocking access on error |
| **Input Validation** | Allowlist approach |
| **Secure by Default** | HTTPS, secure cookies out of the box |

See [Web Application Security](../06-frontend/07-security-web.md).

## System Qualities

| Quality | Description |
| --------- | ------------- |
| **Interoperability** | Exchanging data with systems that other parties build and run, through shared protocols and formats |
| **Manageability** | How easily operators can configure, observe, and tune the system while it runs |
| **Monitoring** | Logging, metrics, alerting, distributed tracing, and health checks |
| **Supportability** | When something goes wrong, the system gives support staff enough detail to find and fix the cause |
| **Testability** | How easily each part can be isolated, given controlled inputs, and checked against an expected result |

## User Qualities

| Quality | Description |
| --------- | ------------- |
| **Usability** | Users can learn the system without help and reach their goals quickly, with no surprises along the way |
| **i18n / L10n** | Internationalization — building so that language and region can vary — and localization, adapting to one of them |
| **[Accessibility](../06-frontend/06-accessibility-wcag.md)** | Usable by people with disabilities, including through assistive technology |
