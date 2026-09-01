---
type: Guide
title: Clouds
description: Routes to the AWS, Azure and Google Cloud handbooks: the service catalogs, the vocabulary, and the ground a cloud role is interviewed on.
tags: [aws, azure, gcp, cloud, devops, interview]
---

# Clouds

The three major clouds, one handbook each. All three are written to serve two kinds of reading. As **reference**, reach for one while a design is open and take only the section the decision needs — the service entries and concept tables are meant to be read out of order. As **rehearsal**, go through it end to end before an interview loop, because what is tested is whether you can say the answer out loud, not whether it looks familiar.

No handbook assumes prior experience with its cloud. Every term is explained the first time it appears.

---

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[AWS Handbook](01-aws.md)** | Foundations, compute, networking, storage and data, messaging and events, identity, and observability; then infrastructure as code, resilience, and the practices that keep a system running; then the diagrams and trade-offs to rehearse |
| **[Azure Handbook](02-azure.md)** | The same ground on Azure, plus immutable delivery and landing zones; ends with an AWS-to-Azure name map |
| **[GCP Handbook](03-gcp.md)** | The same ground on Google Cloud, where the resource hierarchy, the global VPC and Pub/Sub change the shape of the answers; ends with an AWS-to-Google-Cloud name map |

## Crossing Between Them

Two of the handbooks end with a service map written for a reader arriving from AWS: [AWS to Azure](02-azure.md#aws-to-azure-service-map) and [AWS to Google Cloud](03-gcp.md#aws-to-google-cloud-service-map). Each names the counterpart of an AWS service and — more usefully — where the analogy breaks down. They are the fastest route in from any direction.

Read them for the differences, not the similarities. Compute is compute everywhere; what varies is the boundary a permission is granted at, whether a network is regional or global, and what the billing unit is. Those three questions are where migrations and interview answers go wrong.
