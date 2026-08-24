---
type: Guide
title: Containers — core concepts and orchestration
description: Explains what a container is, how images are built and shipped, what an orchestrator does, and how containers shape a system design.
tags: [tech-stack, containers, docker, oci, deployment]
---

# Containers — core concepts and orchestration

## Core concepts

- **Container** — one or more processes running on the *host's* kernel, isolated so they behave as if they owned the machine. Not a virtual machine: no guest OS, no boot sequence, starts in milliseconds.
- **Namespace** — the kernel primitive that controls *what a process can see*: its own process tree, network stack, mounts, hostname, users. Isolation is per-namespace rather than all-or-nothing, so a container can share the host's network while keeping its own filesystem.
- **cgroup (control group)** — the kernel primitive that controls *how much a process can use*: CPU shares, memory ceiling, I/O bandwidth. Cross the memory ceiling and the kernel kills the process; it does not throttle it.
- **Image** — a read-only filesystem plus metadata (entrypoint, default environment, exposed ports, user). The image is the build-time artifact; a container is one running instance of it.
- **Layer** — each build instruction produces a filesystem diff. Layers stack, are content-addressed, are cached between builds, and are shared between images that start the same way — so pulling a second image built on the same base only transfers what differs.
- **Registry** — the store images are pushed to and pulled from (Docker Hub, ECR, GHCR).
- **Tag vs. digest** — a tag (`app:1.4`) is a *mutable pointer*; a digest (`app@sha256:…`) names exact bytes. Only the digest is a version.
- **OCI (Open Container Initiative)** — three specifications (image, runtime, distribution) that make the ecosystem interchangeable: an image built by one tool runs under another runtime and lives in any registry. See [Standards](../00-software-engineering/02-standards.md).
- **Container runtime** — split in two. A *high-level* runtime (containerd, CRI-O) pulls images and manages lifecycle; a *low-level* one (runc) actually asks the kernel for the namespaces and cgroups.
- **Ephemeral filesystem** — the container's writable layer dies with the container. Anything that must survive goes to a **volume** (storage mounted in from outside) or, in a distributed system, out to a Database or Object Storage.
- **Container vs. VM** — a VM virtualizes hardware and boots its own kernel: a stronger isolation boundary, seconds to start, hundreds of MB of overhead. A container virtualizes the operating system: a weaker boundary (a kernel exploit escapes it), milliseconds to start, near-zero overhead. Managed platforms often close that gap by running each container inside its own micro-VM.

## Build and ship workflow

1. **Write a Dockerfile** — an ordered recipe: base image, dependency install, source copy, entrypoint.
2. **Send a build context** — the builder receives the directory you point it at. `.dockerignore` keeps `node_modules`, `.git`, and local secrets out of it; a large context slows every build.
3. **Build, layer by layer** — each instruction is cached against the hash of its inputs and the layer below. The first instruction whose inputs changed invalidates itself *and everything after it*.
4. **Tag, and record the digest** — the tag is for humans, the digest is what you deploy.
5. **Push to a registry** — only layers the registry does not already hold travel over the wire.
6. **Pull on the target host** — likewise, only the missing layers. A host that already ran a sibling image pulls almost nothing; a fresh host pulls everything.
7. **Run** — the runtime stacks the layers into one filesystem, creates the namespaces and cgroups, and starts the entrypoint as process 1 inside them.

The same image, byte for byte, runs in every environment. What differs between environments is Configuration injected at step 7 — never a rebuild.

## Running many — what an orchestrator does

One container on one host is a single command. A real system is tens to thousands of them across a fleet, and everything below is the work an orchestrator takes over. The products differ; the jobs do not.

- **Desired-state reconciliation** — you declare "ten replicas of this image"; a controller continuously compares reality against that and acts. Declarative, not imperative: you never issue "start one more".
- **Scheduling and bin-packing** — placing each container on a host with enough free CPU and memory, honouring constraints (spread across failure zones, keep these two apart, this one needs a GPU). Declared resource requests are the input, so getting them wrong either wastes half the fleet or packs it until everything degrades together.
- **Health checks** — two different questions. *Liveness*: is this still working? If not, restart it. *Readiness*: can this take traffic right now? If not, remove it from the load balancer but leave it running. Conflating them is a common outage — a slow-starting application fails its liveness check during warm-up and restarts forever.
- **Service discovery and load balancing** — instances are created and destroyed constantly, so callers address a stable name that resolves to whichever instances are currently healthy.
- **Rolling deploys** — replace instances in batches, bounded by how many may be down and how many extra may exist at once. Blue/green stands up a second full fleet and switches over; canary sends a small share of traffic to the new version first and watches the metrics.
- **Autoscaling** — horizontal (more replicas, the normal answer for stateless work) or vertical (bigger replicas, for work that cannot be split).
- **Configuration and secrets at run time** — injected as environment variables or mounted files, so one image serves every environment.
- **Restart with backoff** — crash loops are slowed down rather than retried tightly, so a broken deploy does not hammer its dependencies.

For the managed implementations of all of this, see [AWS stack overview](../07-cloud-aws/01-aws-stack-overview.md) and [Azure stack overview](../08-cloud-azure/01-azure-stack-overview.md).

## Design implications

