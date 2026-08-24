---
type: Guide
title: Machine Learning Foundations
description: The learning paradigms and core concepts — model, training, inference, generalization — that underpin deep learning and LLMs.
tags: [ai, machine-learning, training, supervised-learning]
---

# Machine Learning Foundations

**Machine Learning (ML)** is the branch of AI where behavior is learned from data rather than written
as explicit rules: a model's parameters are fitted to examples until it approximates the target function.

It is the layer below deep learning in the stack described in
[Artificial Intelligence](22-ai-overview.md); the self-supervised paradigm below is the objective that
[Large Language Models](02-llm.md) are trained on.

## Paradigms

| Paradigm | Description |
| ---------- | ------------- |
| **Supervised** | Learn from labeled pairs (input → known output); used for classification and regression |
| **Unsupervised** | Find structure in unlabeled data (clustering, dimensionality reduction) |
| **Self-Supervised** | Generate labels from the data itself (e.g. predict the next/masked token) — the engine behind LLMs |
| **Reinforcement Learning (RL)** | Learn a policy by maximizing cumulative reward through trial and interaction |

## Core Concepts

| Concept | Definition |
| --------- | ------------ |
| **Model** | A parameterized function whose weights are fitted to data |
| **Training** | Optimizing weights to minimize a loss function (typically by gradient descent) |
| **Inference** | Running a trained model to produce predictions on new input |
| **Generalization** | Performance on unseen data, balancing **underfitting** vs. **overfitting** |
| **Bias / Variance** | Error from wrong assumptions vs. error from sensitivity to data noise |

---

## References

| Resource | URL |
| --- | --- |
| Deep Learning Book (Goodfellow, Bengio, Courville) | <https://www.deeplearningbook.org/> |
| Deep Learning (LeCun, Bengio, Hinton, *Nature* 2015) | <https://www.nature.com/articles/nature14539> |
