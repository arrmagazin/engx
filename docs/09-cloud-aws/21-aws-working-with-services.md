---
type: Guide
title: Working with AWS
description: AWS core services, networking, storage, identity, and DevOps.
tags: [interview, aws, cloud, devops]
---

# Working with AWS

##  Implementing & Maintaining Intricate AWS Infrastructure (Native + OSS Tools)

### Infrastructure as Code (IaC) options
| Tool | Native/OSS | Notes |
|---|---|---|
| **CloudFormation** | Native | YAML/JSON, stacks + change sets, StackSets for multi-account/region; drift detection built in |
| **AWS CDK** | Native | TypeScript/Python/etc. that *synthesizes* CloudFormation; constructs and aspects for reuse |
| **Terraform (aws provider)** | OSS (HashiCorp) | Multi-cloud, explicit state, by far the most common in mixed estates |
| **Pulumi** | OSS | IaC in general-purpose languages, own state backend |
| **SAM / Serverless Framework** | Native / OSS | Opinionated shorthand for Lambda-centric stacks |
| **Ansible (`amazon.aws`)** | OSS | Config management + light provisioning |

Be ready to discuss:
- **State management**: Terraform remote state in S3 with locking (S3 conditional writes natively since 2024 — the DynamoDB lock table is now legacy, and knowing that shows you are current)
- **Modules**: CDK constructs vs Terraform modules — reuse, versioning, private registries, when a shared module becomes a bottleneck
- **Drift detection**: `terraform plan`, CloudFormation drift detection, AWS Config rules
- **Idempotency**: why declarative tools converge safely on repeated runs — and where AWS APIs make that hard (eventual consistency, non-updatable properties forcing replacement)
- **Multi-environment strategy**: **account-per-environment** is the AWS-idiomatic answer, not one account with tags. Say that out loud.

### Maintaining infrastructure at scale
- **Landing zone architecture**: AWS Control Tower, Landing Zone Accelerator, the multi-account strategy from the Well-Architected Framework
- **Network topology**: Transit Gateway hub-and-spoke, centralized egress and inspection VPCs
- **Account vending**: Control Tower Account Factory / AFT (Account Factory for Terraform) for multi-team orgs
- **Backup & DR**: AWS Backup (org-wide backup policies), pilot light vs warm standby vs multi-site, RTO/RPO planning
- **Patch management**: SSM Patch Manager for mutable fleets; image-based patching (EC2 Image Builder) for the immutable approach
- **Quotas and limits**: Service Quotas — the thing that actually breaks large deployments; know that ENIs, EIPs, and VPC CIDRs run out before CPU does

---

##  Automating Infrastructure Changes & Configuration Management

### CI/CD for infrastructure
- **GitHub Actions / GitLab CI** vs native **CodePipeline + CodeBuild** (and CodeCatalyst): where the code already lives usually decides it
- **Pipeline patterns**: plan → manual approval → apply (Terraform); `cdk diff` / change set → review → execute (CloudFormation/CDK)
- **Credentials**: **OIDC federation to an IAM role** — never store access keys in CI. This is the single highest-signal thing to mention.
- **GitOps**: Flux/Argo CD on EKS, config as the source of truth
- **Multi-account deploys**: a pipeline in a tooling account assuming a deployment role in each target account

### Configuration management
- **Systems Manager**: State Manager (associations = continuous enforcement), Run Command, Automation runbooks, Session Manager (shell access without SSH — removes the need for bastion hosts)
- **Ansible** for post-provision config on EC2, especially mixed-OS or ordered multi-host sequences
- **user-data / cloud-init** for bootstrap; **AWS Config remediation actions** for auto-correcting non-compliant resources
- **EventBridge → Lambda** as the general-purpose "react to an infrastructure event" pattern

### Secrets & config
- **Secrets Manager** (rotation built in, priced per secret) vs **SSM Parameter Store** (SecureString, free standard tier, no native rotation)
- Injecting secrets: ECS task definition `secrets` block, Lambda extensions, External Secrets Operator on EKS
- Never bake secrets into AMIs or images — expect a question probing whether you know this

### Testing infrastructure code
- **Terratest**, **cfn-lint**, **CDK assertions / snapshot tests**, `checkov` / `tfsec` / `cfn-nag` for policy-as-code scanning
- **Open Policy Agent / Conftest** or CloudFormation **Guard** for org-specific rules in the pipeline

---

##  Immutable Infrastructure, Automated Infrastructure & Cloud-Native Frameworks

### Immutable infrastructure concepts
- **Golden AMIs**: EC2 Image Builder or Packer — bake config into the image rather than mutating running servers
- **ASG instance refresh / rolling replacement**: replace instances instead of patching in place; ASG lifecycle hooks for graceful drain
- **Blue/green and canary**: **CodeDeploy** (ECS/Lambda/EC2 blue-green), ALB weighted target groups, Lambda alias traffic shifting, Argo Rollouts or Flagger on EKS
- **Immutable containers**: pin images by digest not tag, ECR immutable tags setting, no `latest` in production

### Cloud-native / CNCF-aligned practices
- **Containerization**: Docker fundamentals, multi-stage builds, distroless base images, scanning (ECR enhanced scanning via Inspector, Trivy)
- **Kubernetes on EKS**:
  - Deployments, StatefulSets, DaemonSets, Services, Ingress (AWS Load Balancer Controller)
  - Helm for packaging
  - HPA / **Karpenter** (AWS-originated, now CNCF) vs Cluster Autoscaler
  - **IRSA / EKS Pod Identity** for AWS API access from pods — the container-native alternative to node roles
  - Network policies, VPC CNI prefix delegation for IP density
- **Service mesh basics**: Istio/Linkerd concepts (traffic management, mTLS); App Mesh is being retired — knowing that shows you follow the roadmap
- **KEDA** for event-driven autoscaling (scaling on SQS depth, etc.)
- **12-factor app principles** as the philosophy underlying cloud-native automation
- **Serverless-first thinking**: Lambda + EventBridge + Step Functions as an architecture, not just glue
