---
type: Guide
title: Artificial Intelligence
description: The layered AI stack — machine learning, deep learning, foundation models, LLMs, agents, and multi-agent systems.
tags: [ai, machine-learning, llm, agentic-ai]
---

# Artificial Intelligence

**Artificial Intelligence** is the engineering discipline of building systems that perform tasks normally requiring human cognition — perception, reasoning, learning, planning, and language. It is not one technique but a nested stack, each layer built on the one below. This overview maps the stack and holds the vocabulary and references the whole chapter shares; each layer is documented in its own guide.

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Machine Learning Foundations](01-machine-learning.md)** | The learning paradigms, and the vocabulary of model, training, inference, and generalization that every layer above inherits |
| **[Deep Learning](02-deep-learning.md)** | Why depth removes hand-crafted features, the concepts and training loop behind a neural network, and the architectures worth knowing |
| **[Large Language Models (LLM)](03-llm.md)** | Transformer mechanics, the training lifecycle from pre-training to alignment, the inference controls you tune at call time, and techniques such as RAG and tool calling |
| **[Agentic AI](04-agents.md)** | The anatomy of an agent, the established agent patterns, the boundaries autonomy has to respect, and multi-agent topologies |

## The Layered Map

| Layer | What it is | Defining idea |
| --- | --- | --- |
| **Artificial Intelligence** | Any system exhibiting intelligent behavior | Goal-directed problem solving |
| **Machine Learning (ML)** | Systems that improve from data rather than explicit rules | Learn a function from examples |
| **Deep Learning (DL)** | ML with many-layered neural networks | Learn representations automatically |
| **Foundation Models** | Large models pre-trained on broad data, adaptable to many tasks | Transfer learning at scale |
| **Large Language Models (LLM)** | Foundation models for text and sequence prediction | Next-token prediction over language |
| **Agentic AI** | An LLM that plans, acts via tools, and observes results in a loop | Autonomy through the perceive-decide-act cycle |
| **Multi-Agent Systems (MAS)** | Multiple coordinating agents solving a shared goal | Division of labor and communication |

```mermaid
graph TD
  AI[Artificial Intelligence]
  ML[Machine Learning]
  DL[Deep Learning]
  FM[Foundation Models]
  LLM[Large Language Models]
  AG[Agentic AI]
  MAS[Multi-Agent Systems]
  AI --> ML --> DL --> FM --> LLM --> AG --> MAS
```

## Glossary

Terms that cut across the whole chapter. Vocabulary belonging to one layer is defined in that layer's guide.

AGI
: Artificial General Intelligence — the hypothetical point at which one system matches human breadth across arbitrary tasks

Alignment
: Making a model's behavior match the intent and values of the people deploying it

Hallucination
: Fluent, confident output that is not true, produced with no signal distinguishing it from output that is

MCP
: Model Context Protocol — an open standard for connecting models to tools and data sources

MoE
: Mixture of Experts — routing each token through a subset of the network so capacity can grow faster than the cost of running it

Quantization
: Reducing the numeric precision of weights to shrink a model and speed it up, at some cost in accuracy

Vector Database
: A store optimized for nearest-neighbor search over dense vectors, which is what makes retrieval practical at scale

## Perspectives

| Lens | View |
| --- | --- |
| **Capability** | LLMs are pattern predictors, not reasoners with grounded truth — treat output as a draft to verify, not an oracle |
| **Engineering** | Favor deterministic workflows, and introduce autonomy only where the task genuinely demands it. Measure, log, and evaluate as you would any other system |
| **Reliability** | Non-determinism, hallucination, and prompt sensitivity make evaluation a first-class engineering concern rather than a research one |
| **Economics** | Cost scales with tokens and model size, so caching, smaller models, and tight context control are the core optimizations |
| **Safety and Ethics** | Bias, privacy, misuse, and alignment risks all grow with autonomy — keep a human in the loop for consequential actions |
| **Scaling** | The Bitter Lesson: general methods that leverage compute and data tend to win over hand-crafted, domain-specific cleverness |
| **Human Role** | The model accelerates; the human directs, judges, and owns the outcome |

## References

The whole chapter draws on this list. The guides in this chapter link here rather than repeating it.

### Foundational Papers

| Title | URL |
| --- | --- |
| **Deep Learning** (LeCun, Bengio, Hinton, *Nature* 2015) | [nature.com/articles/nature14539](https://www.nature.com/articles/nature14539) |
| **Attention Is All You Need** (the transformer) | [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762) |
| **BERT** | [arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805) |
| **Language Models are Few-Shot Learners** (GPT-3) | [arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165) |
| **Chain-of-Thought Prompting** | [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903) |
| **Training Language Models to Follow Instructions with Human Feedback** (InstructGPT, RLHF) | [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155) |
| **ReAct: Synergizing Reasoning and Acting** | [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) |
| **Toolformer: Language Models Can Teach Themselves to Use Tools** | [arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761) |
| **Retrieval-Augmented Generation** | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401) |

### Guides and Documentation

| Resource | URL |
| --- | --- |
| **The Bitter Lesson** (Rich Sutton) | [incompleteideas.net/IncIdeas/BitterLesson.html](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) |
| **Deep Learning Book** (Goodfellow, Bengio, Courville) | [deeplearningbook.org](https://www.deeplearningbook.org/) |
| **Building Effective Agents** (Anthropic) | [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents) |
| **Anthropic Documentation** | [docs.claude.com](https://docs.claude.com/) |
| **OpenAI Documentation** | [platform.openai.com/docs](https://platform.openai.com/docs) |
| **Hugging Face Documentation** | [huggingface.co/docs](https://huggingface.co/docs) |
| **Prompt Engineering Guide** (DAIR.AI) | [promptingguide.ai](https://www.promptingguide.ai/) |
| **Model Context Protocol** | [modelcontextprotocol.io](https://modelcontextprotocol.io/) |
