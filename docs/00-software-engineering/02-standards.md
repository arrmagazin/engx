---
type: Guide
title: Software Engineering Standards
description: Explains what software engineering standards are, the areas they cover, and the bodies that publish them.
tags: [standards, engineering, code-quality, best-practices]
---

## Categories of Standards

| Category | Governs | Examples |
| --- | --- | --- |
| **Product standards** | The artifact being built | Google's Style Guides for formatting, unified document structures, specific file schemas |
| **Process standards** | The methods teams must follow | Validation steps, specification workflows, continuous deployment tracking |

## Key Areas Covered by Standards

### 1. Code Quality & Maintenance

| Standard | What it sets |
| --- | --- |
| **Coding conventions** | Naming formats (e.g., camelCase vs. snake_case) and directory layout, so any developer can read the code |
| **Design principles** | Heuristics such as [SOLID](../05-coding/04-design-principles.md) that keep systems flexible and modular |
| **Architecture rules** | Established conventions such as [REST](../03-system-design/06-client-server-communication.md) and interchange formats such as JSON |

### 2. Operations & DevOps

| Standard | What it sets |
| --- | --- |
| **Containerization** | [Open Container Initiative (OCI)](https://opencontainers.org/) specifications, so an image built by one tool runs on any compliant runtime |
| **[CI/CD](../04-development-process/03-ci-cd.md) pipelines** | Automated test coverage targets and roll-back workflows, to deploy code in small batches |
| **Semantic Versioning (SemVer)** | `major.minor.patch` numbers that tell what kind of change a release contains |

### 3. Security & Compliance

| Standard | What it sets |
| --- | --- |
| **Secure coding** | References such as the [OWASP Top 10](https://owasp.org/www-project-top-ten/), to protect against vulnerabilities such as SQL injection or broken access control |
| **Regulatory compliance** | Legally binding data-handling laws, such as HIPAA for health data held by US covered entities (health plans, health care clearinghouses, and certain providers) and their business associates, or GDPR for personal data in the EU |

Which laws apply depends on the organization and where it operates; involve legal counsel to confirm.

## Major International Standards Bodies

| Organization | Key Software Standards | Purpose |
| --- | --- | --- |
| **ISO / IEC / IEEE** | [ISO/IEC/IEEE 12207](https://www.iso.org/standard/77451.html) | Governs the processes of the whole software lifecycle |
| **ISO / IEC** | ISO/IEC 25010 | Defines the product quality model that software is evaluated against |
| **ISO / IEC / IEEE** | ISO/IEC/IEEE 29148, ISO/IEC/IEEE 29119 | Structures requirements specification and software testing; 29148 superseded the withdrawn IEEE 830 |
| **W3C** | CSS, WCAG, ARIA | Establishes web styling and accessibility rules |
