---
type: Guide
title: Azure DevOps/Infrastructure Engineer — Prep Guide
description: Study checklist covering Azure core services, networking, storage, identity, and DevOps competency areas for interviews.
tags: [interview, azure, cloud, devops]
---

# Azure DevOps/Infrastructure Engineer — Prep Guide

A study map organized around the five competency areas from the job description. Use this as a checklist: for each bullet, be ready to explain the concept, name the relevant Azure service, and describe a scenario where you used or would use it.

## 1. Azure Core Concepts

The service reference lives in [the Azure stack overview](01-azure-stack-overview.md). This section covers only what an interview asks on top of it.

- **Walk the hierarchy out loud**: Management Group → Subscription → Resource Group → Resource, naming the level each policy assignment, role assignment, and budget belongs at
- **Subscription vs. resource group**: the subscription is the billing, quota, and hard isolation boundary; the resource group is a lifecycle and RBAC-scoping container inside it
- **Azure RBAC vs. Entra ID roles**: Azure RBAC governs resources, Entra ID directory roles govern the directory itself, and they are separate assignment systems
- **Governance as code**: Azure Policy for guardrails, Template Specs plus deployment stacks for packaged deployments (Azure Blueprints is deprecated), landing zones for the pre-built starting point, and tags for cost allocation and automation targeting
- **Regions, availability zones, and region pairs**: which of the three answers a resilience question and which answers a disaster-recovery question
- **Managed identity vs. service principal**: system-assigned vs. user-assigned identities, and OIDC workload identity federation for CI/CD in place of long-lived secrets

## 2. Implementing and Maintaining Intricate Azure Infrastructure

### Infrastructure as Code (IaC) Options
| Tool | Native/OSS | Notes |
|---|---|---|
| **ARM templates** | Native | JSON, verbose, still underlies everything |
| **Bicep** | Native (Microsoft) | DSL that transpiles to ARM JSON; what-if deployments, modules |
| **Terraform (azurerm/azapi providers)** | OSS (HashiCorp) | Multi-cloud, state management, most common in hybrid orgs |
| **Pulumi** | OSS | IaC with general-purpose languages |
| **Ansible (azure.azcollection)** | OSS | Config management + light provisioning |

Be ready to discuss:
- **State management**: Terraform remote state in Azure Storage with state locking (blob lease)
- **Modules**: Bicep modules vs. Terraform modules — reuse, versioning, and private registries
- **Drift detection**: `terraform plan`, Azure Policy compliance scans, and Bicep what-if
- **Idempotency**: why declarative tools converge safely on repeated runs
- **Multi-environment strategy**: workspaces or parameter files per environment (dev/test/prod), and naming conventions

### Maintaining Infrastructure at Scale
- **Landing zone architecture** (Cloud Adoption Framework / Enterprise-Scale)
- **Hub-spoke networking topology**
- **Subscription vending** for multi-team orgs
- **Backup & DR**: Azure Backup, Site Recovery, and RTO/RPO planning
- **Patch management**: Update Manager (Azure Automation), and image-based patching for an immutable approach

## 3. Automating Infrastructure Changes and Configuration Management

### CI/CD for Infrastructure
- **Azure DevOps Pipelines** vs. **GitHub Actions**: YAML pipelines, environments, and approvals/gates
- **Pipeline patterns**: plan → manual approval → apply (Terraform); validate → what-if → deploy (Bicep)
- **Service connections**: workload identity federation (OIDC) vs. service principal secrets
- **GitOps**: Flux/Argo CD with AKS, config as the source of truth — see [CI/CD](../04-development-process/03-ci-cd.md)

### Configuration Management
- **Azure Machine Configuration**: the successor to PowerShell DSC and Azure Automation DSC, and the name to use for new guest-configuration work
- **Azure Automation runbooks** (PowerShell/Python) for scheduled and event-driven operational tasks
- **Ansible** for post-provision config (packages, files, and services) on VMs
- **Custom Script Extension / cloud-init** for VM bootstrap
- **Azure Policy "DeployIfNotExists" / "Modify" effects** — auto-remediation as a form of continuous config enforcement

