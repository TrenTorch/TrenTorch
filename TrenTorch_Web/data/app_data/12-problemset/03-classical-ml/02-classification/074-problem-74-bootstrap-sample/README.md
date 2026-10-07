---
name: problem-74-bootstrap-sample
title: 'Bootstrap Sample'
tags: [problemset, classical-ml-trees-ensembles, bagging]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'bagging'
hint: 'default_rng(seed).integers(0, n, size=n)'
tools: [NumPy]
---

## Statement

Draw a bootstrap sample of indices: `n` indices chosen uniformly **with replacement** from $0,\dots,n-1$, using `np.random.default_rng(seed).integers(0, n, size=n)`.

Implement `solve(n,seed=0)`.

**Returns.** Return an integer NumPy array of length `n`. Indices may repeat and some indices may be missing.

### Examples

**Example 1**

Input:

```python
solve(6, 0)
```

Output:

```text
[5, 3, 3, 1, 1, 0]
```

**Example 2**

Input:

```python
solve(5, 42)
```

Output:

```text
[0, 3, 3, 2, 2]
```

## Theory

### The simple version

Bagging trains each model on a different resample of the data. A bootstrap sample is made by drawing $n$ items **with replacement** from $n$ items: some items appear several times and others not at all. On average about $63.2\%$ of the distinct items are included, and the other $36.8\%$ are left "out of bag".

### Why $63.2\%$

The chance that a given item is never drawn in $n$ tries is $(1-1/n)^n\to e^{-1}\approx0.368$.

## Explanation

The result depends on the generator, so the seed is part of the contract. A new `default_rng(seed)` is created on every call, so the same seed always yields the same sample.
