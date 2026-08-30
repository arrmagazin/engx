---
type: Guide
title: AWS Interview Prep
description: Study checklist covering AWS core services, networking, storage, identity, and DevOps competency areas for interviews.
tags: [interview, aws, cloud, devops]
---

# AWS Interview Prep

A study map organized around the five competency areas that recur in AWS infrastructure job descriptions. For each bullet, be ready to explain the concept, name the relevant AWS service, and describe a scenario where you used or would use it.

## 1. AWS Core Concepts

### Fundamentals

- **Account hierarchy**: AWS Organizations → OUs → Accounts → Resources. The *account* is the billing, quota, and hard isolation boundary. Its Azure counterpart is the subscription, not the resource group — see [the Azure stack overview](../08-cloud-azure/01-azure-stack-overview.md)
- **Control plane**: everything goes through public service APIs (Console, CLI, SDKs, CloudFormation, and Terraform all call the same APIs). There is no single "resource manager" layer — each service has its own API and its own eventual consistency behavior
- **Regions, Availability Zones (AZs), Local Zones, and edge locations**: how AWS models fault domains; AZ letters are *per account* (your `us-east-1a` is not my `us-east-1a` — use AZ IDs when it matters)
- **IAM**: identity-based vs. resource-based policies, policy evaluation logic (explicit deny > allow > implicit deny), SCPs as guardrails not grants
- **Service Control Policies (SCPs), Resource Control Policies, AWS Config, and Control Tower**: governance-as-code, enforcing regions, tagging, and allowed services
- **Tags**: cost allocation tags (must be activated in Billing), automation targeting, and ABAC (attribute-based access control)

## 2. Implementing and Maintaining Intricate AWS Infrastructure

### Infrastructure as Code (IaC) Options

| Tool | Native/OSS | Notes |
| --- | --- | --- |
| **CloudFormation** | Native | YAML/JSON, stacks + change sets, StackSets for multi-account/region; drift detection built in |
| **AWS CDK** | Native | TypeScript/Python/etc. that *synthesizes* CloudFormation; constructs and aspects for reuse |
| **Terraform (aws provider)** | OSS (HashiCorp) | Multi-cloud, explicit state, common in mixed estates |
| **Pulumi** | OSS | IaC in general-purpose languages, own state backend |
| **SAM / Serverless Framework** | Native / OSS | Opinionated shorthand for Lambda-centric stacks |
| **Ansible (`amazon.aws`)** | OSS | Config management + light provisioning |

- **State management**: Terraform remote state in S3 with locking — a DynamoDB lock table is still supported, and S3-native locking arrived as the opt-in `use_lockfile` in Terraform 1.10 (November 2024)
- **Modules**: CDK constructs vs. Terraform modules — reuse, versioning, private registries, and when a shared module becomes a bottleneck
- **Drift detection**: `terraform plan`, CloudFormation drift detection, and AWS Config rules
- **Idempotency**: why declarative tools converge safely on repeated runs — and where AWS APIs make that hard (eventual consistency, non-updatable properties forcing replacement). See [system design concepts](../03-system-design/01-concepts.md)
- **Multi-environment strategy**: **account-per-environment** is the AWS-idiomatic answer, not one account with tags

### Maintaining Infrastructure at Scale

- **Landing zone architecture**: AWS Control Tower, Landing Zone Accelerator, and the multi-account strategy from the Well-Architected Framework
- **Network topology**: Transit Gateway hub-and-spoke, centralized egress, and inspection VPCs
- **Account vending**: Control Tower Account Factory / AFT (Account Factory for Terraform) for multi-team orgs
- **Backup and DR**: AWS Backup (org-wide backup policies), pilot light vs. warm standby vs. multi-site, and RTO/RPO planning
- **Patch management**: SSM Patch Manager for mutable fleets; image-based patching (EC2 Image Builder) for the immutable approach
- **Quotas and limits**: Service Quotas, and which limit binds first — in network-dense designs (many ENIs per task or pod, many attached VPCs), ENI, Elastic IP, and VPC CIDR quotas are reached before compute quotas

## 3. Automating Infrastructure Changes and Configuration Management

