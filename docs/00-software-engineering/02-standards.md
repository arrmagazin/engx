---
type: Guide
title: Software Engineering Standards
description: Explains what software engineering standards are, the areas they cover, and the bodies that publish them.
tags: [standards, engineering, code-quality, best-practices]
---

# Software Engineering Standards

**Software engineering standards** are unified sets of rules, protocols, paradigms, and best practices that dictate how software is developed, reviewed, deployed, and maintained. They exist so that a system's safety, reliability, security, maintainability, and interoperability do not depend on which team happened to build it.

## Categories of Standards

* Product Standards: Rules applied directly to the artifact being built. Examples include Google's Style Guides for formatting, unified document structures, and specific file schemas.
* Process Standards: Frameworks defining the operational methodologies teams must follow. These encompass validation steps, specification workflows, and continuous deployment tracking.

## Key Areas Covered by Standards

### 1. Code Quality & Maintenance

* Coding Conventions: Standardizing naming formats (e.g., camelCase vs. snake_case) and file directory organization so any developer can read the code.
* Design Principles: Enforcing heuristics such as [SOLID](../05-coding/02-design-principles.md) to keep systems flexible and modular.
* Architecture Rules: Using established conventions such as [REST](../06-frontend/03-client-server-communication.md) and interchange formats such as JSON.

### 2. Operations & DevOps

* Containerization: Following [Open Container Initiative (OCI)](https://opencontainers.org/) specifications so that an image built by one tool runs on any compliant runtime.
* [CI/CD](../04-development-process/03-ci-cd.md) Pipelines: Standardizing automated test coverage targets and roll-back workflows to deploy code in small batches.
* Semantic Versioning (SemVer): Using `major.minor.patch` numbering to communicate what kind of change a release contains.

### 3. Security & Compliance

* Secure Coding: Adhering to references such as the [OWASP Top 10](https://owasp.org/www-project-top-ten/) to protect systems from vulnerabilities such as SQL injection or broken access control.
* Regulatory Compliance: Meeting legally binding data handling laws, such as HIPAA for health data in the United States or GDPR for personal data in the EU.

## Major International Standards Bodies

| Organization | Key Software Standards | Purpose |
|---|---|---|
| **ISO / IEC / IEEE** | [ISO/IEC/IEEE 12207](https://www.iso.org/standard/77451.html) | Governs the processes of the whole software lifecycle |
| **ISO / IEC** | ISO/IEC 25010 | Defines the product quality model that software is evaluated against |
| **ISO / IEC / IEEE** | ISO/IEC/IEEE 29148, ISO/IEC/IEEE 29119 | Structures requirements specification and software testing; 29148 superseded the withdrawn IEEE 830 |
| **W3C** | CSS, WCAG, ARIA | Establishes web styling and accessibility rules |
