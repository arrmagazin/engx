---
type: Guide
title: Machine Learning Foundations
description: The learning paradigms and core concepts — model, training, inference, generalization — that underpin deep learning and LLMs.
tags: [ai, machine-learning, training, supervised-learning]
---

# Machine Learning Foundations

**Machine Learning (ML)** is the branch of AI where behavior is learned from data rather than written
as explicit rules: a model's parameters are fitted to examples until it approximates the target function.

It is the layer below [deep learning](02-deep-learning.md) in the stack described in
[Artificial Intelligence](index.md), and the self-supervised paradigm is the objective that
[Large Language Models](03-llm.md) are trained on. External reading for this chapter is collected
under [References](index.md#references).

## Learning Paradigms

| Paradigm | Description |
| --- | --- |
| **Supervised** | Learn from labeled pairs (input → known output); used for classification and regression |
| **Unsupervised** | Find structure in unlabeled data (clustering, dimensionality reduction) |
| **Self-Supervised** | Generate labels from the data itself (e.g. predict the next/masked token) — the engine behind LLMs |
| **Reinforcement Learning (RL)** | Learn a policy by maximizing cumulative reward through trial and interaction |

## Core Concepts

Model
: A parameterized function whose weights are fitted to data

Training
: Optimizing weights to minimize a loss function (typically by gradient descent)

Inference
: Running a trained model to produce predictions on new input

Generalization
: Performance on data the model was not trained on

Underfitting
: A model too simple to capture the pattern in its training data, so it scores poorly on both training and new data

Overfitting
: A model that has absorbed noise specific to its training data, so it scores well in training and poorly on new data

Bias / Variance
: Error from wrong assumptions vs. error from sensitivity to data noise