### CI/CD for Infrastructure

- **GitHub Actions / GitLab CI** vs. native **CodePipeline + CodeBuild** (and CodeCatalyst): where the code already lives usually decides it. See [CI/CD](../04-development-process/03-ci-cd.md)
- **Pipeline patterns**: plan → manual approval → apply (Terraform); `cdk diff` / change set → review → execute (CloudFormation/CDK)
- **Credentials**: **OIDC federation to an IAM role** — never store access keys in CI
- **GitOps**: Flux/Argo CD on EKS, config as the source of truth
- **Multi-account deploys**: a pipeline in a tooling account assuming a deployment role in each target account

### Configuration Management

- **Systems Manager**: State Manager (associations = continuous enforcement), Run Command, Automation runbooks, and Session Manager (shell access without SSH — removes the need for bastion hosts)
- **Ansible** for post-provision config on EC2, especially mixed-OS or ordered multi-host sequences
- **user-data / cloud-init** for bootstrap; **AWS Config remediation actions** for auto-correcting non-compliant resources
- **EventBridge → Lambda** as the general-purpose "react to an infrastructure event" pattern

### Secrets & Config

- **Secrets Manager** (rotation built in, priced per secret) vs. **SSM Parameter Store** (SecureString, free standard tier, no native rotation)
- Injecting secrets: ECS task definition `secrets` block, Lambda extensions, and External Secrets Operator on EKS
- Never bake secrets into AMIs or container images

### Testing Infrastructure Code

- **Terratest**, **cfn-lint**, **CDK assertions / snapshot tests**, and `checkov` / `tfsec` / `cfn-nag` for policy-as-code scanning
- **Open Policy Agent / Conftest** or CloudFormation **Guard** for org-specific rules in the pipeline

## 4. Immutable Infrastructure and Cloud-Native Frameworks

### Immutable Infrastructure Concepts

- **Golden AMIs**: EC2 Image Builder or Packer — bake config into the image rather than mutating running servers
- **ASG instance refresh / rolling replacement**: replace instances instead of patching in place; ASG lifecycle hooks for graceful drain
- **Blue/green and canary**: **CodeDeploy** (ECS/Lambda/EC2 blue-green), ALB weighted target groups, Lambda alias traffic shifting, and Argo Rollouts or Flagger on EKS
- **Immutable containers**: pin images by digest not tag, set ECR immutable tags, and keep `latest` out of production. See [containers](../03-system-design/05-containers.md)

### Cloud-Native / CNCF-Aligned Practices

- **Containerization**: Docker fundamentals, multi-stage builds, distroless base images, and scanning (ECR enhanced scanning via Inspector, Trivy)
- **Kubernetes on EKS**:
  - Deployments, StatefulSets, DaemonSets, Services, and Ingress (AWS Load Balancer Controller)
  - Helm for packaging
  - HPA / **Karpenter** (AWS-originated, now CNCF) vs. Cluster Autoscaler
  - **IRSA / EKS Pod Identity** for AWS API access from pods — the container-native alternative to node roles
  - Network policies, and VPC CNI prefix delegation for IP density
- **Service mesh basics**: Istio/Linkerd concepts (traffic management, mTLS)
- **KEDA** for event-driven autoscaling (scaling on SQS depth, for example)
- **12-factor app principles** as the philosophy underlying cloud-native automation
- **Serverless-first thinking**: Lambda + EventBridge + Step Functions as an architecture, not just glue

## 5. Performance, Cost Management, and Security Best Practices

### Performance Optimization

- **Right-sizing**: instance family selection (including Graviton) and Compute Optimizer recommendations
- **Caching layers**: CloudFront, ElastiCache, and DAX for DynamoDB. See [system design concepts](../03-system-design/01-concepts.md)
- **Database tuning**: Aurora read replicas, RDS Proxy for connection storms (especially with Lambda), and Performance Insights
- **Storage performance**: gp3 IOPS/throughput tuning, and S3 request patterns and prefix parallelism
- **Load testing** and **X-Ray**/ADOT tracing to find the actual bottleneck before resizing anything

### Cost Management

