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
[Artificial Intelligence](22-ai-overview.md): a transformer is the architecture, an LLM is that
architecture trained at scale, and an [Agent](03-agents.md) is an LLM wrapped in a loop with tools
and memory.

## Core Mechanics

| Concept | Definition |
| --------- | ------------ |
| **Token** | The atomic unit of text (sub-word fragment) the model reads and emits |
| **Tokenizer** | Maps text ↔ tokens (e.g. BPE); affects cost, context limits, and multilingual fairness |
| **Transformer** | Architecture built on stacked self-attention and feed-forward blocks |
| **Attention** | Mechanism letting each token weigh the relevance of every other token |
| **Context Window** | Maximum tokens the model can attend to at once (prompt + output) |
| **Parameters** | The learned weights; scale correlates with capability |
| **Logits / Sampling** | Output is a probability distribution over next tokens, sampled to generate text |

## Training Lifecycle

| Stage | Purpose |
| ------- | --------- |
| **Pre-training** | Self-supervised next-token prediction on broad corpora — builds general competence |
| **Fine-tuning** | Adapt to a domain or task on a smaller curated dataset |
| **Instruction Tuning** | Teach the model to follow natural-language instructions |
| **RLHF / RLAIF** | Align outputs with human (or AI) preferences via reinforcement learning |
| **Distillation** | Compress a large model's behavior into a smaller, cheaper one |

## Inference Controls

| Parameter | Effect |
| ----------- | -------- |
| **Temperature** | Higher = more random/creative; lower = more deterministic |
| **Top-p / Top-k** | Restrict sampling to the most probable tokens (nucleus / top-k) |
| **Max Tokens** | Caps the length of the generated output |
| **System Prompt** | Persistent instruction shaping role, tone, and constraints |
| **Stop Sequences** | Strings that halt generation |

## Usage Techniques

| Technique | Description |
| ----------- | ------------- |
| **Prompt Engineering** | Crafting input to elicit desired behavior |
| **Few-Shot / In-Context Learning** | Providing examples in the prompt instead of retraining |
| **Chain-of-Thought (CoT)** | Prompting step-by-step reasoning to improve accuracy on complex tasks |
| **RAG** | Retrieval-Augmented Generation — inject relevant external documents into context |
| **Function / Tool Calling** | Model emits structured calls the host executes and feeds back |
| **Structured Output** | Constrain responses to JSON/schema for reliable downstream parsing |

> Two failure modes to design around: **hallucination** (confident but false output) and
> **context limits** (truncation and "lost in the middle" degradation on long inputs).

---

## References

| Title | URL |
| --- | --- |
| Attention Is All You Need (Transformer) | <https://arxiv.org/abs/1706.03762> |
| BERT | <https://arxiv.org/abs/1810.04805> |
| Language Models are Few-Shot Learners (GPT-3) | <https://arxiv.org/abs/2005.14165> |
| Chain-of-Thought Prompting | <https://arxiv.org/abs/2201.11903> |
| Training LMs to Follow Instructions with Human Feedback (InstructGPT/RLHF) | <https://arxiv.org/abs/2203.02155> |
| Retrieval-Augmented Generation (RAG) | <https://arxiv.org/abs/2005.11401> |
| Prompt Engineering Guide (DAIR.AI) | <https://www.promptingguide.ai/> |
