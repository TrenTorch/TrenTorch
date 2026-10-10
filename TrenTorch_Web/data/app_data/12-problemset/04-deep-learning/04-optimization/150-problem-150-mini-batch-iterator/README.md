---
name: problem-150-mini-batch-iterator
title: 'Mini-Batch Iterator'
tags: [problemset, dl-training-theory, batch-dynamics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'batch dynamics'
hint: 'permute the indices once, then slice them in chunks of batch_size'
tools: [NumPy]
---

## Statement

Split a dataset into shuffled mini-batches. Shuffle the row indices once with `np.random.default_rng(seed).shuffle`, then cut the shuffled order into consecutive chunks of at most `batch_size`; the last batch may be smaller.

Implement `solve(X, y, batch_size, seed=0)`.

**Returns.** Return a list of `(X_batch, y_batch)` tuples, each a pair of Python lists, covering every example exactly once.

### Examples

**Example 1**

Input:

```python
solve([[0], [1], [2], [3], [4]], [0, 1, 2, 3, 4], 2, seed=0)
```

Output:

```text
[([[2], [4]], [2, 4]), ([[3], [0]], [3, 0]), ([[1]], [1])]
```

**Example 2**

Input:

```python
solve([[1], [2], [3], [4]], [10, 20, 30, 40], 4, seed=1)
```

Output:

```text
[([[1], [2], [3], [4]], [10, 20, 30, 40])]
```

## Theory

### The simple version

Computing the gradient on the whole dataset is slow, and using one example at a time is noisy. Mini-batches are the compromise: shuffle the data, take it a few dozen or hundred rows at a time, and update after each batch. One pass through all batches is an epoch.

### The recipe

1. Shuffle the indices $0,\dots,n-1$ once.
2. Take consecutive slices of length `batch_size`.
3. Keep the final short slice rather than dropping it.

### Why it matters

- Mini-batches are the compromise between a slow full-batch gradient and a noisy single-sample one.
- Shuffling once per epoch stops the order of the data from biasing training.

### How it works

1. Shuffle the indices with the seed.
2. Cut into chunks of `batch_size`.
3. Take features and labels with the same indices.

### Worked example

Five samples with batch size $2$ shuffle to the order $(2,4,3,0,1)$, giving batches $(2,4)$, $(3,0)$ and the leftover $(1)$ with their labels: [([[2], [4]], [2, 4]), ([[3], [0]], [3, 0]), ([[1]], [1])].

## Explanation

Features and labels are indexed with the _same_ shuffled indices, so each label stays attached to its row. With `batch_size` at least $n$ the whole shuffled dataset forms a single batch (second example).