- **Cost Explorer, AWS Budgets, Cost Anomaly Detection**, and CUR (Cost and Usage Report) into Athena/QuickSight for real analysis
- **Savings Plans (Compute vs. EC2 Instance) vs. Reserved Instances vs. Spot** — Compute Savings Plans are the flexible default; Spot for interruptible, checkpointed workloads
- **Scale to zero** where possible: Lambda, Fargate scale-in, and non-prod shutdown schedules via EventBridge
- **The line items people miss**: idle NAT Gateways and their data processing charges, unattached EBS volumes and old snapshots, unassociated EIPs, cross-AZ data transfer, and CloudWatch Logs retention set to "never expire"
- **Graviton migration** and **S3 Intelligent-Tiering** as low-risk structural changes
- **Cost allocation tags + AWS Organizations consolidated billing** for chargeback/showback

### Security Best Practices

- **Least privilege**: no IAM users, roles only, and Identity Center for humans; use IAM Access Analyzer to find unused permissions and external access
- **SCPs as guardrails**: deny leaving the org, deny disabling CloudTrail, and restrict regions — guardrails that no admin in a member account can override
- **GuardDuty** (threat detection), **Security Hub** (findings aggregation and standards), **Inspector** (vulnerability scanning), and **Macie** (sensitive data in S3)
- **Network segmentation**: private subnets by default, VPC endpoints so traffic to S3/ECR never hits the internet, and SGs referencing SGs
- **Encryption**: KMS CMKs with key policies, S3 default encryption, and TLS enforced via bucket policy `aws:SecureTransport`. Automatic key rotation has been configurable from 90 to 2,560 days since 2024, where the period used to be fixed at the 365-day default
- **Secrets**: Secrets Manager with rotation; never in environment variables checked into Git
- **Supply chain security**: image scanning, SBOM, signed artifacts, and dependency scanning in pipelines
- **Audit and compliance**: organization CloudTrail to a locked-down log archive account, Config aggregator, and Security Hub standards (CIS, AWS FSBP)

## Behavioral Stories (STAR)

The STAR format itself, the two rules that separate a strong story from a weak one, and the stories every loop asks for whatever the cloud are in [Interview Technique](../11-interview/01-technique.md). What follows is the AWS-specific half.

### Worked Example — Area 3 (Automation)

Every figure below is a placeholder. Keep the shape of the answer and substitute the numbers from your own project.

> **S:** "We had about 70 EC2 instances across three environments, all configured by hand, and every one reachable by SSH with a shared key that had been in the team password manager for two years. Environments had drifted far enough apart that a release passing in staging failed in prod roughly one time in three."
>
> **T:** "I owned bringing configuration under version control and removing the standing SSH access — without a big-bang rewrite, because the team had releases to ship."
>
> **A:** "I started with an audit rather than code: ran Ansible in check mode against prod to get a factual inventory of what was actually installed versus what we believed. That surfaced 14 undocumented packages. I codified the *current* prod state first, so day one had zero behavioral change and no risk, then converged staging and dev up to it. I chose Ansible over SSM State Manager at that point because a third of the fleet was Windows and the ordering between hosts mattered for the app's startup sequence. Separately I rolled out SSM Session Manager and deleted the shared key — that was a two-week change on its own and I deliberately kept it off the critical path of the config work so a rollback of one couldn't block the other."
>
> **R:** "Environment-drift incidents went to zero over the next two quarters, rebuilding a box dropped from a half-day of tribal knowledge to a 20-minute playbook run, and we passed the SSH finding in the next security review. In hindsight I'd have pushed for golden AMIs sooner — we kept patching mutable instances for a year longer than we needed to."

Note what that does: it names a **decision with an alternative rejected and a reason** (Ansible over State Manager, because mixed OS plus ordering), shows **risk management** (codify current state first; decouple the two changes), and closes with **honest hindsight**.

### Worked Example — Area 5 (Cost)

The figures here are placeholders too. Substitute your own spend, savings, and timelines.

