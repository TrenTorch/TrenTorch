---
name: problem-51-logistic-gradient
title: 'Logistic Gradient'
tags: [problemset, classical-ml, logistic-regression]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'logistic regression'
hint: 'use p-y as the residual'
tools: [NumPy]
---

## Statement

Implement `solve(X, y, w)`. Compute the logistic-loss gradients with respect to weight vector w and scalar bias for a design matrix X and binary labels y.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [1.0]], [1, 0], [0.0])
```

Output:

```text
([0.0], 0.0)
```

**Example 2**

Input:

```python
solve([[1.0], [2.0]], [1, 1], [0.0])
```

Output:

```text
([-0.75], -0.5)
```

## Theory

For each row, p=σ(Xw); the weight gradient is Xᵀ(p−y)/n and the bias gradient is mean(p−y).

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
