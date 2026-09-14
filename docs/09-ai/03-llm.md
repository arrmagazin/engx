---
type: Guide
title: Large Language Models (LLM)
description: Covers LLM core mechanics, the training lifecycle, inference controls, and usage techniques like RAG and tool calling.
tags: [ai, llm, transformer, prompt-engineering]
---

An **LLM** is a transformer-based model trained on vast text corpora to predict the next **token**,
acquiring broad knowledge and language ability as an emergent side effect of that single objective.

It sits between deep learning and agents in the stack described in
[Artificial Intelligence](index.md): a transformer is the architecture, an LLM is that
architecture trained at scale, and an [Agent](04-agents.md) is an LLM wrapped in a loop with tools
and memory. This guide is written for engineers building on an LLM API; the papers and guides behind
it are collected under [References](index.md#references).

## Core Mechanics

Everything later in this guide is bounded by the mechanics below. The model has no unit of work
smaller than a token, nothing it can attend to beyond the context window, and no output that was not
drawn from a distribution — which is why cost, truncation, and non-determinism are properties of the
architecture rather than quirks of a particular API.

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

Those mechanics describe the machinery; the stages below are how a particular model acquires the
behavior you call. Each stage after pre-training narrows a general next-token predictor into
something that follows instructions and answers the way its owners intended. For an engineer the
lifecycle matters mostly as a boundary: whatever these stages put into the weights is settled by the
time you hold an API key, and everything still adjustable happens at inference.

| Stage | Purpose |
| --- | --- |
| **Pre-training** | Self-supervised next-token prediction on broad corpora — builds general competence |
| **Fine-tuning** | Adapt to a domain or task on a smaller curated dataset |
| **Instruction Tuning** | Teach the model to follow natural-language instructions |
| **RLHF / RLAIF** | Align outputs with human (or AI) preferences via reinforcement learning |
| **Distillation** | Compress a large model's behavior into a smaller, cheaper one |

## Inference Controls

Inference is where the adjustable part starts, and these parameters are the cheapest thing in it to
change. None of them alters what the model knows; they shape how it draws on that — how much of the
distribution the next token may come from, how long generation runs, and what instruction stands
over every turn. Reach for them before reaching for anything more elaborate.

| Parameter | Effect |
| --- | --- |
| **Temperature** | Higher = more random/creative; lower = more deterministic |
| **Top-p / Top-k** | Restrict sampling to the most probable tokens (nucleus / top-k) |
| **Max Tokens** | Caps the length of the generated output |
| **System Prompt** | Persistent instruction shaping role, tone, and constraints |
| **Stop Sequences** | Strings that halt generation |

## Usage Techniques

When the controls are not enough, what is left is the prompt and what you put around it. The
techniques below differ in what they add — examples, intermediate reasoning, retrieved documents, a
schema, the result of a tool call — but they work through the same channel, because the context
window is the only route by which anything training did not supply reaches the model.

| Technique | Description |
| --- | --- |
| **Prompt Engineering** | Crafting input to elicit desired behavior |
| **Zero-Shot / Few-Shot** | Solving a task with no examples, or with a handful supplied in the prompt rather than by retraining — also called in-context learning |
| **Chain-of-Thought (CoT)** | Prompting step-by-step reasoning to improve accuracy on complex tasks |
| **RAG** | Retrieval-Augmented Generation — inject relevant external documents into context |
| **Function / Tool Calling** | Model emits structured calls the host executes and feeds back |
| **Structured Output** | Constrain responses to JSON/schema for reliable downstream parsing |

Routing everything through that one channel is also what leaves two failures standing, both of them
traceable to the mechanics at the top of this guide rather than to any technique above — which is
why they are budgeted for rather than removed.

> Two failure modes to design around: **hallucination** (confident but false output) and
> **context limits** (truncation and "lost in the middle" degradation on long inputs).