> **S:** "AWS spend was growing about 8% month over month while traffic was flat. Nobody could attribute it — one account, no cost allocation tags activated."
>
> **T:** "I was asked to find the cause and stop the growth without degrading service."
>
> **A:** "First I made cost *visible*: turned on the Cost and Usage Report into Athena, because Cost Explorer alone wasn't granular enough to see data-transfer charges by resource. Two problems showed up immediately. Non-prod was 40% of spend and ran 24/7, so I put dev and staging on EventBridge shutdown schedules and moved the batch fleet to Spot — safe because those jobs were already idempotent and checkpointed. The bigger surprise was NAT Gateway data processing at about $3k a month: every ECR pull and S3 read from private subnets was routing through NAT. I added gateway and interface VPC endpoints, which is a few hours of Terraform. I deliberately did *not* right-size prod instances first even though they were the biggest line item, because resizing prod without load-test evidence is how you cause an incident — I queued that behind a Compute Optimizer review and a Graviton pilot on one stateless service."
>
> **R:** "About 34% reduction in monthly spend within two billing cycles, with no change to prod latency. The part that lasted is the tagging policy enforced by SCP plus the CUR dashboard — it means the next person can answer 'why did this go up' in ten minutes instead of a week."

### Story Bank — Map Yours to the Areas

| Area | Likely Prompt | The Story to Prepare |
| --- | --- | --- |
| **1. AWS core** | "Walk me through how you'd structure accounts for a new business unit" | A multi-account, IAM, or landing-zone decision |
| **2. Infrastructure** | "Tell me about the most complex environment you've built" | Transit Gateway, a VPC redesign, or a migration |
| **3. Automation** | "Describe a manual process you automated" | IaC adoption, a pipeline build, or configuration management |
| **4. Immutable and cloud-native** | "Tell me about a deployment that went wrong" | A rollback, blue/green, or containerization effort |
| **5. Performance, cost, and security** | "How have you handled a security or cost problem?" | Cost reduction, incident response, or key elimination |

## Diagrams You Should Be Able to Sketch

Rehearsal and narration technique are in [Interview Technique](../11-interview/01-technique.md); these are the AWS diagrams worth being able to draw cold.

### Multi-Account Landing Zone + Transit Gateway Hub-Spoke

Draw order: org and OUs top-down → the network account and TGW → workload VPCs → the routes last.

```text
        ┌──────────────────── AWS Organization (Management acct) ────────────────────┐
        │   SCPs applied at OU level ─ billing ─ Control Tower                        │
        └───┬───────────────────┬────────────────────┬──────────────────┬────────────┘
            │                   │                    │                  │
     ┌──────▼──────┐     ┌──────▼──────┐      ┌──────▼──────┐    ┌──────▼──────┐
     │ Security OU │     │Infrastructure│     │ Workloads OU│    │  Sandbox OU │
     ├─────────────┤     │      OU      │     ├─────────────┤    ├─────────────┤
     │ Log Archive │     ├──────────────┤     │  Prod acct  │    │  per-dev    │
     │ Audit/SecHub│     │Network  Shared│    │ NonProd acct│    │  accounts   │
     └─────────────┘     │ acct   Svcs   │    └──────┬──────┘    └─────────────┘
                         └───┬───────────┘           │
                             │                       │
                    ┌────────▼───────────────────────▼────────┐
                    │        TRANSIT GATEWAY (Network acct)   │
                    │   shared to org via AWS RAM             │
                    │   separate route tables per segment     │
                    └──┬──────────────┬───────────────┬───────┘
                       │              │               │
          ┌────────────▼───┐  ┌───────▼────────┐  ┌───▼──────────────┐
          │ INSPECTION VPC │  │  EGRESS VPC    │  │  ON-PREM         │
          │ Network Fw /   │  │  NAT GW (AZ-a) │  │  DX + VPN backup │
          │ GWLB appliance │  │  NAT GW (AZ-b) │  └──────────────────┘
          └────────────────┘  └───────┬────────┘
                                      │ 0.0.0.0/0
        ┌─────────────────────────────┴──────────────────────────────┐
        │                                                            │
  ┌─────▼───────────────────┐                        ┌───────────────▼─────────┐
  │ PROD VPC (Prod acct)    │                        │ NONPROD VPC             │
  │ ┌────────┐  ┌────────┐  │                        │  (same modules,         │
  │ │public  │  │public  │  │ ALB across 2+ AZs      │   smaller sizes)        │
  │ └───┬────┘  └───┬────┘  │                        └─────────────────────────┘
  │ ┌───▼────┐  ┌───▼────┐  │
  │ │private │  │private │  │ EKS nodes / ECS tasks
  │ └───┬────┘  └───┬────┘  │
  │ ┌───▼────┐  ┌───▼────┐  │
  │ │  data  │  │  data  │  │ RDS Multi-AZ, no route to IGW
  │ └────────┘  └────────┘  │
  │   VPC endpoints ────────┼──► S3 / ECR / SSM / Secrets Mgr
  │   (no NAT for AWS APIs) │     (traffic never leaves the VPC)
  └─────────────────────────┘
```

