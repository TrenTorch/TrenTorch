---
name: problem-58-knn-regression
title: "KNN Regression"
tags: [problemset, classical-ml, knn]
difficulty: Advanced
kind: problemset
relatedModule: "part-classical-linear|Classification"
topic: "knn"
hint: "average the neighbor targets"
tools: [NumPy]
---

# KNN Regression

## Statement

Implement `solve(X, y, q, k)`. Predict a numeric target by averaging the targets of the k nearest training rows.

## Theory

K-nearest-neighbor regression selects rows with smallest Euclidean distances and returns their target mean.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.

## Examples

**Example 1**

Input:
```python
solve([[0.0], [2.0]], [0.0, 10.0], [0.2], 1)
```

Output:
```text
0.0
```

**Example 2**

Input:
```python
solve([[0.0], [2.0], [4.0]], [0.0, 10.0, 20.0], [3.0], 2)
```

Output:
```text
15.0
```
