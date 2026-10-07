---
name: problem-123-layer-normalization
title: 'Layer Normalization'
tags: [problemset, dl-core, normalization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'normalization'
hint: 'same as batch norm but with mean/var over axis=1 (keepdims)'
tools: [NumPy]
---

## Statement

Apply layer normalisation to a 2-D batch `X`: for each **row** compute the mean and population variance across its features, normalise with $\sqrt{\text{var}+\varepsilon}$, then apply the per-feature scale `gamma` and shift `beta`. `eps` defaults to $10^{-5}$.

Implement `solve(X, gamma, beta, eps=1e-5)`.

**Returns.** Return a float NumPy array with the shape of `X`.

### Examples

**Example 1**

Input:

```python
solve([[1, 3], [2, 6]], [1, 2], [0, 1], eps=0)
```

Output:

```text
[[-1.0, 3.0], [-1.0, 3.0]]
```

**Example 2**

Input:

```python
solve([[2, 2]], [3, 4], [1, -1])
```

Output:

```text
[[1.0, -1.0]]
```

## Theory

### The simple version

Layer normalisation does what batch normalisation does but across the features of _one sample_ instead of across the batch. That makes it independent of the batch size and works unchanged at training and inference time, which is why transformers use it.

### The formula

$$\hat x_{i}=\frac{x_{i}-\mu_i}{\sqrt{\sigma_i^2+\varepsilon}},\quad \mu_i=\frac1d\sum_jx_{ij},\quad y_{ij}=\gamma_j\hat x_{ij}+\beta_j$$

## Explanation

The only difference from batch norm is the axis: `axis=1` with `keepdims=True` so each row is normalised on its own. The two rows of the first example, $[1,3]$ and $[2,6]$, differ in scale but normalise to the same pattern.
