---
name: research-layernorm-per-example-stats
title: 'Layer Normalization: Per-Example Statistics'
tags: [research-papers, normalization, layernorm]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The key difference from batch norm is which axis the statistics come from. Layer norm computes one mean and variance per example, across its features, so the result never depends on batch size.

### From theory to code

Implement `per_example_stats(x)`, which returns the mean and variance of each example's features as two arrays of length `N`.

### Constraints

- `x` has shape `(N, D)`.
- Variance is biased (divides by `D`).

### Hints

<details>
<summary>Hint 1</summary>

Reduce over the last axis: `mean(axis=-1)` and `var(axis=-1)`.

</details>

## Theory

### The simple version

Batch norm reduces over the batch axis, so each feature has its own statistic. Layer norm reduces over the feature axis, so each example has its own statistic, which is why it works at batch size 1.

### The formula

$$\mu_n = \frac{1}{D}\sum_j x_{nj}, \qquad \sigma_n^2 = \frac{1}{D}\sum_j (x_{nj} - \mu_n)^2$$

### How NumPy/PyTorch actually implements this

`x.mean(-1)` and `x.var(-1)` in NumPy, or `torch.var_mean(x, dim=-1)`, compute these per-row statistics.

## Explanation

Each returned value is a statistic for one row. These are the same quantities `normalize_last_axis` uses internally.