### Secrets & Config
- **Azure Key Vault**: secrets, keys, and certificates; access via managed identity; Key Vault references in App Service/Functions
- **App Configuration service**: feature flags, centralized settings, and dynamic refresh

### Testing Infrastructure Code
- **Terratest**, **Pester** (for ARM/Bicep + PowerShell), and linting (`tflint`, `bicep lint`, and checkov/tfsec for policy-as-code scanning)

## 4. Immutable Infrastructure and Cloud-Native Frameworks

### Immutable Infrastructure Concepts
- **Golden images**: Azure Image Builder, Packer — bake config into the image rather than mutating running servers
- **VMSS with rolling upgrades**: replace instances instead of patching in place
- **Blue/green and canary deployments**: deployment slots (App Service), traffic splitting (Front Door/App Gateway/AKS with Argo Rollouts or Flagger)
- **Immutable containers**: image tags pinned by digest, no in-place modification of running containers

### Cloud-Native / CNCF-Aligned Practices
- **Containerization**: Docker fundamentals, multi-stage builds, and image scanning (Trivy, Defender for Containers) — see [Containers](../03-system-design/04-containers.md)
- **Kubernetes on Azure (AKS)**:
  - Deployments, StatefulSets, DaemonSets, Services, and Ingress (AGIC — Application Gateway Ingress Controller)
  - Helm charts for packaging
  - HPA/VPA/Cluster Autoscaler
  - Entra Workload ID (workload identity federation) for Azure resource access from pods — AAD Pod Identity was retired in September 2024
  - Networking modes: Azure CNI Overlay is the recommendation for new clusters, and kubenet is legacy with a retirement announced
  - Network policies (Azure Network Policy Manager, Calico, or Cilium)
- **Service mesh basics**: traffic management and mTLS, via the Istio-based AKS service mesh add-on — the Open Service Mesh add-on is retired and the project is archived by CNCF
- **Dapr** (Distributed Application Runtime) — increasingly relevant with Azure Container Apps
- **12-factor app principles** as the philosophy underlying cloud-native automation
- **KEDA** (Kubernetes Event-Driven Autoscaling) — Microsoft co-developed, common on AKS

### Automated Infrastructure Delivery Pipeline
1. Code (Bicep/Terraform) in Git
2. PR triggers validation + plan/what-if
3. Approval gate
4. Apply/deploy via pipeline using federated identity
5. Post-deploy: automated smoke tests, policy compliance scan
6. GitOps sync for app-layer changes on AKS

## 5. Performance, Cost Management, and Security Best Practices

### Performance Optimization
- **Right-sizing**: VM SKU selection, AKS node pool sizing, and autoscale thresholds
- **Caching layers**: Front Door caching for new edge work, Azure Cache for Redis for application data — Azure CDN from Edgio was retired on 15 January 2025, and Azure CDN Standard from Microsoft has a separate, later announced retirement date
- **Database tuning**: DTU vs. vCore models, query performance insights, and read replicas
- **Application Insights** profiling, and load testing (**Azure Load Testing** service)
- **Availability Zones + zone-redundant SKUs** for resilience without heavy overhead

### Cost Management
- **Azure Cost Management + Billing**: budgets, alerts, and cost analysis by tag/resource group
- **Reserved Instances / Savings Plans** vs. pay-as-you-go vs. Spot VMs (for interruptible workloads — a good fit with immutable/stateless design)
- **Autoscaling to match demand** (scale-to-zero where possible — Container Apps, Functions consumption)
- **Right-sizing and orphaned resource cleanup** (unattached disks, idle public IPs)
- **Azure Advisor cost recommendations**
- **Tagging strategy** for chargeback/showback

### Security Best Practices
- **Zero Trust principles**: least privilege via RBAC, no standing secrets (managed identity + workload identity federation)
- **Microsoft Defender for Cloud**: Secure Score, CSPM, and container/VM/DB threat protection
- **Network segmentation**: NSGs, Azure Firewall, and private endpoints to avoid public exposure of PaaS services
- **Key Vault** for all secrets/certs; automatic rotation where supported
- **Encryption**: at rest (platform-managed vs. customer-managed keys), in transit (TLS everywhere)
- **Azure Policy** for guardrails (deny public IP creation, enforce HTTPS, and require specific SKUs)
- **Supply chain security**: image scanning, SBOM, signed commits/artifacts, and dependency scanning in pipelines
- **Audit & compliance**: Activity Log, diagnostic settings piped to Log Analytics/SIEM (Sentinel), and the regulatory compliance dashboard

