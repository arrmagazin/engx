---
type: Guide
title: Key Quality Attributes
description: Catalogs design, runtime, system, and user quality attributes used to evaluate software architecture.
tags: [architecture, quality-attributes, system-design]
---

# Key Quality Attributes

#### Design Qualities

| Quality | Description |
| --------- | ------------- |
| **Conceptual Integrity** | Consistency, simplicity, and coherence of overall design including component design, coding style, and naming |
| **Changeability** | Ability to undergo changes with ease; includes maintainability for updates, debugging, and extensions |
| **Reusability** | Suitability for use in other applications and scenarios; minimizes duplication |

#### Runtime Qualities

| Quality | Description |
| --------- | ------------- |
| **Scalability** | Ability to handle load increases without performance impact, or to be readily enlarged (vertical vs. horizontal scaling, load balancing, database sharding) |
| **Performance** | Responsiveness measured in latency or throughput (caching, database indexing, asynchronous processing, optimizations) |
| **Availability** | Proportion of time the system is functional; affected by errors, infrastructure problems, attacks, and load |
| **Reliability** | Ability to remain operational over time (fault tolerance, high availability, disaster recovery, data replication) |
| **Security** | Capability to prevent malicious actions and protect assets (authentication, authorization, encryption, HTTPS, firewalls) |

#### System Qualities

| Quality | Description |
| --------- | ------------- |
| **Interoperability** | Ability to operate successfully by communicating with other external systems |
| **Manageability** | Ease for administrators to manage through instrumentation for monitoring, debugging, and tuning |
| **Monitoring** | Logging, metrics, alerting, distributed tracing, health checks |
| **Supportability** | Ability to provide information for identifying and resolving issues |
| **Testability** | Ease of creating and executing test criteria |

#### User Qualities

| Quality | Description |
| --------- | ------------- |
| **Usability** | Meeting user requirements by being intuitive, easy to localize/globalize |
| **L18N/I10N** | Internationalization and localization |
| **Accessibility** | Providing good access for disabled users |

## Fundamental System Design Concepts

| Area | Key Concepts |
| ------ | -------------- |
| **IT Infrastructure** | OS basics (processes, threads, concurrency, memory), Network protocols (TCP/IP, HTTP) |
| **Data Storage** | Codd Normalization, ACID, SQL vs. NoSQL, Object Storage, File Systems, Data Warehousing |
| **Distributed Systems** | Consensus, leader election, CAP theorem, Circuit Breaker |
| **Microservices** | SOA, API Gateway, Service Discovery, Saga pattern |
| **Cloud Services** | IaaS vs. PaaS vs. SaaS, Serverless, Containers (Docker, Kubernetes) |
| **Rendering** | SSR, SSG, ISR, CSR |
| **Event-Driven** | Event Sourcing, Pub/Sub |
| **Architecture Patterns** | Monolithic, Layered, Component-based, Microservice, Client-Server, MVC, RESTful, CQRS, Bulkhead |
