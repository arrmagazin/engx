---
type: Guide
title: Containers — Core Concepts and Orchestration
description: Explains what a container is, how images are built and shipped, what an orchestrator does, and how containers shape a system design.
tags: [tech-stack, containers, docker, oci, deployment]
---

A container is an application and its dependencies, packaged as an image and run as an isolated process on the host's kernel. This guide covers how that isolation works, how images are built and shipped, what an orchestrator does, and what it all means for state.

## Core Concepts

- **Namespace** — the kernel primitive controlling *what a process can see*: process tree, network, mounts, users. Isolation is per namespace, so a container can share the host's network but keep its own filesystem.
- **cgroup** — the kernel primitive controlling *how much a process can use*: CPU, memory, I/O.
- **Image** — a read-only filesystem plus metadata (entrypoint, environment, user). A container is one running instance of it.
- **Layer** — the filesystem diff one build instruction produces. Layers are content-addressed, cached between builds, and shared between images, so pulling a second image on the same base transfers only what differs.
- **Tag vs. digest** — a tag (`app:1.4`) is a *mutable pointer*; a digest (`app@sha256:…`) names exact bytes. Only the digest is a version.
- **OCI (Open Container Initiative)** — the [standard](../00-software-engineering/02-standards.md) image, runtime, and registry specifications, so an image built by one tool runs under any runtime.
- **Ephemeral filesystem** — the container's writable layer dies with it. Anything that must survive goes to a **volume** mounted from outside or, in a distributed system, to a Database or Object Storage.
- **Container vs. VM** — a VM boots its own kernel: a stronger isolation boundary, paid for with a guest OS that must boot and stay resident. A container is a process on the shared kernel — nothing to boot — but a kernel exploit escapes it.

## Build and Ship Workflow

1. **Build** from a Dockerfile. Each instruction is cached against the hash of its inputs; the first one whose inputs changed invalidates itself *and everything after it*.
2. **Tag, and record the digest** — the tag is for humans; the digest is what you deploy.
3. **Push to a registry, pull on the host** — only missing layers travel, so a fresh host pulls everything.
4. **Run** — the runtime stacks the layers, creates the namespaces and cgroups, and starts the entrypoint as process 1.

The same image runs in every environment; only the Configuration injected at run time differs.

## What an Orchestrator Does

A real system runs tens to thousands of containers across a fleet. The orchestrator products differ; the jobs do not.

- **Desired-state reconciliation** — you declare "ten replicas of this image"; a controller keeps reality matching it. A deploy points it at a new versioned template; rollback points it back.
- **Scheduling** — placing each container on a host with enough free CPU and memory, spread across failure zones. Declared resource requests are the input: wrong numbers waste the fleet or overload it.
- **Health checks** — two different questions:
  - *Liveness* — is it still working? If not, restart it.
  - *Readiness* — can it take traffic now? If not, remove it from the [load balancer](06-client-server-communication.md#load-balancing) but leave it running.
  - Conflating them causes outages: a slow-starting application fails liveness during warm-up and restarts forever. On shutdown, an instance reports *not ready* while staying *alive*, so traffic stops but the drain is not cut short.
- **Deploy strategies**:
  - *Rolling* — replace instances in batches. It needs no spare fleet, but two versions serve at once, so every change must stay backward compatible for the length of the roll.
  - *Blue/green* — stand up a second fleet and switch traffic to it. Fastest rollback, at the cost of two fleets; awkward when both versions share a database only one schema fits.
  - *Canary* — send a small share of traffic to the new version first. It optimizes *detection* while the blast radius is small, and needs metrics good enough to tell the canary from the baseline.
- **Autoscaling and restarts** — more replicas for stateless work; crash loops restarted with backoff, so a broken deploy does not hammer its dependencies.

The managed versions across the three clouds are in [Compute — Containers](../08-clouds/01-concept-map.md#compute--containers).

## Design Implications

- **Stateless by default.** Instances disappear without warning, so sessions go to a Cache, records to a Database, uploads to Object Storage.
- **Shutdown is a contract.** The orchestrator sends SIGTERM, waits a grace period, then SIGKILL; in that window the application finishes in-flight work. Process 1 gets no default signal handlers, so an application that does not handle SIGTERM — or a shell-form `CMD npm start`, whose shell never forwards it — makes every deploy fail whoever was mid-request. Use exec form and handle the signal.
- **Image size is scale-out latency.** A fresh host pulls the whole image before the container starts, exactly when the capacity is needed.
- **Sidecars** — a second container in the same unit (a log shipper, proxy, or metrics agent) that adds a concern without touching the application, but shares its resources and can delay startup and shutdown.
- **Requests and limits are two numbers.** The request is what the scheduler reserves; the limit is what the kernel enforces. With no memory limit, one leak takes its neighbors down; with too low a limit, the kernel kills the process with no stack trace.

Choosing between compute models comes down to one question each: a **container** if it must stay up and hold connections; a **VM** if it needs its own kernel or hardware access; a **serverless function** if every request finishes well inside the timeout and the load is spiky enough to want scaling to zero.

## Details People Get Wrong

- **`latest` is not a version.** Two hosts pulling it an hour apart can run different code. Deploy by digest.
- **Containers run as root unless told otherwise**, and that root shares the host's kernel. Declare a non-root user.
- **Copying source before installing dependencies** invalidates the install layer on every change. Copy the manifest, install, *then* copy the source.
- **Deleting a secret in a later layer does not remove it** — the earlier layer still holds it. Use build secrets, or inject at run time.
- **Shipping the build toolchain** — a multi-stage build leaves it behind.
- **Logging to a file in the container** — the file dies with it. Write to standard output and let the platform collect it.

## References

1. [Docker Cheat Sheet](https://devsheets.io/sheets/docker-commands) — DevSheets
2. [Kubernetes Essentials Cheat Sheet](https://devsheets.io/sheets/kubernetes-essentials) — DevSheets