Points to make **while** drawing:

- **The account is the blast radius.** Prod and non-prod are separate accounts, not separate tags in one account — that's the answer to "how do you stop a dev mistake taking prod down?"
- Spoke VPCs attach to the TGW, **never peer to each other** — east-west goes through the TGW route tables, and through the inspection VPC where the compliance regime requires it.
- **Centralized egress**: one NAT Gateway pair in the egress VPC instead of a pair per VPC. NAT gateways bill per hour and per GB processed, so a pair in every VPC is an avoidable cost.
- **VPC endpoints bypass NAT entirely** for S3/ECR/SSM. This is both a cost and a security point.
- SCPs are attached at the **OU** so new accounts inherit guardrails at creation. Mention **Account Factory / AFT** as the automation that makes new accounts repeatable.

### CI/CD for IaC (Multi-Account)

Draw order: left-to-right, PR path on top, main path on the bottom, auth arrows last.

```text
   ┌──────────┐
   │ Feature  │
   │  branch  │
   └────┬─────┘
        │ open PR
        ▼
   ┏━━━━━━━━━━━━━━━━━━━━━━━ PR VALIDATION ━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃  fmt/lint ──► validate ──► checkov/tfsec ──► plan / cdk diff ┃
   ┃  (tflint,     (terraform   (policy-as-       (posted as a    ┃
   ┃   cfn-lint)    validate)    code scan)        PR comment)    ┃
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                    │ human review + merge
                                    ▼
   ┏━━━━━━━━━━━━━━━━━━━━━━━━ MAIN PIPELINE ━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃                                                              ┃
   ┃   DEV acct ────► STAGING acct ──► [ APPROVAL ] ──► PROD acct  ┃
   ┃    auto            auto           (environment)     manual    ┃
   ┃      │               │             protection)         │      ┃
   ┃      └───────────────┴──── same modules, different ─────┘     ┃
   ┃                            *.tfvars / CDK context            ┃
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                    ▼
                    ┌───────────────────────────────┐
                    │  POST-DEPLOY                  │
                    │  • smoke tests                │
                    │  • AWS Config compliance      │
                    │  • drift detection (nightly   │
                    │    plan → alert if non-empty) │
                    └───────────────────────────────┘

   AUTH:  GitHub Actions ──OIDC──► IAM role (tooling acct)
                                      │ sts:AssumeRole
                                      ▼
                          per-env deployment role in each target account
          (NO access keys anywhere)

   STATE: Terraform state in S3, one bucket/key per env
          + S3 conditional-write locking (use_lockfile) + versioning + KMS
```

Points to make while drawing:

- **Plan artifact promotion**: apply the *saved plan file* from the PR, not a fresh plan at apply time — otherwise you're approving something you didn't review.
- **Blast radius**: separate state *and separate account* per environment, so a corrupted dev state can't reach prod.
- **Trust policy conditions**: the OIDC role's trust policy must pin `sub` to the specific repo *and branch/environment*. A trust policy with `repo:org/*:*` is a finding.
- **Drift detection**: a nightly plan that alerts on a non-empty diff is what proves IaC is the source of truth.

### Also Worth Being Able to Draw

