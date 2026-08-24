---
type: Guide
title: Deep Learning
description: How layered neural networks learn representations from raw data, and the training machinery and architectures behind them.
tags: [ai, deep-learning, neural-networks, training]
---

# Deep Learning

**Deep Learning** uses neural networks with many layers that learn hierarchical representations
directly from raw data, removing the need for hand-crafted features.

It is the layer between [machine learning](01-machine-learning.md) and the foundation models that
[large language models](03-llm.md) are built from: the paradigms, the loss-minimizing training loop,
and the generalization concerns described in the machine learning guide all still apply here, and the
transformer that this guide introduces is the architecture an LLM is a scaled-up instance of. Papers
and books behind this material are collected under [References](00-ai.md#references).

## Why Depth Matters

Classical machine learning asks an engineer to decide, in advance, which properties of the input the
model should see — the edges in an image, the word counts in a document, the ratios in a table. That
step is where most of the domain knowledge, and most of the effort, goes.

Depth replaces it. Each layer transforms the output of the one below, so a stack of layers can learn a
progression of representations: early layers pick up local, generic structure, and later layers compose
those into the abstractions the task actually needs. Nothing in that progression is specified by hand;
it falls out of minimizing the loss. That is the trade deep learning makes — far less feature
engineering, in exchange for far more data, compute, and opacity about what the intermediate layers
have decided to represent.

Depth only buys this if the layers are separated by non-linearities. Composing linear maps yields
another linear map, so a network of purely linear layers, however tall, is equivalent to a single one
and can represent nothing more. The activation function is what keeps each added layer worth having.

## Core Concepts

| Concept | Definition |
| --- | --- |
| **Neuron** | A weighted sum of inputs passed through a non-linear activation |
| **Layer** | A group of neurons; stacking them is what makes a network deep, and depth is what buys hierarchical features |
| **Activation Function** | The non-linearity — ReLU, GELU, sigmoid — without which any stack of layers collapses into a single linear map |
| **Backpropagation** | The algorithm that computes the gradient of the error with respect to each weight, by applying the chain rule backward through the network |
| **Gradient Descent** | Iterative weight update in the direction that reduces the error, with SGD and Adam the usual variants |
| **Loss Function** | The scalar measure of prediction error that training minimizes |
| **Regularization** | Techniques such as dropout and weight decay that curb overfitting |
| **Embedding** | A dense vector representation that places semantically similar inputs close together in geometric space |

## The Training Loop

Training is the repeated application of four steps to batches of examples. Understanding them as one
cycle explains most of what goes wrong in practice, because a failure in any step shows up as a model
that will not improve.

```mermaid
graph LR
  F[Forward pass] --> L[Loss]
  L --> B[Backpropagation]
  B --> U[Weight update]
  U --> F
```

1. **Forward pass.** Input flows through the layers and the network emits a prediction.
2. **Loss.** The loss function reduces the gap between that prediction and the target to a single
   number, which is the only definition of "wrong" the network has. Choosing it is a modeling decision,
   not a detail.
3. **Backpropagation.** The chain rule is applied backward through the network to obtain the gradient
   of that loss with respect to every weight — the direction and magnitude by which each weight is
   responsible for the error.
4. **Weight update.** Gradient descent moves each weight a small step against its gradient. The step
   size is the learning rate: too large and the optimization diverges, too small and it crawls. Adam
   and the other adaptive variants of SGD exist to make this step less sensitive to that choice.

Because the loop is driven entirely by training error, it will happily keep reducing that error by
absorbing noise specific to the training set — the overfitting described in the
[machine learning guide](01-machine-learning.md). Regularization is the counterweight: dropout removes
random neurons during training so no single path can be relied on, and weight decay penalizes large
weights so the fitted function stays smoother than the data strictly permits.

## Embeddings

An embedding is what a trained network's internal representation looks like from the outside: a dense
vector in which position encodes meaning, so that inputs the model treats as similar end up near each
other geometrically. This is why nearest-neighbor search over embeddings is a usable proxy for semantic
similarity, and it is the property that retrieval systems and vector databases are built on.

## Architectures

An architecture is a prior about the structure of the data — which inputs are related to which, and
how information should be allowed to flow. Picking one that matches the data is worth more than depth
for its own sake.

| Architecture | Best suited for |
| --- | --- |
| **MLP** (feed-forward) | Tabular data and general function approximation |
| **CNN** (convolutional) | Images and spatial data |
| **RNN / LSTM** | Sequences; largely superseded by transformers for language |
| **Transformer** | Sequences via attention, and the foundation of modern LLMs |
| **Diffusion** | Generative images and audio, by iterative denoising |

The **MLP** assumes nothing about how its inputs relate, which makes it a general approximator and the
default where no structure is known. A **CNN** assumes that meaning is local and position-independent,
which is what makes it efficient on images. **RNNs** and **LSTMs** assume order, processing a sequence
one element at a time — the assumption is right, but the sequential dependency limits how much of the
work can be parallelized, which is a large part of why transformers displaced them for language. The
**transformer** keeps the sequence assumption while letting attention relate any two positions
directly, and scaling it is what produced [large language models](03-llm.md). **Diffusion** models
invert a noising process instead of predicting a next element, generating images and audio by
denoising step by step.
