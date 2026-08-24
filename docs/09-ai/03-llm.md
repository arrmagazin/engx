---
type: Guide
title: Large Language Models (LLM)
description: Covers LLM core mechanics, the training lifecycle, inference controls, and usage techniques like RAG and tool calling.
tags: [ai, llm, transformer, prompt-engineering]
---

# Large Language Models (LLM)

An **LLM** is a transformer-based model trained on vast text corpora to predict the next **token**,
acquiring broad knowledge and language ability as an emergent side effect of that single objective.

It sits between deep learning and agents in the stack described in
[Artificial Intelligence](00-ai.md): a transformer is the architecture, an LLM is that
architecture trained at scale, and an [Agent](04-agents.md) is an LLM wrapped in a loop with tools
and memory. This guide is written for engineers building on an LLM API; the papers and guides behind
it are collected under [References](00-ai.md#references).

## Core Mechanics

| Concept | Definition |
| --- | --- |
| **Token** | The atomic unit of text (sub-word fragment) the model reads and emits |
| **Tokenizer** | The component that maps text to and from tokens (BPE, for example), driving cost, context limits, and multilingual fairness |
| **Transformer** | Architecture built on stacked self-attention and feed-forward blocks |
| **Attention** | Mechanism letting each token weigh the relevance of every other token |
| **Context Window** | Maximum tokens the model can attend to at once (prompt + output) |
| **Parameters** | The learned weights; scale correlates with capability |
| **Logits / Sampling** | A probability distribution over the next tokens, from which the emitted token is drawn |

## Training Lifecycle

| Stage | Purpose |
| --- | --- |
| **Pre-training** | Self-supervised next-token prediction on broad corpora — builds general competence |
| **Fine-tuning** | Adapt to a domain or task on a smaller curated dataset |
| **Instruction Tuning** | Teach the model to follow natural-language instructions |
| **RLHF / RLAIF** | Align outputs with human (or AI) preferences via reinforcement learning |
| **Distillation** | Compress a large model's behavior into a smaller, cheaper one |

## Inference Controls

| Parameter | Effect |
| --- | --- |
| **Temperature** | Higher = more random/creative; lower = more deterministic |
| **Top-p / Top-k** | Restrict sampling to the most probable tokens (nucleus / top-k) |
| **Max Tokens** | Caps the length of the generated output |
| **System Prompt** | Persistent instruction shaping role, tone, and constraints |
| **Stop Sequences** | Strings that halt generation |

## Usage Techniques

| Technique | Description |
| --- | --- |
| **Prompt Engineering** | Crafting input to elicit desired behavior |
| **Zero-Shot / Few-Shot** | Solving a task with no examples, or with a handful supplied in the prompt rather than by retraining — also called in-context learning |
| **Chain-of-Thought (CoT)** | Prompting step-by-step reasoning to improve accuracy on complex tasks |
| **RAG** | Retrieval-Augmented Generation — inject relevant external documents into context |
| **Function / Tool Calling** | Model emits structured calls the host executes and feeds back |
| **Structured Output** | Constrain responses to JSON/schema for reliable downstream parsing |

> Two failure modes to design around: **hallucination** (confident but false output) and
> **context limits** (truncation and "lost in the middle" degradation on long inputs).
