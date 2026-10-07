---
name: batchnorm-inference-company-215
title: 'batchnorm-inference — Databricks case'
tags: [problemset, dl-core, normalization, databricks]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'Databricks'
hint: 'gamma * (x - mean) / sqrt(var + eps) + beta'
tools: [NumPy]
---

## Statement

Databricks-inspired batch inference service has a trained normalization layer whose running statistics are already fixed. You need to apply the inference-time BatchNorm transformation consistently so predictions do not change merely because request batches have different sizes.

Apply the inference-time batch-normalisation transform with **fixed** running statistics: $y=\gamma\,\dfrac{x-\mu}{\sqrt{\sigma^2+\varepsilon}}+\beta$ with `eps` defaulting to $10^{-5}$. All of `mean`, `var`, `gamma` and `beta` may be scalars or arrays that broadcast against `x`.

Implement `solve(x, mean, var, gamma, beta, eps=1e-5)`.

**Returns.** Return a float NumPy array with the shape of `x`.

### Examples

**Example 1**

Input:

```python
solve([1, 2, 3], [2], [0.25], [2], [0.5])
```

Output:

```text
[-3.49992, 0.5, 4.49992]
```

**Example 2**

Input:

```python
solve([4.0], 2.0, 4.0, 1.0, 0.0, eps=0.0)
```

Output:

```text
[1.0]
```

## Theory

### The simple version

During training batch norm uses the statistics of the current mini-batch. At inference those would make a prediction depend on whichever other requests share the batch, so the layer instead uses running averages of the mean and variance collected during training. The transformation then becomes a fixed per-feature scale and shift.

### The formula

$$y=\gamma\,\frac{x-\mu_{\text{run}}}{\sqrt{\sigma^2_{\text{run}}+\varepsilon}}+\beta$$

## Explanation

The same input always gives the same output, regardless of batch size or composition. The small $\varepsilon$ prevents division by zero for a feature with (nearly) zero variance; with $\varepsilon=0$ the second example is exactly $(4-2)/2=1$.
