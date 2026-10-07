---
name: problem-122-batch-normalization-forward
title: 'Batch Normalization Forward'
tags: [problemset, dl-core, normalization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'normalization'
hint: '(X - mean(axis=0)) / sqrt(var(axis=0)+eps), times gamma, plus beta'
tools: [NumPy]
---

## Statement

Apply training-mode batch normalisation to a 2-D batch `X` of shape `(batch, features)`: for each feature compute the mean and **population** variance over the batch, normalise with $\sqrt{\text{var}+\varepsilon}$, then apply the per-feature scale `gamma` and shift `beta`. `eps` defaults to $10^{-5}$.

Implement `solve(X, gamma, beta, eps=1e-5)`.

**Returns.** Return a float NumPy array with the shape of `X`.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 4]], [1, 2], [0, 1], eps=0)
```

Output:

```text
[[-1.0, -1.0], [1.0, 3.0]]
```

**Example 2**

Input:

```python
solve([[2], [2]], [3], [4])
```

Output:

```text
[[4.0], [4.0]]
```

## Theory

### The simple version

During training the distribution of each layer's inputs keeps shifting as earlier layers change. Batch normalisation re-centres and re-scales every feature using the statistics of the current mini-batch, then lets the network learn its own preferred scale ($\gamma$) and offset ($\beta$). This stabilises and speeds up training.

### The formula

$$\hat x=\frac{x-\mu_B}{\sqrt{\sigma_B^2+\varepsilon}},\qquad y=\gamma\hat x+\beta$$

## Explanation

Statistics are taken per column (`axis=0`) with `ddof=0`. In the second example the feature is constant, so $\hat x=0$ and the output is just $\beta=4$; the $\varepsilon$ keeps that division defined. At inference time the batch statistics are replaced by running averages, which this problem does not cover.