- **Stateless by default.** Instances appear and disappear without warning, so whatever a container writes locally is lost. Session data goes to a Cache, records to a Database, uploads to Object Storage. "Stateless" does not mean the system holds no state — it means no state lives in the compute tier.
- **Shutdown is a contract.** The orchestrator sends SIGTERM, waits a grace period, then sends SIGKILL. In that window the application must stop accepting new work, finish what is in flight, and close its connections. Ignore SIGTERM and every deploy drops requests — invisible in staging, obvious under load.
- **Image size is scale-out latency.** A host with no cached layers pulls the whole image before the container starts. A 1.5 GB image can add tens of seconds to each new instance, which is precisely when you needed it. Multi-stage builds matter operationally, not just aesthetically.
- **Sidecars.** A second container in the same unit, sharing network and lifecycle — a log shipper, a proxy, a metrics agent. Useful, but platforms that bill per container make each sidecar a real cost, and platforms with no node-level agents force this pattern whether you wanted it or not.
- **Requests and limits are two different numbers.** The request is what the scheduler reserves; the limit is what the kernel enforces. Set the request too low and hosts get oversubscribed. Set no memory limit and one leak takes its neighbours down. Set the limit too low and the kernel kills the process with no stack trace.

| | Container | Virtual machine | Serverless function |
|---|---|---|---|
| Unit | Process group on a shared kernel | Full guest operating system | One invocation |
| Start | Milliseconds, once the image is pulled | Tens of seconds | Milliseconds, plus cold start |
| You operate | Image and orchestrator config | OS, patching, capacity | Code only |
| Scales to zero | Rarely, and slowly | No | Yes |
| Best for | Long-running services with steady or shaped load | Legacy, kernel-level, or strict-isolation workloads | Spiky, short, event-driven work |
| Deciding question | Does it need to stay up and hold connections? | Do you need your own kernel or hardware access? | Does every request finish well inside the timeout? |

## Entities diagram

```
Dockerfile
    │ build (each instruction becomes one cached layer)
    ▼
┌─────────── Image ────────────┐
│ metadata: entrypoint, user   │
│ ┌──────────────────────────┐ │
│ │ layer 3 — app source     │ │
│ ├──────────────────────────┤ │
│ │ layer 2 — dependencies   │ │
│ ├──────────────────────────┤ │
│ │ layer 1 — base OS        │ │
│ └──────────────────────────┘ │
└──────────────┬───────────────┘
               │ push / pull by digest
               ▼
        ┌──────────────┐
        │   Registry   │
        └──────┬───────┘
               │
               ▼
┌─────────────── Host (shared kernel) ─┐
│  ┌────────────┐    ┌────────────┐    │
│  │ Container  │    │ Container  │    │
│  │  writable  │    │  writable  │    │
│  │   layer    │    │   layer    │    │
│  └─────┬──────┘    └────────────┘    │
│        │  namespaces + cgroups       │
└────────┼─────────────────────────────┘
         ▼
   Volume — the only part that outlives the container

Orchestrator: desired state → scheduling → health checks → rollout
```

Two containers from the same image share every layer on disk and differ only in their writable layer and the configuration handed to them at start. The host contributes the kernel; the orchestrator decides which host, how many, and when to replace them.

## Details people get wrong

- **Process 1 gets no default signal handlers.** The kernel gives process 1 no default action for SIGTERM, so an application that does not explicitly handle it simply ignores the signal and dies to SIGKILL when the grace period expires. Shell-form `CMD npm start` makes it worse: the shell becomes process 1 and never forwards the signal. Use exec form and handle SIGTERM in code.
- **`latest` is not a version.** It is a mutable tag that can point at different bytes tomorrow, so two hosts pulling it an hour apart can run different code. Deploy by digest.
- **Containers run as root unless told otherwise.** Root inside the container is root on the kernel it shares with everything else on the host. Declare a non-root user.
- **Copying source before installing dependencies busts the cache on every build.** Any source change invalidates the copy layer and everything below it, including the dependency install. Copy the manifest, install, *then* copy the source.
- **Deleting a secret in a later layer does not remove it.** Layers are additive diffs, so the earlier layer still holds it and anyone who pulls the image can read it. The same applies to build arguments. Use build secrets, or inject at run time.
- **Shipping the build toolchain to production.** Compilers, dev dependencies, and test fixtures inflate the image and widen the attack surface. Leaving them behind is the point of a second build stage.
- **Writing logs to a file inside the container.** The file dies with the container and nothing collects it. Write to standard output and standard error, and let the platform ship them.

## Dockerfile — multi-stage Node example

```dockerfile
# --- build stage: holds the toolchain, never ships ---
FROM node:22-slim@sha256:<digest> AS build
WORKDIR /app

# manifest first, so this layer stays cached until dependencies actually change
COPY package.json package-lock.json ./
RUN npm ci

# source last, so editing it invalidates only the layers below
COPY . .
RUN npm run build && npm prune --omit=dev

# --- runtime stage: only what is needed to run ---
FROM node:22-slim@sha256:<digest>
WORKDIR /app
ENV NODE_ENV=production

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist

# non-root; this user already exists in the base image
USER node

# exec form — node is process 1 and receives SIGTERM directly
CMD ["node", "dist/server.js"]
```

Both `FROM` lines pin a digest rather than a tag, so the build is reproducible. The image carries no environment-specific values: the connection strings and secrets arrive at run time. Receiving SIGTERM is only half the shutdown contract — the application still has to stop the listener and drain in-flight requests before the grace period ends.
