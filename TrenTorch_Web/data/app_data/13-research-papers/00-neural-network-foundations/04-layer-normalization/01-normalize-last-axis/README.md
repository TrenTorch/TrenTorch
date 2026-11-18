---
name: research-layernorm-normalize
title: 'Layer Normalization: Normalizing Across Features'
tags: [research-papers, normalization, layernorm]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Batch norm needs a batch of examples to compute statistics, which is awkward for sequence models and batch size 1. Layer normalization (Ba, Kiros & Hinton, 2016) computes the statistics across the features of each example instead.

### From theory to code

Implement `normalize_last_axis(x, eps)`, which normalizes each example over its feature dimension.

### Constraints

- Works on any shape `(..., D)`.
- The statistics are per example, not per batch.

### Hints

<details>
<summary>Hint 1</summary>

Use `axis=-1` with `keepdims=True` so each example's mean and variance broadcast back correctly.

</details>

## Theory

### The simple version

Each example is normalized using only its own features, so the result does not depend on the other examples in the batch.

### The formula

$$\mu = \frac{1}{D}\sum_{j} x_j, \quad \sigma^2 = \frac{1}{D}\sum_{j}(x_j - \mu)^2, \quad \hat x_j = \frac{x_j - \mu}{\sqrt{\sigma^2 + \epsilon}}$$

### How NumPy/PyTorch actually implements this

`torch.nn.LayerNorm` computes this per example over its normalized shape, and `torch.nn.functional.layer_norm` is the functional form.

## Explanation

`keepdims=True` keeps the reduced axis so the subtraction broadcasts over features. The same code works for a single example or a batch.
