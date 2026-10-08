---
name: problem-63-k-fold-indices
title: 'K-Fold Indices'
tags: [problemset, classical-ml, cross-validation]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'cross validation'
hint: 'np.array_split(arange(n), k); train is everything outside the fold'
tools: [NumPy]
---

## Statement

Split the indices $0,\dots,n-1$ into `k` consecutive folds whose sizes differ by at most one, and build the train/test index pair for each fold. Fold $i$ is the test set of split $i$ and everything else is its training set. Assume $k\le n$.

Implement `solve(n, k)`.

**Returns.** Return a list of `k` tuples `(train_indices, test_indices)` of NumPy arrays, in fold order. When $n$ is not divisible by $k$ the first $n \bmod k$ folds get one extra index (`np.array_split`).

### Examples

**Example 1**

Input:

```python
solve(6, 3)
```

Output:

```text
[([2, 3, 4, 5], [0, 1]), ([0, 1, 4, 5], [2, 3]), ([0, 1, 2, 3], [4, 5])]
```

**Example 2**

Input:

```python
solve(5, 2)
```

Output:

```text
[([3, 4], [0, 1, 2]), ([0, 1, 2], [3, 4])]
```

## Theory

### The simple version

K-fold cross-validation estimates how well a model generalises by training $k$ times. Each round holds out a different slice of the data for testing and trains on the rest, so every sample is tested exactly once.

### The recipe

Cut the index range into $k$ consecutive, near-equal blocks. For fold $i$: test = block $i$, train = all other blocks concatenated.

### Why it matters

- Cross-validation gives a more reliable performance estimate than one split, because every sample is tested once.
- Equal-size folds keep the estimates comparable.

### How it works

1. Split the indices into $k$ consecutive near-equal blocks.
2. For each block, test on it and train on the rest.

### Worked example

For $n=6$ and $k=3$ the blocks are $(0,1)$, $(2,3)$ and $(4,5)$. Fold 0 tests on $(0,1)$ and trains on $(2,3,4,5)$, and so on, giving [([2, 3, 4, 5], [0, 1]), ([0, 1, 4, 5], [2, 3]), ([0, 1, 2, 3], [4, 5])].

## Explanation

`np.array_split` handles the uneven case for you by giving the leading folds one extra element. The folds are consecutive, not shuffled, so shuffle the data first if its order carries information.
