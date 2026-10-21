---
type: Guide
title: Deep Learning
description: How layered neural networks learn representations from raw data, and the training machinery and architectures behind them.
tags: [ai, deep-learning, neural-networks, training]
---

**Deep Learning** uses neural networks with many layers. They learn hierarchical representations directly from raw data, so no hand-crafted features are needed.

It sits between [machine learning](01-machine-learning.md) and the foundation models that [large language models](03-llm.md) are built from:

- The paradigms, the loss-minimizing training loop and the generalization concerns of machine learning all still apply.
- The transformer introduced here is the architecture an LLM scales up.

Papers and books behind this material are under [References](index.md#references).

## Why Depth Matters

Classical machine learning asks an engineer to decide in advance which properties of the input the model should see — the edges in an image, the word counts in a document, the ratios in a table. Most of the domain knowledge, and most of the effort, goes into that step.

Depth replaces it. Each layer transforms the output of the layer below, so a stack of layers learns a progression of representations:

- Early layers pick up local, generic structure.
- Later layers compose it into the abstractions the task needs.

Nobody specifies this progression by hand; it comes out of minimizing the loss. That is the trade deep learning makes: far less feature engineering, in exchange for far more data, far more compute, and little insight into what the intermediate layers represent.

Depth only helps if non-linearities separate the layers. Composing linear maps gives another linear map, so a network of purely linear layers, however tall, equals a single layer. The activation function is what makes each added layer worth having.

## Core Concepts

Neuron
: A weighted sum of inputs passed through a non-linear activation

Layer
: A group of neurons; stacking them makes a network deep, and depth is what yields hierarchical features

Activation Function
: The non-linearity — ReLU, GELU, sigmoid — without which any stack of layers collapses into a single linear map

Backpropagation
: The algorithm that computes the gradient of the error with respect to each weight, by applying the chain rule backward through the network

Gradient Descent
: Iterative weight update in the direction that reduces the error; SGD and Adam are the usual variants

Loss Function
: The scalar measure of prediction error that training minimizes

Regularization
: Techniques such as dropout and weight decay that curb overfitting

Embedding
: A dense vector representation that places semantically similar inputs close together in geometric space

## The Training Loop

Training repeats four steps over batches of examples. A failure in any step shows up the same way — a model that will not improve — so seeing them as one cycle explains most practical problems.

```mermaid
graph LR
  F[Forward pass] --> L[Loss]
  L --> B[Backpropagation]
  B --> U[Weight update]
  U --> F
```

1. **Forward pass.** Input flows through the layers, and the network emits a prediction.
2. **Loss.** The loss function reduces the gap between prediction and target to one number. That number is the network's only definition of "wrong", so choosing the loss is a modeling decision, not a detail.
3. **Backpropagation.** The chain rule, applied backward through the network, gives the gradient of the loss with respect to every weight — how much, and in which direction, each weight is responsible for the error.
4. **Weight update.** Gradient descent moves each weight a small step against its gradient. The step size is the learning rate: too large and the optimization diverges, too small and it crawls. Adam and the other adaptive variants of SGD make this step less sensitive to that choice.

The loop is driven only by training error. So it will keep reducing that error by absorbing noise specific to the training set — the overfitting described in the [machine learning guide](01-machine-learning.md). Regularization is the counterweight:

- **Dropout** removes random neurons during training, so the network cannot rely on any single path.
- **Weight decay** penalizes large weights, so the fitted function stays smoother than the data strictly allows.

## Embeddings

An embedding is a trained network's internal representation seen from the outside: a dense vector where position encodes meaning, so inputs the model treats as similar end up near each other. This is why nearest-neighbor search over embeddings works as a proxy for semantic similarity. Retrieval systems and vector databases are built on this property.

## Architectures

An architecture is a prior about the structure of the data: which inputs relate to which, and how information may flow. Choosing one that matches the data is worth more than depth for its own sake.

| Architecture | Best suited for |
| --- | --- |
| **MLP** (feed-forward) | Tabular data and general function approximation |
| **CNN** (convolutional) | Images and spatial data |
| **RNN / LSTM** | Sequences; largely superseded by transformers for language |
| **Transformer** | Sequences via attention, and the foundation of modern LLMs |
| **Diffusion** | Generative images and audio, by iterative denoising |

What each one assumes about the data:

- **MLP** — nothing about how inputs relate. This makes it a general approximator and the default when no structure is known.
- **CNN** — meaning is local and position-independent. This makes it efficient on images.
- **RNN / LSTM** — order. They process a sequence one element at a time. The assumption is right, but the sequential dependency limits parallel work, which is a large part of why transformers replaced them for language.
- **Transformer** — order too, but attention relates any two positions directly. Scaling it produced [large language models](03-llm.md).
- **Diffusion** — instead of predicting a next element, it inverts a noising process, generating images and audio by denoising step by step.