## Behavioral Stories (STAR)

Interviewers for this role mix conceptual questions with "tell me about a time you...". Prepare 2–3 stories per competency area. Reuse the same project across areas — one substantial migration can supply four different stories depending on which angle you emphasize.

### The Format

| Part | What Goes Here | Time |
|---|---|---|
| **Situation** | Context, scale, and constraints, with the numbers | ~15s |
| **Task** | What *you* specifically owned | ~10s |
| **Action** | Decisions and trade-offs rather than a task list, and the bulk of the answer | ~60s |
| **Result** | Measured outcome plus what you would do differently | ~20s |

Two rules that separate a strong story from a weak one:
- **"We" is a red flag.** Say "I" for your decisions, "we" only for team context.
- **Quantify the Result.** "Deploys went from 4 hours to 12 minutes" beats "deploys got much faster."

### Worked Example — Area 3 (Automation)

Every figure below is a placeholder: substitute your own fleet sizes, timings, and outcomes, and keep the shape of the answer.

> **S:** "We had 60-odd VMs across three environments, all configured by hand. Environments had drifted so far apart that a release passing in test would fail in prod maybe one time in three."
>
> **T:** "I owned bringing config under version control without a big-bang rewrite — the team had releases to ship."
>
> **A:** "I started with an audit rather than code: ran Ansible in check mode against prod to get a factual inventory of what was actually installed versus what we thought. That surfaced 14 undocumented packages. I codified the *current* prod state first, so day one had zero behavioral change and no risk — then converged test and dev up to it. I chose Ansible over DSC because a third of the fleet was Linux and the team already knew YAML from the pipelines. Roles went into a private Git repo with tagged versions so environments could adopt changes on their own schedule."
>
> **R:** "Environment-drift incidents went to zero over the next two quarters, and rebuilding a box dropped from a half-day of tribal knowledge to a 20-minute playbook run. In hindsight I'd have pushed for immutable images sooner — we kept patching mutable VMs for a year longer than we needed to."

Note what that does: names a **decision with an alternative rejected and a reason** (Ansible over DSC, because mixed OS + existing skills), shows **risk management** (codify current state first), and closes with **honest hindsight** — which reads as senior, not as weakness.

### Worked Example — Area 5 (Cost)

The figures here are placeholders too: replace the growth rate, the split, and the saving with your own before you use this in an interview.

> **S:** "Azure spend was growing ~8% month over month while traffic was flat. Nobody could attribute it — one subscription, no tags."
>
> **T:** "I was asked to find the cause and stop the growth without degrading service."
>
> **A:** "First I made cost *visible*: enforced a tagging policy via Azure Policy with a `Deny` effect on new resources, then a remediation task for existing ones. Cost analysis by tag showed non-prod was 40% of spend and ran 24/7. I moved dev/test to auto-shutdown schedules and swapped the batch pool to Spot VMs — safe because those jobs were already idempotent and checkpointed. Separately, orphaned disks and idle public IPs from old experiments were costing us every month with nothing running on them, so I added a weekly Advisor-driven cleanup report. I deliberately did *not* touch prod SKUs first even though they were the biggest line item, because right-sizing prod without load-test evidence is how you cause an incident."
>
> **R:** "About 31% reduction in monthly spend within two billing cycles, with no change to prod latency. The tagging policy is the part that lasted — it means the next person can answer 'why did this go up' in ten minutes."

### Story Bank by Area

