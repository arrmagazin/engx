---
type: Guide
title: CI/CD
description: Explains continuous integration and delivery pipelines and the environment stages code moves through before production.
tags: [devops, ci-cd, development-process]
---

Continuous integration (CI) *verifies* every commit against the shared mainline; continuous delivery (CD) *moves* each verified build toward production. This guide covers both, and the environment stages a change passes through before it reaches users.

```svg
<Panel>
  <Node key="code" col="0" row="1" label="Code" />
  <Node key="build" col="1" row="1" label="Build" />
  <Node key="test" col="2" row="1" label="Test" />
  <Node key="deploy" col="3" row="1" label="Deploy" />
  <Node key="monitor" col="3" row="2" label="Monitor" />
  <Edge from="code" to="build" />
  <Edge from="build" to="test" />
  <Edge from="test" to="deploy" label="pass" />
  <Edge from="test" to="code" label="fail" fromSide="top" toSide="top" />
  <Edge from="deploy" to="monitor" />
  <Edge from="monitor" to="code" label="regression" fromSide="left" toSide="bottom" />
</Panel>
```

| Aspect | CI | CD |
| --- | --- | --- |
| **Focus** | Code integration | Automated deployment |
| **Goal** | Detect integration issues | Deploy to production |
| **Frequency** | Every commit | After CI passes |
| **Tools** | GitHub Actions, Jenkins | Argo CD, Spinnaker |

## Environment Stages

| Environment | Purpose *(data)* | Promotion |
| --- | --- | --- |
| **Local** | Individual development *(mocked/sample)* | Push to a shared branch |
| **Development** | Integration testing *(test database)* | Promote once CI passes |
| **Staging** | Pre-production and user acceptance testing *(production-like)* | Release to production |
| **Production** | End users *(real data)* | None — telemetry feeds the next change |

## References

1. [GitHub Actions Documentation](https://docs.github.com/en/actions)
