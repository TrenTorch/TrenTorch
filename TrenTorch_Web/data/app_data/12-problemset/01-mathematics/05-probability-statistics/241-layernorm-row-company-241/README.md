---
name: layernorm-row-company-241
title: 'layernorm-row — Atlassian case'
tags: [problemset, dl-core, normalization, atlassian]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Atlassian'
hint: '(X - mean(axis=-1)) / sqrt(var(axis=-1) + eps), times gamma, plus beta'
tools: [NumPy]
---

## Statement

Atlassian-inspired sequence model normalizes each token representation independently before passing it to the next block. You need to implement row-wise LayerNorm with the supplied scale and bias parameters.

Apply layer normalisation to every row of `X` (the last axis): subtract the row mean, divide by $\sqrt{\text{row variance}+\varepsilon}$ (population variance, `eps` defaults to $10^{-5}$), then scale by `gamma` and shift by `beta`. `gamma` and `beta` may be scalars or arrays that broadcast over the last axis.

Implement `solve(X,gamma,beta,eps=1e-5)`.

**Returns.** Return a float NumPy array with the shape of `X`.

### Examples

**Example 1**

Input:

```python
solve([[1, 2, 3]], 1, 0)
```

Output:

```text
[[-1.224736, 0.0, 1.224736]]
```

**Example 2**

Input:

```python
solve([[1.0, 3.0], [10.0, 30.0]], [1.0, 2.0], [0.0, 1.0], eps=0.0)
```

Output:

```text
[[-1.0, 3.0], [-1.0, 3.0]]
```

## Theory

### The simple version

Layer normalisation rescales each token's feature vector to have mean 0 and variance 1 by itself, independent of the other tokens and of the batch size. That keeps the activations of a deep Transformer in a stable range. The learnable $\gamma,\beta$ then let the network undo the normalisation where it wants to.

### The formula

$$y=\gamma\,\frac{x-\mu}{\sqrt{\sigma^2+\varepsilon}}+\beta,\qquad \mu,\sigma^2\text{ over the features of one row}$$

## Explanation

Rows of very different magnitude, like $(1,3)$ and $(10,30)$ in the second example, normalise to the same pattern $(-1,1)$ before the scale and shift. A constant row has zero variance, and only $\varepsilon$ prevents a division by zero.
