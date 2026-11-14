---
type: Guide
title: Agentic AI
description: Covers agent anatomy, common agent patterns, the boundaries autonomy needs, and multi-agent topologies.
tags: [ai, agentic-ai, agents, llm]
---

An **Agent** is an [LLM](03-llm.md) inside a loop where it can **reason**, **act** through tools, **observe** results, and **iterate** toward a goal. The loop turns a passive text predictor into an autonomous problem solver. This guide is for engineers deciding whether a task needs an agent at all, and how to bound one that does.

## Anatomy of an Agent

| Component | Role |
| --- | --- |
| **Model (reasoner)** | The LLM that decides what to do next |
| **Goal / `Task`** | The objective the agent pursues |
| **Tools** | External capabilities (search, code execution, `APIs`, databases) the agent can invoke |
| **Memory** | Short-term (context) and long-term (vector store / files) state across steps |
| **Planning** | Decomposing goals into ordered subtasks |
| **Loop / Controller** | The perceive → decide → act → observe cycle, with a stopping condition |

```svg
<Panel caption="The agent loop">
  <Node key="start" col="0" row="0" shape="point" />
  <Node key="perceive" col="1" row="0" label="Perceive" shape="round" tone="primary" />
  <Node key="decide" col="2" row="0" label="Decide" shape="round" />
  <Node key="act" col="3" row="0" label="Act" shape="round" />
  <Node key="observe" col="3" row="1" label="Observe" shape="round" />
  <Node key="end" col="4" row="1" shape="point" />
  <Edge from="start" to="perceive" />
  <Edge from="perceive" to="decide" label="context" />
  <Edge from="decide" to="act" label="tool call" />
  <Edge from="act" to="observe" label="result" />
  <Edge from="observe" to="perceive" label="continue" fromSide="left" toSide="bottom" />
  <Edge from="observe" to="end" label="goal met" />
</Panel>
```

## Common Agent Patterns

Prompt Chaining, Routing and the guidance below follow Anthropic's [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents); ReAct is from Yao et al. (see [References](index.md#references)).

| Pattern | Idea |
| --- | --- |
| **ReAct** | Interleave **Rea**soning traces with **Act**ions and observations |
| **Plan-and-Execute** | Produce a full plan first, then carry out each step |
| **Reflection / Self-Critique** | Agent reviews and revises its own output |
| **Tool Use** | Delegate to external functions rather than reasoning in a vacuum |
| **Prompt Chaining** | Pipe one step's output into the next |
| **Routing** | Classify the request and dispatch to a specialized handler |

> **Engineering guidance:** prefer the simplest design that works. Add autonomy only when a fixed workflow cannot handle how open-ended the task is. Autonomy buys flexibility at the cost of predictability, latency, and token spend.

## Autonomy Boundaries

These rules apply once an agent can act on the world without a human approving each step.

1. **The stopping condition belongs outside the loop.** A controller whose job is to remove blockers treats any constraint it is asked to evaluate as one more blocker to route around. Fix the conditions under which the agent must stop before the loop runs, and enforce them in code the loop does not control.
2. **The constraint set is not self-modifiable.** `Plans`, tools, memory, and the agent's own structure can all change from inside the loop. What the agent is not allowed to do cannot — otherwise the boundary is only decoration.
3. **A sandbox needs a restoring boundary.** An agent may run with relaxed constraints in an isolated environment for training or evaluation. The mechanism that reimposes the constraints at the sandbox-to-production edge sits outside that environment, so a relaxation granted for training cannot travel with the agent into production.

## Multi-Agent Systems (MAS)

A **Multi-Agent System** coordinates several specialized agents, each with its own role, tools, and context, to tackle problems too broad or too parallel for a single agent.

| Topology | Description |
| --- | --- |
| **Orchestrator–Worker** | A lead agent plans and delegates subtasks to worker agents, then synthesizes results |
| **Hierarchical** | Layered supervisors and sub-agents mirroring an org chart |
| **Sequential Pipeline** | Agents arranged as stages, each refining the previous output |
| **Debate / Ensemble** | Agents argue or vote to reach a better answer |
| **Blackboard** | Agents read/write a shared workspace asynchronously |
| **Network / Swarm** | Peer agents communicate freely without a central controller |

```svg
<Panel>
  <Node key="mas" col="2" row="2" rowspan="2" label="MAS" shape="circle" tone="primary" />
  <Node key="ow" col="1" row="0" label="Orchestrator-Worker" shape="round" />
  <Node key="lead" col="0" row="0" label="Lead" shape="pill" />
  <Node key="workers" col="0" row="1" label="Workers" shape="pill" />
  <Node key="hier" col="1" row="2" label="Hierarchical" shape="round" />
  <Node key="supervisor" col="0" row="2" label="Supervisor" shape="pill" />
  <Node key="subagents" col="0" row="3" label="Sub-agents" shape="pill" />
  <Node key="seq" col="1" row="4" label="Sequential Pipeline" shape="round" />
  <Node key="stage1" col="0" row="4" label="Stage 1" shape="pill" />
  <Node key="stage2" col="0" row="5" label="Stage 2" shape="pill" />
  <Node key="debate" col="3" row="0" label="Debate" shape="round" />
  <Node key="proposer" col="4" row="0" label="Proposer" shape="pill" />
  <Node key="critic" col="4" row="1" label="Critic" shape="pill" />
  <Node key="board" col="3" row="2" label="Blackboard" shape="round" />
  <Node key="store" col="4" row="2" label="Shared store" shape="pill" />
  <Node key="swarm" col="3" row="4" label="Swarm" shape="round" />
  <Node key="peers" col="4" row="4" label="Peer agents" shape="pill" />
  <Edge from="mas" to="ow" arrow="none" />
  <Edge from="mas" to="hier" arrow="none" />
  <Edge from="mas" to="seq" arrow="none" />
  <Edge from="mas" to="debate" arrow="none" />
  <Edge from="mas" to="board" arrow="none" />
  <Edge from="mas" to="swarm" arrow="none" />
  <Edge from="ow" to="lead" arrow="none" />
  <Edge from="ow" to="workers" arrow="none" />
  <Edge from="hier" to="supervisor" arrow="none" />
  <Edge from="hier" to="subagents" arrow="none" />
  <Edge from="seq" to="stage1" arrow="none" />
  <Edge from="seq" to="stage2" arrow="none" />
  <Edge from="debate" to="proposer" arrow="none" />
  <Edge from="debate" to="critic" arrow="none" />
  <Edge from="board" to="store" arrow="none" />
  <Edge from="swarm" to="peers" arrow="none" />
</Panel>
```

| Concern | Why it matters |
| --- | --- |
| **Communication Protocol** | How agents pass messages and share state without losing coherence |
| **Coordination & Conflict** | Avoiding duplicated work, deadlock, or contradictory actions |
| **Cost & Latency** | Each agent multiplies token usage and round-trips |
| **Error Propagation** | One agent's mistake can cascade; needs checkpoints and validation |
| **Observability** | Tracing decisions across agents is essential for debugging |

> Multi-agent designs work best for parallel, decomposable work (research, large-scale code changes), but they add real complexity. A single capable agent with good tools is often enough, and cheaper.
