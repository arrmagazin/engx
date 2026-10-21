---
type: Guide
title: Large Language Models (LLM)
description: Covers LLM core mechanics, the training lifecycle, inference controls, and usage techniques like RAG and tool calling.
tags: [ai, llm, transformer, prompt-engineering]
---

An **LLM** is a transformer-based model trained on vast text corpora to predict the next **token**. Broad knowledge and language ability emerge as a side effect of that single objective.

In the stack described in [Artificial Intelligence](index.md), it sits between deep learning and agents:

- a transformer is the architecture;
- an LLM is that architecture trained at scale;
- an [Agent](04-agents.md) is an LLM wrapped in a loop with tools and memory.

This guide is for engineers building on an LLM API. The papers and guides behind it are under [References](index.md#references).

## Core Mechanics

These mechanics bound everything later in this guide. The model has no unit of work smaller than a token, can attend to nothing beyond the context window, and draws every output from a distribution. That is why cost, truncation and non-determinism are properties of the architecture, not quirks of a particular API.

Token
: The atomic unit of text (sub-word fragment) the model reads and emits

Tokenizer
: The component that maps text to and from tokens (BPE, for example), driving cost, context limits, and multilingual fairness

Transformer
: Architecture built on stacked self-attention and feed-forward blocks

Attention
: Mechanism letting each token weigh the relevance of every other token

Context Window
: Maximum tokens the model can attend to at once (prompt + output)

Parameters
: The learned weights; scale correlates with capability

Logits / Sampling
: A probability distribution over the next tokens, from which the emitted token is drawn

## Training Lifecycle

These stages are how a particular model acquires its behavior. Each stage after pre-training narrows a general next-token predictor into one that follows instructions and answers as its owners intended.

For an engineer, the lifecycle matters mostly as a boundary: whatever these stages put into the weights is fixed by the time you hold an API key. Everything still adjustable happens at inference.

| Stage | Purpose |
| --- | --- |
| **Pre-training** | Self-supervised next-token prediction on broad corpora — builds general competence |
| **Fine-tuning** | Adapt to a domain or task on a smaller curated dataset |
| **Instruction Tuning** | Teach the model to follow natural-language instructions |
| **RLHF / RLAIF** | Align outputs with human (or AI) preferences via reinforcement learning |
| **Distillation** | Compress a large model's behavior into a smaller, cheaper one |

## Inference Controls

These parameters are the cheapest thing to change at inference — try them before anything more elaborate. None of them changes what the model knows. They shape how it uses that knowledge: how much of the distribution the next token may come from, how long generation runs, and what instruction applies to every turn.

| Parameter | Effect |
| --- | --- |
| **Temperature** | Higher = more random/creative; lower = more deterministic |
| **Top-p / Top-k** | Restrict sampling to the most probable tokens (nucleus / top-k) |
| **Max Tokens** | Caps the length of the generated output |
| **System Prompt** | Persistent instruction shaping role, tone, and constraints |
| **Stop Sequences** | Strings that halt generation |

## Usage Techniques

When the controls are not enough, what is left is the prompt and what you put around it. The techniques below add different things — examples, intermediate reasoning, retrieved documents, a schema, a tool result — but all go through one channel: the context window is the only route by which anything training did not supply reaches the model.

| Technique | Description |
| --- | --- |
| **Prompt Engineering** | Crafting input to elicit desired behavior |
| **Zero-Shot / Few-Shot** | Solving a task with no examples, or with a handful supplied in the prompt rather than by retraining — also called in-context learning |
| **Chain-of-Thought (CoT)** | Prompting step-by-step reasoning to improve accuracy on complex tasks |
| **RAG** | Retrieval-Augmented Generation — inject relevant external documents into context |
| **Function / Tool Calling** | Model emits structured calls the host executes and feeds back |
| **Structured Output** | Constrain responses to JSON/schema for reliable downstream parsing |

> **Design around two failure modes.** Both come from the core mechanics, not from any technique above, so budget for them rather than try to remove them.
>
> - **Hallucination** — confident but false output.
> - **Context limits** — truncation and "lost in the middle" degradation on long inputs (Liu et al., 2023, [Lost in the Middle](https://arxiv.org/abs/2307.03172)).