- **EKS request path**: Route 53 → CloudFront → ALB (Load Balancer Controller) → Ingress → Service → Pods, with IRSA arrows out to Secrets Manager/RDS.
- **Immutable pipeline**: source → Packer/EC2 Image Builder → AMI (versioned, shared across accounts via RAM) → launch template version bump → ASG instance refresh.
- **Blue/green on ECS**: CodeDeploy shifting an ALB listener between two target groups, with the rollback alarm drawn explicitly.
- **Event-driven serverless**: API Gateway → Lambda → EventBridge → Step Functions, with SQS DLQs on every async hop.

## Trade-Offs — The "It Depends on X" Answers

[Interview Technique](../11-interview/01-technique.md) covers the answer pattern and the phrasing that carries it. The pairs below are the AWS ones to have rehearsed.

### CloudFormation/CDK vs. Terraform

**It depends on:** whether you're AWS-only, what the org already runs, and whether the team wants a general-purpose language or a config language.

| Aspect | CloudFormation / CDK | Terraform |
| --- | --- | --- |
| **Scope** | AWS only | Multi-cloud, plus GitHub, Datadog, Okta, and Cloudflare |
| **State** | Managed by the service — no state file to lose | Explicit state file (power **and** liability) |
| **New AWS features** | Usually fast, but *not* always day 0 | Provider lag; sometimes ahead of CloudFormation, and `awscc` covers the gap |
| **Preview/dry-run** | Change sets, `cdk diff` | `plan` (precise, from state) |
| **Failure mode** | Automatic rollback — good, until a stack is `UPDATE_ROLLBACK_FAILED` | Partial apply; you re-run and converge |
| **Multi-account** | StackSets, natively org-aware | Per-account state plus assume-role providers |
| **Abstraction** | CDK gives you real code (loops, types, unit tests) | HCL: deliberately limited, more predictable to read |
| **Cost/support** | Free, AWS-supported | OSS core; the BUSL license change matters to some orgs → OpenTofu |

**Sample answer:** *"If the estate is AWS-only and the team is application engineers who'd rather write TypeScript than HCL, CDK — the constructs give real reuse, you can unit-test your infrastructure, and there's no state file to corrupt or back up. I flip to Terraform the moment there's a second provider in play, and there usually is: GitHub repos, Okta apps, DNS at an external registrar, Datadog monitors. That's not multi-cloud, it's multi-provider, and CDK can't reach it. The real cost of Terraform is that state becomes a production asset — remote storage, locking, backup, and an access model of its own, because state files contain secrets in plaintext. The real cost of CloudFormation is the day a production stack lands in UPDATE_ROLLBACK_FAILED at 2am and you have to repair a stack whose internals you don't control. I'd pick based on which of those two failures the team is better equipped to handle."*

### ECS Fargate vs. EKS

**It depends on:** whether you need the Kubernetes API surface, your team's operational maturity, and whether portability is a real requirement or an aspiration.

| Aspect | ECS on Fargate | EKS |
| --- | --- | --- |
| **You manage** | Task definitions only | Cluster add-ons, node lifecycle, and version upgrades |
| **Control plane cost** | None | A per-cluster hourly charge, plus nodes |
| **Upgrade cadence** | AWS handles it | Roughly quarterly Kubernetes versions; as of 2025, 14 months of standard support per version and then 12 months of extended support at a higher price. AWS has already revised those windows once, so read the EKS Kubernetes version lifecycle page before you plan an upgrade calendar around them |
| **Ecosystem** | AWS-native only | Full CNCF: operators, CRDs, Helm, and service mesh |
| **IAM integration** | Task roles — simple and clean | IRSA / Pod Identity — more moving parts |
| **Portability** | Locked to AWS | Manifests move; the surrounding glue mostly does not |
| **Ops burden** | Low | Real — needs a named owner |

