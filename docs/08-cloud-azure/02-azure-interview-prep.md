---
type: Guide
title: Azure Interview Prep
description: Study checklist covering Azure core services, networking, storage, identity, and DevOps competency areas for interviews.
tags: [interview, azure, cloud, devops]
---

# Azure Interview Prep

A study map organized around the five competency areas that recur in Azure infrastructure job descriptions. Use this as a checklist: for each bullet, be ready to explain the concept, name the relevant Azure service, and describe a scenario where you used or would use it.

## 1. Azure Core Concepts

The service reference lives in [the Azure stack overview](01-azure-stack-overview.md). This guide covers only what an interview asks on top of it.

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
- **Containerization**: Docker fundamentals, multi-stage builds, and image scanning (Trivy, Defender for Containers) — see [Containers](../03-system-design/05-containers.md)
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
- **Caching layers**: Front Door caching for new edge work, Azure Cache for Redis for application data — Azure CDN from Edgio was announced for retirement on 15 January 2025, with service reportedly extended for some customers past that date, so check the Microsoft retirement notice before assuming a given profile is gone; Azure CDN Standard from Microsoft has a separate, later announced retirement date
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

Story structure, the two rules for telling one, and the two stories asked in every loop whatever the cloud are in [Interview Technique](../11-interview/01-technique.md). Everything below is particular to Azure.

### Worked Example — Area 3 (Automation)

Every figure below is a placeholder: substitute your own resource counts, timings, and outcomes, and keep the shape of the answer.

> **S:** "Three environments, about 200 resources, all built in the portal over two years and described by nothing but a wiki page. Deployments ran from an Azure DevOps variable group holding one service principal secret that was Owner on every subscription and had not been rotated since the pipeline was written."
>
> **T:** "I owned getting the estate into code and getting that standing secret out of the pipeline, without freezing delivery while I did it."
>
> **A:** "I didn't start by writing Bicep. I exported the existing resource groups to ARM templates and ran `what-if` against them until the diff came back empty, which told me what the portal had actually created rather than what the wiki claimed — six resources nobody could name an owner for, and two NSG rules that existed only in prod. Then I rewrote that as Bicep modules, one per resource group, and adopted environments into the code one at a time instead of in a single pass. I chose Bicep over Terraform deliberately: the estate was Azure-only, the team already read ARM JSON in the portal, and I didn't want to hand people with no prior state-file experience a Terraform backend to operate on top of a new language. Separately I replaced the variable-group secret with workload identity federation on the service connection, scoped per environment, and cut the identity from Owner down to Contributor plus an explicit User Access Administrator assignment only where role assignments were genuinely needed. Those two changes went in as separate pull requests so a rollback of one couldn't block the other."
>
> **R:** "Within two quarters every environment deployed from `main`, the drift that had made prod special was either codified or deleted, and there was no secret left in the pipeline to rotate or leak. What I'd do differently is turn on the Azure Policy `DeployIfNotExists` for diagnostic settings in month one rather than month four — half the resources I adopted had never emitted a log anywhere, and I only found that out at the point I needed the logs."

Note what that does: it names a **decision with an alternative rejected and a reason** (Bicep over Terraform, because the estate was Azure-only and nobody was ready to own state), shows **risk management** (reconcile with `what-if` before writing a line; keep the two changes in separate PRs), and closes with **honest hindsight** — which reads as senior, not as weakness.

### Worked Example — Area 5 (Cost)

The figures here are placeholders too: replace the spend, the split, and the saving with your own before you use this in an interview.

> **S:** "One subscription, and about 40% of the monthly bill sat on resources with no owner tag at all. Finance had asked twice which team owned which half of the spend and nobody could answer, so the bill had never really been questioned."
>
> **T:** "I was asked to cut the run-rate without a migration and without resizing production on guesswork."
>
> **A:** "I went after attribution before savings: a Cost Management export into a Log Analytics workspace, plus an Azure Resource Graph query listing every resource missing the owner and environment tags. Two weeks of asking the teams who recognised the resource names got the untagged share under 5%, and only then did I look at what to cut — in a deliberate order. Azure Hybrid Benefit turned out to be switched off across the whole Windows fleet, which was the single largest line and a licence-entitlement conversation with procurement rather than an engineering change; I mention it first because engineers rarely look there first. Then three App Service Plans were each running one app at P2v3, so consolidating them onto one plan was two hours of work. Then an Azure Firewall sat in the non-prod hub billing its fixed hourly charge around the clock for workloads that ran office hours. I held reservations back until the resizing had settled, because a reservation bought against a SKU you're about to change stops being a saving and becomes a stranded commitment."
>
> **R:** "About 28% off the monthly run-rate over two billing cycles, with no production change at all. The durable part is the tagging: budgets are scoped per team now and the alert goes to that team rather than to me. In hindsight I'd have checked Hybrid Benefit in week one — I spent a month in infrastructure detail while the biggest lever was a licensing setting."

