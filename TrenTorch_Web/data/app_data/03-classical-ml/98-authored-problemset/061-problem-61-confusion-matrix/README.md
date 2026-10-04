---
name: problem-61-confusion-matrix
title: "Confusion Matrix"
tags: [problemset, classical-ml, metrics]
difficulty: Beginner
kind: problemset
relatedModule: "part-classical-unsupervised|Metrics & Evaluation"
topic: "metrics"
hint: "count four outcome types"
tools: [NumPy]
---

# Confusion Matrix

## Statement

Implement `solve(y, pred)`. Build a 2×2 confusion matrix with rows as true class [0,1] and columns as predicted class [0,1].

## Theory

The matrix cells are true negatives, false positives, false negatives, and true positives in row-major order.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.

## Examples

**Example 1**

Input:
```python
solve([0,0,1,1], [0,1,0,1])
```

Output:
```text
[[1, 1], [1, 1]]
```

**Example 2**

Input:
```python
solve([1,1,0], [1,0,0])
```

Output:
```text
[[1, 0], [1, 1]]
```
