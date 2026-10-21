---
type: Guide
title: Clouds
description: One concept at a time across AWS, Azure and Google Cloud: what each calls it, where the analogy breaks, what changes a design.
tags: [aws, azure, gcp, cloud, devops, interview]
---

Three clouds, one chapter, organized by the problem rather than by the vendor. Only that arrangement keeps the interesting part visible: compute is compute everywhere; what varies is the boundary a permission is granted at, whether a network is regional or global, and what the billing unit is. Read it for the differences, not the similarities.

The chapter assumes no prior experience with any of the three. Every term is explained where it first appears, and no claim depends on knowing one cloud before reading about another.

Vendor facts are as of October 2026. Cloud services change often, so check a fact against the vendor's own documentation before a design depends on it.

---

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Concepts Across the Clouds](01-concept-map.md)** | The main tables, one per concept group, first half — accounts, geography, the control plane, compute, networking, identity. Each names the concept in all three clouds and where the analogy stops holding |
| **[Data and Operations Across the Clouds](02-data-and-operations.md)** | The second half of the tables — storage and data, messaging, encryption, observability, delivery, resilience — and four habits that keep a cross-cloud claim safe |
| **[Service Names Across the Clouds](03-service-names.md)** | The lookup: AWS service to its Azure and Google Cloud counterparts, grouped like the concepts, with the difference that matters in each row |
| **[Cross-Cloud Trade-Offs](04-trade-offs.md)** | The five structural differences that change a design rather than a name, plus the four decisions that are the same on every cloud under different product names |

## How to Use It

Three readings for three purposes:

- **Orientation.** You know one cloud and need the other two. Start with [Service Names](03-service-names.md) and read the last column: the mapping is the cheap half, the note is the useful half.
- **Design review.** A decision is open. Go to [Cross-Cloud Trade-Offs](04-trade-offs.md) and ask its five questions of the design:
  - Which wall is it relying on?
  - Is the network one object or one per region?
  - Is the guardrail on an action or on a configuration?
  - What does the billing meter count?
  - Is the resilience a property or a topology?
- **Rehearsal.** An interview loop is coming. Read [Concepts Across the Clouds](01-concept-map.md) and [Data and Operations Across the Clouds](02-data-and-operations.md) end to end: the test is whether you can say the comparison out loud, not whether it looks familiar. The four recurring decisions at the end of the trade-offs page are the ones most often asked.