| Area | Likely Prompts | The Story to Prepare |
|---|---|---|
| **1. Azure core** | "Walk me through how you'd structure subscriptions for a new business unit" | A governance, RBAC, or landing-zone decision |
| **2. Infrastructure** | "Tell me about the most complex environment you've built" | Hub-spoke, networking, or a migration |
| **3. Automation** | "Describe a manual process you automated" | IaC adoption, a pipeline build, or config management |
| **4. Immutable/cloud-native** | "Tell me about a deployment that went wrong" | A rollback, blue/green, or containerization effort |
| **5. Perf/cost/security** | "How have you handled a security or cost problem?" | Cost reduction, incident response, or secret elimination |

Also prepare the two that always come up regardless of role: **a failure you caused** (own it, show the systemic fix — not "I worked too hard") and **a disagreement with a colleague** (show you changed your mind on evidence, or escalated cleanly).

## Diagrams You Should Be Able to Sketch

Expect "can you draw how that would look?" on a whiteboard or shared doc. Practice these until you can draw each in ~3 minutes while talking. **Narrate the order you draw in** — it demonstrates how you decompose a problem.

### Landing Zone / Hub-Spoke

Draw order: management groups top-down → hub → spokes → the connections last.

```
              ┌──────────────── Tenant Root MG ────────────────┐
              │                                                │
        ┌─────┴─────┐    ┌───────────┐    ┌───────────┐  ┌─────┴─────┐
        │ Platform  │    │ Landing   │    │  Sandbox  │  │Decommiss- │
        │    MG     │    │ Zones MG  │    │    MG     │  │  ioned MG │
        └─────┬─────┘    └─────┬─────┘    └───────────┘  └───────────┘
              │                │
     ┌────────┼────────┐   ┌───┴────┬─────────┐
  Identity Management Connectivity │         │
    sub      sub        sub      Corp     Online
                         │        sub       sub
                         │         │         │
                    ┌────▼─────────▼─────────▼────┐
                    │      HUB VNet (Connectivity) │
                    │  ┌────────┐  ┌────────────┐  │
                    │  │ Azure  │  │ VPN / ER   │  │──── on-prem
                    │  │Firewall│  │  Gateway   │  │
                    │  └────────┘  └────────────┘  │
                    │  ┌────────┐  ┌────────────┐  │
                    │  │ Bastion│  │Private DNS │  │
                    │  └────────┘  └────────────┘  │
                    └───┬──────────────────┬───────┘
                 peering│                  │peering
                 ┌──────▼──────┐    ┌──────▼──────┐
                 │ SPOKE: Prod │    │ SPOKE: NonPd│
                 │ ┌─────────┐ │    │ ┌─────────┐ │
                 │ │ AKS /   │ │    │ │ AKS /   │ │
                 │ │ App Svc │ │    │ │ App Svc │ │
                 │ └────┬────┘ │    │ └─────────┘ │
                 │ ┌────▼────┐ │    └─────────────┘
                 │ │ Private │ │
                 │ │Endpoints│──────► SQL / Storage / Key Vault
                 │ └─────────┘ │      (no public access)
                 └─────────────┘
```

Points to make **while** drawing:
- Spokes peer to the hub, **never to each other** — east-west traffic is forced through the firewall via UDR (`0.0.0.0/0` → firewall private IP).
- Private DNS zones live in the hub and are linked to every spoke VNet — otherwise private endpoint name resolution silently breaks.
- Policy is assigned at the **management group** level so new subscriptions inherit guardrails on creation. This is the answer to "how does this scale to 50 teams?"
- Mention **subscription vending** as the automation that makes new spokes repeatable.

### CI/CD for IaC

Draw order: left-to-right, PR path on top, main path on the bottom.

