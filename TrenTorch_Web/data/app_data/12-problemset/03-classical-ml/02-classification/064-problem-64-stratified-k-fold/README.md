---
name: problem-64-stratified-k-fold
title: 'K-Fold Splits (Index-Based)'
tags: [problemset, classical-ml, cross-validation]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'cross validation'
hint: 'array_split the indices; training = setdiff1d(all, fold)'
tools: [NumPy]
---

## Statement

Split the indices $0,\dots,n-1$ into `k` consecutive, near-equal validation folds and return, for each fold, the sorted training indices (all others) and the validation indices. No labels are given, so the split is index-based and does **not** stratify.

Implement `solve(n, k)`.

**Returns.** Return a list of `k` tuples `(train_indices, validation_indices)` of NumPy arrays in fold order. The first $n\bmod k$ folds are one element larger (`np.array_split`).

### Examples

**Example 1**

Input:

```python
solve(5, 3)
```

Output:

```text
[([2, 3, 4], [0, 1]), ([0, 1, 4], [2, 3]), ([0, 1, 2, 3], [4])]
```

**Example 2**

Input:

```python
solve(4, 2)
```

Output:

```text
[([2, 3], [0, 1]), ([0, 1], [2, 3])]
```

## Theory

### The simple version

Cross-validation repeatedly holds out one slice of the data for validation and trains on the remainder. Here the slices are consecutive blocks of indices, and the number of blocks is `k`.

### The recipe

Split $\{0,\dots,n-1\}$ into $k$ consecutive blocks $V_1,\dots,V_k$. The training set for fold $i$ is $\{0,\dots,n-1\}\setminus V_i$.

### Why it matters

- K-fold splitting is the backbone of model selection and hyper-parameter tuning.
- This version works from indices alone and does not use labels.

### How it works

1. Cut the indices into $k$ consecutive blocks (earlier blocks one longer if needed).
2. For each block, validate on it and train on the rest.

### Worked example

For $n=5$, $k=3$ the blocks have sizes $2,2,1$: $(0,1)$, $(2,3)$, $(4)$. Fold 0 validates on $(0,1)$ and trains on $(2,3,4)$, and so on: [([2, 3, 4], [0, 1]), ([0, 1, 4], [2, 3]), ([0, 1, 2, 3], [4])].

## Explanation

The training indices come from a set difference, which also returns them sorted. With $n=5$ and $k=3$ the blocks have sizes $2,2,1$ because the leftover element goes to the earliest folds.
