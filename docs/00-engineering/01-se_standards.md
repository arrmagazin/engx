---
type: Guide
title: Software engineering standards
description: Explains what software engineering standards are, the areas they cover, and the bodies that publish them.
tags: [standards, engineering, code-quality, best-practices]
---

# Software engineering standards 

**Software engineering standards **n are unified sets of rules, protocols, paradigms and best practices that dictate how software is developed, reviewed, deployed, and maintained. 

They serve as a foundational blueprint to ensure that systems are safe, reliable, secure, maintainable, and interoperable across different platforms. [1, 2, 3] 

Without standards, software development relies on tribal knowledge, leading to a chaotic codebase that is slow to update. Implementing standards reduces engineering onboarding time, eliminates configuration drift, and prevents minor bugs from causing massive cascading system failures. [1, 18, 19, 20] 


## Categories of Standards

Software engineering standards generally split into two categories:

* Product Standards: Rules applied directly to the artifact being built. Examples include Google's Style Guides for formatting, unified document structures, and specific file schemas. [4, 5, 6] 
* Process Standards: Frameworks defining the operational methodologies teams must follow. These encompass validation steps, specification workflows, and continuous deployment tracking. [5, 7] 

## Key Areas Covered by Standards

### 1. Code Quality & Maintenance

* Coding Conventions: Standardizing naming formats (e.g., camelCase vs snake_case) and file directory organization so any developer can seamlessly read the code.
* Design Principles: Enforcing concepts like SOLID (Single Responsibility, Open/Closed, etc.) to keep systems flexible and modular.
* Architecture Rules: Using predictable paradigms like [REST API standards](https://restfulapi.net/) and universal file formats like JSON. [8, 9, 10] 

### 2. Operations & DevOps

* Containerization: Following [Open Container Initiative (OCI)](https://opencontainers.org/) standards via tools like Docker to guarantee software runs identically across all environments.
* CI/CD Pipelines: Standardizing automated test coverage targets and roll-back workflows to safely deploy code in small batches.
* Semantic Versioning (SemVer): Utilizing standard major.minor.patch numbering to systematically communicate code updates. [10, 11, 12]

### 3. Security & Compliance

* Secure Coding: Adhering to standards like the [OWASP Top 10](https://owasp.org/www-project-top-ten/) to protect systems from vulnerabilities like SQL injection or broken access controls.
* Regulatory Compliance: Meeting legally binding data handling laws like HIPAA for medical data or GDPR for European privacy. [10, 13, 14, 15] 

## Major International Standards Bodies
While individual companies maintain custom guidelines, global interoperability relies on recognized organizations: [16, 17] 

| Organization | Key Software Standards | Purpose |
|---|---|---|
| ISO / IEC | ISO/IEC 12207[](https://www.iso.org/standard/77451.html) | Governs entire software lifecycle processes. |
| ISO / IEC | ISO/IEC 25010[](https://www.iso.org/standard/35733.html) | Evaluates software product quality metrics. |
| IEEE | IEEE 830 / ISO 29119 | Structures systems requirements and QA testing. |
| W3C | HTML5 / CSS3 / WCAG | Establishes web structure and accessibility rules. |

## References

[1] [https://www.cortex.io](https://www.cortex.io/post/software-development-standards-and-best-practices)
[2] [https://en.wikipedia.org](https://en.wikipedia.org/wiki/Software_standard)
[3] [https://www.parasoft.com](https://www.parasoft.com/learning-center/coding-standards/)
[4] [https://www.sapbwconsulting.com](https://www.sapbwconsulting.com/blog/software-engineering-standards)
[5] [https://www.youtube.com](https://www.youtube.com/watch?v=fClHH0PVI0k&t=120)
[6] [https://pubs.opengroup.org](https://pubs.opengroup.org/standards-guide/handbook-publications-development/latest/chap08-intro.html)
[7] [https://cs.ccsu.edu](https://cs.ccsu.edu/~stan/classes/CS530/Notes18/24-QualityManagement.html)
[8] [https://www.promovre.com](https://www.promovre.com/coding-standards-and-guidelines-in-software-engineering-explained/)
[9] [https://www.linkedin.com](https://www.linkedin.com/top-content/engineering/engineering-standards-and-compliance/engineering-standards-for-software-development/)
[10] [https://www.youtube.com](https://www.youtube.com/watch?v=fH0OfImhfFg)
[11] [https://www.opslevel.com](https://www.opslevel.com/resources/standards-in-software-development-and-9-best-practices)
[12] [https://roadie.io](https://roadie.io/blog/how-to-define-engineering-standards/)
[13] [https://www.geeksforgeeks.org](https://www.geeksforgeeks.org/software-engineering/software-engineering-classification-of-software-requirements/)
[14] [https://iborn.net](https://iborn.net/blog/the-importance-of-standards-in-software-engineering)
[15] [https://dev.to](https://dev.to/binoy123/beyond-functionality-mastering-non-functional-requirements-nfrs-for-software-success-34gk)
[16] [https://www.institutedata.com](https://www.institutedata.com/blog/standards-and-guidelines-in-software-engineering/)
[17] [https://www.reddit.com](https://www.reddit.com/r/civilengineering/comments/1rkqzs4/can_someone_explain_to_me_why_there_is_not_one/)
[18] [https://www.skmgp.com](https://www.skmgp.com/blog/software-engineering-and-design-key-models-and-standards)
[19] [https://www.appsierra.com](https://www.appsierra.com/blog/coding-standards-in-software-engineering)
[20] [https://axify.io](https://axify.io/blog/speed-vs-quality-software-development)
