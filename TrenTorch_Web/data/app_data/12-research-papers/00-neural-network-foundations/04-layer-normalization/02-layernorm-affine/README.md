---
name: research-layernorm-affine
title: 'Layer Normalization: The Learned Scale and Shift'
tags: [research-papers, normalization, layernorm]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Plain normalization removes information the layer may need, such as an overall scale or offset per feature. Layer norm therefore adds a learned gain and bias, as in the paper, so the layer can choose how much normalization to keep.

### From theory to code

Implement `layernorm(x, gamma, beta, eps)`, which normalizes each example over its features and then applies the per-feature `gamma` and `beta`.

### Constraints

- `gamma` and `beta` have shape `(D,)`.

### Hints

<details>
<summary>Hint 1</summary>

Reuse the last-axis normalization from `normalize_last_axis` and multiply by `gamma`, then add `beta`.

</details>

## Theory

### The simple version

Normalization makes the features comparable; `gamma` and `beta` restore a learned scale and offset so the layer is not forced into zero mean and unit variance.

### The formula

$$y_j = \gamma_j \frac{x_j - \mu}{\sqrt{\sigma^2 + \epsilon}} + \beta_j$$

### How NumPy/PyTorch actually implements this

`torch.nn.LayerNorm(D)` stores `weight` (gamma) and `bias` (beta) and applies exactly this rule.

## Explanation

The per-feature `gamma` and `beta` broadcast across the leading axes. This is the form used in every transformer block.
