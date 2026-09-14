---
type: Guide
title: Clouds
description: One concept at a time across AWS, Azure and Google Cloud: what each calls it, where the analogy breaks, what changes a design.
tags: [aws, azure, gcp, cloud, devops, interview]
---

Three clouds, one chapter. It is organized by the problem rather than by the vendor, because that is the only arrangement in which the interesting part survives: compute is compute everywhere, and what varies is the boundary a permission is granted at, whether a network is regional or global, and what the billing unit is.

This chapter assumes no prior experience with any of the three. Every term is explained the first time it appears, and no claim depends on knowing one cloud before reading about another.

Read it for the differences, not the similarities.

---

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Concepts Across the Clouds](01-concept-map.md)** | The main table set: one section per concept group — accounts, geography, the control plane, compute, networking, storage and data, messaging, identity, encryption, observability, delivery, resilience — naming each concept's incarnation in all three clouds and where the analogy stops holding |
| **[Service Names Across the Clouds](02-service-names.md)** | The lookup: AWS service to Azure and Google Cloud counterpart, grouped the way the concepts are grouped, with the difference that matters in each row |
| **[Cross-Cloud Trade-Offs](03-trade-offs.md)** | The five structural differences that change a design rather than a name, plus the four decisions that are the same on every cloud under different product names |

## How to Use It

Three readings serve three purposes.

- **Orientation.** You know one cloud and need the other two. Start with [Service Names](02-service-names.md), then read the notes column — the mapping is the cheap half, the note is the useful half.
- **Design review.** A decision is open. Go to [Cross-Cloud Trade-Offs](03-trade-offs.md) and ask its five questions of the design: which wall is it relying on, is the network one object or one per region, is the guardrail an action or a configuration, what does the billing meter count, and is the resilience a property or a topology.
- **Rehearsal.** An interview loop is coming. Read [Concepts Across the Clouds](01-concept-map.md) end to end, because what is tested is whether you can say the comparison out loud, not whether it looks familiar. The four recurring decisions at the end of the trade-offs page are the ones most often asked.
