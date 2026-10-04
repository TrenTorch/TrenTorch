---
name: problem-57-knn-classification
title: "KNN Classification"
tags: [problemset, classical-ml, knn]
difficulty: Advanced
kind: problemset
relatedModule: "part-classical-linear|Classification"
topic: "knn"
hint: "use squared Euclidean distance and deterministic tie-breaking"
tools: [NumPy]
---

# KNN Classification

## Statement

Implement `solve(X, labels, q, k)`. Predict a query class by majority vote among the k nearest training rows. Ties follow NumPy’s sorted class order.

## Theory

Euclidean nearest neighbors are selected by squared distance; the most frequent neighbor label is returned.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.

## Examples

**Example 1**

Input:
```python
solve([[0.0], [2.0]], [0, 1], [0.2], 1)
```

Output:
```text
0
```

**Example 2**

Input:
```python
solve([[0.0], [2.0], [4.0]], [0, 1, 1], [3.0], 3)
```

Output:
```text
1
```