```
   ┌──────────┐
   │ Feature  │
   │  branch  │
   └────┬─────┘
        │ open PR
        ▼
   ┏━━━━━━━━━━━━━━━━━━━━━━━ PR VALIDATION ━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃  fmt/lint ──► validate ──► tfsec/checkov ──► plan / what-if  ┃
   ┃  (tflint)     (bicep       (policy-as-      (posted as a     ┃
   ┃               build)        code scan)       PR comment)     ┃
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                    │ human review + merge
                                    ▼
   ┏━━━━━━━━━━━━━━━━━━━━━━━━ MAIN PIPELINE ━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃                                                              ┃
   ┃   DEV ──────► TEST ──────► [ APPROVAL GATE ] ──────► PROD     ┃
   ┃  auto        auto           (env protection)       manual    ┃
   ┃    │           │                                      │      ┃
   ┃    └───────────┴──── same modules, different ─────────┘      ┃
   ┃                        *.tfvars / .bicepparam               ┃
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                    ▼
                    ┌───────────────────────────────┐
                    │  POST-DEPLOY                  │
                    │  • smoke tests                │
                    │  • Azure Policy compliance    │
                    │  • drift detection (nightly   │
                    │    plan → alert if non-empty) │
                    └───────────────────────────────┘

   AUTH:  Pipeline ──OIDC federated credential──► Entra ID workload identity
          (NO secrets stored in the pipeline — this is the bit to say out loud)

   STATE: Terraform remote state in Storage Account
          + blob lease locking + separate state file per env
```

Points to make while drawing:
- **Plan artifact promotion**: apply the *saved plan file* from the PR, not a fresh plan at apply time — otherwise you're approving something you didn't review.
- **Blast radius**: separate state per environment, so a corrupted dev state can't touch prod.
- **Drift detection** is the bullet most candidates forget — a nightly plan that alerts on a non-empty diff is what proves IaC is the source of truth.

### Also Worth Being Able to Draw
- **AKS request path**: Front Door → App Gateway (AGIC) → Ingress → Service → Pods, with Entra Workload ID pointing off to Key Vault/SQL.
- **Immutable pipeline**: source → Packer/Image Builder → Azure Compute Gallery (versioned, replicated) → VMSS rolling upgrade.
- **Blue/green**: two slots or backends behind one traffic switch, with the swap and the rollback arrow drawn explicitly.

## Trade-Offs — The "It Depends on X" Answers

Definitions get you a pass; trade-offs get you the offer. The pattern:

> **"It depends on three things: [A], [B], [C]. If [A], I'd pick X — because [reason]. Where I'd flip to Y is [specific condition]."**

Never answer "which is better?" without naming the deciding variable. Also be willing to say "we chose X and it was the wrong call, here's what we learned."

### Bicep vs. Terraform

**It depends on:** whether you're Azure-only, what the org already runs, and how fast you need day-0 support for new services.

| Aspect | Bicep | Terraform |
|---|---|---|
| **Scope** | Azure only | Multi-cloud, plus Entra ID, GitHub, Datadog, and other providers |
| **State** | None — ARM *is* the state | Explicit state file (power **and** liability) |
| **New Azure features** | Day 0, via ARM | Provider lag; `azapi` covers the gap |
| **Preview/dry-run** | `what-if` (approximate) | `plan` (precise, from state) |
| **Deletes** | Doesn't remove out-of-band resources unless in Complete mode | Tracks and destroys what it created |
| **Ecosystem** | Azure Verified Modules, growing | Large module registry, mature |
| **Cost/support** | Free, Microsoft-supported | OSS core; the BUSL license change matters to some orgs → OpenTofu |

**Sample answer:** *"If the estate is Azure-only and the team lives in the portal and PowerShell, Bicep — no state file to corrupt, day-0 support for new resource types, and it's supported by the same vendor as the platform. I flip to Terraform the moment there's a second provider in play, and there usually is: Entra ID app registrations, GitHub repos, and DNS at an external registrar. That's not multi-cloud, but it's multi-provider, and Bicep can't reach it. The real cost of Terraform is that state becomes a production asset — it needs remote storage, locking, backup, and an access model of its own. If a team isn't ready to own that, Bicep is the safer choice."*

### AKS vs. Container Apps

**It depends on:** whether you need the Kubernetes API surface, your team's operational maturity, and your scale-to-zero requirements.

| Aspect | Container Apps | AKS |
|---|---|---|
| **You manage** | Containers only | Cluster, node pools, upgrades, and patching |
| **Scale to zero** | Yes, built in | No (nodes cost money at idle) |
| **Built in** | KEDA, Dapr, and Envoy | You install them |
| **Extensibility** | No CRDs, no DaemonSets, no custom controllers | Full ecosystem |
| **Networking** | Simplified | Network policies, CNI modes, full control |
| **Ops burden** | Low | Real — needs a named owner |