**Sample answer:** *"Default to ECS on Fargate. Task roles, ALB integration, and CloudWatch are already wired together, there are no nodes to patch, and a small team can run it without a platform engineer. I move to EKS when I hit something ECS structurally can't do — operators and CRDs, DaemonSets for node-level agents, a service mesh, or a team that already has years of Kubernetes experience and a library of Helm charts. The honest deciding question is usually organizational, not technical: does someone own cluster upgrades? Last time I checked the EKS version lifecycle page — and those numbers have moved before, so I'd check it again — each Kubernetes version got 14 months of standard support and then 12 months of extended support at a higher price, so a cluster with no named owner drifts into paying for support it never planned for. If nobody owns upgrades, ECS is the right call even where EKS would technically fit. And I'd push back on 'we need Kubernetes for portability' — the manifests port; the IAM, the load balancer controller, and the storage classes don't."*

### SSM State Manager vs. Ansible

**It depends on:** OS mix, whether your instances are mutable at all, and push vs. pull.

| Aspect | SSM State Manager | Ansible |
| --- | --- | --- |
| **Model** | Pull, agent-based, **continuously** re-asserts on a schedule | Push, agentless (SSH/WinRM), point-in-time |
| **Drift** | Auto-corrects; compliance reported to SSM/Config | Only fixes when you run it |
| **Reach** | Anything with the SSM agent, including on-prem via hybrid activations | Needs a network path from a control node |
| **Access model** | IAM — no inbound ports, no SSH keys | Requires SSH/WinRM credentials and reachability |
| **Best at** | Enforcing a steady state, fleet-wide, with no bastion | Orchestrating ordered, multi-host sequences |

**Sample answer:** *"State Manager when the goal is 'this baseline must never drift' — it's pull-based, it re-asserts on a schedule, it needs no inbound network path, and compliance lands next to everything else in Config, so auditors get one dashboard. Ansible when the work is orchestration rather than enforcement: ordered steps across multiple hosts, anything with a dependency between machines. They're not really competing — I've run both, State Manager holding the security baseline and Ansible doing app deployment on top. But the answer I'd actually push for is neither: if you're configuring instances at boot, ask why the AMI doesn't already have it. Bake it with Image Builder, replace instances instead of patching them, and the drift problem stops existing. Config management is what you keep for the cases you genuinely can't bake."*

### Other Pairs Worth a Rehearsed Answer

| Pair | The Deciding Variable |
| --- | --- |
| **Security Group vs. NACL** | Stateful per-resource (SG, the default tool) vs. stateless per-subnet (NACL, coarse deny for CIDR blocks) |
| **VPC Peering vs. Transit Gateway** | Number of VPCs — peering is non-transitive and O(n²); TGW past roughly 5–10 VPCs, at a per-attachment and per-GB cost |
| **NAT Gateway vs. VPC endpoints** | Is the destination an AWS service? → endpoint (cheaper, private); NAT only for genuine internet egress |
| **Multi-AZ vs. read replica (RDS)** | Availability (synchronous standby, automatic failover, not readable) vs. read scaling (asynchronous, lag) |
| **Secrets Manager vs. Parameter Store** | Do you need automatic rotation and cross-account sharing? → Secrets Manager, which is priced per secret |
| **Savings Plan vs. Spot** | Steady-state baseline (SP) vs. interruptible and checkpointed (Spot); most fleets want both |
| **Lambda vs. Fargate** | Request duration, concurrency shape, and whether 15 minutes is a ceiling you'll hit |
| **IAM user vs. role** | There is no case for a new IAM user; use roles, Identity Center, and OIDC |
| **ALB vs. NLB** | L7 routing, WAF, and OIDC auth (ALB) vs. static IPs, extreme throughput, and non-HTTP protocols (NLB) |
| **DynamoDB vs. RDS** | Do you know your access patterns up front and need single-digit-ms reads at any scale? → DynamoDB |
| **Control Tower vs. roll-your-own org** | Speed and guardrails out of the box vs. full control; Control Tower is opinionated and hard to un-adopt |

## Final Prep Checklist

The items that hold whatever the cloud are in [Interview Technique](../11-interview/01-technique.md). The AWS-specific ones:

- [ ] Can explain IAM policy evaluation (explicit deny → SCP → allow → implicit deny) cleanly
- [ ] Know your own worst AWS bill line item story and what you did about it
- [ ] Have the AWS-specific questions ready for them: how many accounts and why, and who owns EKS cluster upgrades
