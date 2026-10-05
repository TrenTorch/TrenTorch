---
name: problem-52-ridge-objective
title: 'Ridge Objective'
tags: [problemset, classical-ml, regularization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Optimization'
topic: 'regularization'
hint: 'add lambda times squared weight norm'
tools: [NumPy]
---

## Statement

Implement `solve(X, y, w, b, lam)`. Compute mean squared prediction error plus lambda times the squared L2 norm of weights. The intercept is not penalized.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [2.0]], [2.0, 4.0], [1.0], 1.0, 0.5)
```

Output:

```text
1.0
```

**Example 2**

Input:

```python
solve([[1.0], [2.0]], [2.0, 4.0], [1.0], 1.0, 0.0)
```

Output:

```text
0.5
```

## Theory

The ridge objective combines MSE with an L2 penalty on coefficients; the intercept term is excluded from regularization.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