### Story Bank by Area

| Area | Likely Prompts | The Story to Prepare |
|---|---|---|
| **1. Azure core** | "Walk me through how you'd structure subscriptions for a new business unit" | A governance, RBAC, or landing-zone decision |
| **2. Infrastructure** | "Tell me about the most complex environment you've built" | Hub-spoke, networking, or a migration |
| **3. Automation** | "Describe a manual process you automated" | IaC adoption, a pipeline build, or config management |
| **4. Immutable/cloud-native** | "Tell me about a deployment that went wrong" | A rollback, blue/green, or containerization effort |
| **5. Perf/cost/security** | "How have you handled a security or cost problem?" | Cost reduction, incident response, or secret elimination |

## Diagrams You Should Be Able to Sketch

How to practice a sketch and narrate it while drawing is in [Interview Technique](../11-interview/01-technique.md). The diagrams themselves are Azure-specific.

### Landing Zone / Hub-Spoke

Draw order: management groups top-down → hub → spokes → the connections last.

```text
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

```text
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

The shape of a good trade-off answer, and the phrases that carry one, are in [Interview Technique](../11-interview/01-technique.md). These are the Azure pairs to have ready.

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
| **Scale to zero** | Yes, built in | User node pools can; the **System** pool cannot, so a cluster always costs something at idle |
| **Built in** | KEDA, Dapr, and Envoy | You install them |
| **Extensibility** | No CRDs, no DaemonSets, no custom controllers | Full ecosystem |
| **Networking** | Simplified | Network policies, CNI modes, full control |
| **Ops burden** | Low | Real — needs a named owner |

**Sample answer:** *"Default to Container Apps. It's KEDA, Dapr, and Envoy already wired together, and it scales to zero, which matters for spiky or non-prod workloads. I move to AKS when I hit something Container Apps structurally can't do — CRDs and operators, DaemonSets for a node-level agent, network policies for tenant isolation, or a service mesh. The honest deciding question is usually organizational, not technical: does someone own cluster upgrades? Last time I checked the AKS version support policy — and Microsoft has moved these windows before, so I'd re-read it — a Kubernetes minor version got roughly 12 months of community support, then a further year of *platform* support where Azure keeps supporting the cluster but upstream Kubernetes fixes are no longer backported, with Long-Term Support on the Premium tier stretching the whole thing to two years. That middle window is the one people forget: the cluster is still supported, and it is quietly no longer getting Kubernetes patches. Either way an unowned cluster falls off a supported version on a clock you don't control. If nobody owns upgrades, Container Apps is the right call even where AKS would technically fit."*

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
| **Azure DevOps vs. GitHub Actions** | Where the code already lives; ADO ships more built-in gate types out of the box (query work items, invoke a REST endpoint, wait on an Azure Monitor alert) while GitHub Actions has the bigger ecosystem — both are actively developed, so re-check the gap rather than quoting it |
| **Service endpoint vs. private endpoint** | Do you need a private IP in your VNet and on-prem reachability? → private endpoint (costs more, needs DNS) |
| **VMSS vs. AKS** | Are you running containers, or an app that needs identical instances? |
| **Managed identity vs. service principal** | Is the workload running *in* Azure? → managed identity. External CI → service principal with OIDC federation, never a secret |
| **Azure Firewall vs. NSG** | NSG gives free L4 rules per subnet or NIC; Firewall adds FQDN filtering, threat intel, and central logging, and bills a fixed hourly deployment charge plus a per-GB data-processing charge |
| **Reserved instance vs. Spot** | Is the workload steady-state (RI) or interruptible and checkpointed (Spot)? |
| **Hub-spoke vs. Virtual WAN** | Number of regions and branch sites; vWAN is managed transit at the cost of control |
| **Blue/green vs. canary** | Can you tolerate two full environments (cost), or do you need a metric-driven gradual rollout? |

## Final Prep Checklist

The cloud-independent items are in [Interview Technique](../11-interview/01-technique.md). The Azure-specific ones:

- [ ] Can walk the management group → subscription → resource group → resource hierarchy out loud, naming what belongs at each level
- [ ] Can explain Azure RBAC vs. Entra ID directory roles as two separate assignment systems
