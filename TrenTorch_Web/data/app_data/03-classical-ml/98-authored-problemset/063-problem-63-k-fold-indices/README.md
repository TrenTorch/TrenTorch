---
name: problem-63-k-fold-indices
title: "K-Fold Indices"
tags: [problemset, classical-ml, cross-validation]
difficulty: Beginner
kind: problemset
relatedModule: "part-classical-linear|Classification"
topic: "cross validation"
hint: "partition indices as evenly as possible"
tools: [NumPy]
---

# K-Fold Indices

## Statement

Implement `solve(n, k)`. Partition indices 0..n−1 into k consecutive folds and return (train_indices, test_indices) for each fold. The folds differ in size by at most one.

## Theory

Each fold is used once as the test set; training indices are the concatenation of all other folds in original index order.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.

## Examples

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