**Sample answer:** *"Default to Container Apps. It's KEDA, Dapr, and Envoy already wired together, and it scales to zero, which matters for spiky or non-prod workloads. I move to AKS when I hit something Container Apps structurally can't do — CRDs and operators, DaemonSets for a node-level agent, network policies for tenant isolation, or a service mesh. The honest deciding question is usually organizational, not technical: does someone own cluster upgrades? AKS gives roughly 12 months of community support per Kubernetes minor version, extended to two years by Long-Term Support on the Premium tier, so an unowned cluster falls off a supported version on a clock you don't control. If nobody owns upgrades, Container Apps is the right call even where AKS would technically fit."*

### Machine Configuration vs. Ansible

**It depends on:** OS mix, whether your VMs are mutable at all, and push vs. pull.

| Aspect | Machine Configuration | Ansible |
|---|---|---|
| **Model** | Pull, agent-based, **continuously** re-asserts | Push, agentless (SSH/WinRM), point-in-time |
| **Drift** | Auto-corrects and reports compliance to Azure Policy | Only fixes when you run it |
| **OS strength** | Windows-first (Linux supported) | Strong on both |
| **Reach** | Works anywhere the agent runs, including Arc-connected on-prem | Needs a network path from a control node |
| **Best at** | Enforcing a steady state | Orchestrating ordered, multi-host sequences |

Azure Machine Configuration is the successor to PowerShell DSC and Azure Automation DSC; use that name for anything new.

**Sample answer:** *"Machine Configuration when the goal is 'this baseline must never drift' — it's pull-based, it re-asserts on a schedule, and compliance lands in Azure Policy next to everything else, so auditors get one dashboard. Ansible when the work is orchestration rather than enforcement: sequenced steps across multiple hosts, mixed OS, or anything with ordering between machines. They aren't competing — I've run both, Machine Configuration holding the security baseline and Ansible doing app deployment on top. But the answer I'd push for is neither: if you're configuring VMs at boot, ask why the image doesn't already have it. Bake it with Image Builder and the drift problem stops existing. Config management is what you keep for the cases you can't bake."*

### Other Pairs Worth a Rehearsed Answer

| Pair | The Deciding Variable |
|---|---|
| **Azure DevOps vs. GitHub Actions** | Where the code already lives; ADO's release gates and approvals are still richer, while GitHub Actions has the bigger ecosystem |
| **Service endpoint vs. private endpoint** | Do you need a private IP in your VNet and on-prem reachability? → private endpoint (costs more, needs DNS) |
| **VMSS vs. AKS** | Are you running containers, or an app that needs identical instances? |
| **Managed identity vs. service principal** | Is the workload running *in* Azure? → managed identity. External CI → service principal with OIDC federation, never a secret |
| **Azure Firewall vs. NSG** | NSG gives free L4 rules per subnet or NIC; Firewall adds FQDN filtering, threat intel, and central logging, and bills a fixed hourly deployment charge plus a per-GB data-processing charge |
| **Reserved instance vs. Spot** | Is the workload steady-state (RI) or interruptible and checkpointed (Spot)? |
| **Hub-spoke vs. Virtual WAN** | Number of regions and branch sites; vWAN is managed transit at the cost of control |
| **Blue/green vs. canary** | Can you tolerate two full environments (cost), or do you need a metric-driven gradual rollout? |

### Three Phrases That Read as Senior

- *"I'd want to know X before answering"* — then answer both branches. Better than guessing.
- *"We chose X and it was wrong, because we underestimated Y."* — one of these, ready to go.
- *"The technical answer is X, but the organizational answer is Y."* — shows you've operated the thing, not just built it.

## Final Prep Checklist

- [ ] 10 STAR stories written out — 2 per competency area, with numbers in the Result
- [ ] Failure story and disagreement story prepared
- [ ] Can sketch hub-spoke and IaC CI/CD in 3 minutes each, talking while drawing
- [ ] Can give the three trade-off answers above without notes
- [ ] 3–4 questions ready for them (their IaC tool and why; who owns cluster upgrades; how they handle prod access; what broke most recently)
