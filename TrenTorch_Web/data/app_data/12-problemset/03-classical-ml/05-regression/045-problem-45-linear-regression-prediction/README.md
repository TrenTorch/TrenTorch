---
name: problem-45-linear-regression-prediction
title: 'Linear Regression Prediction'
tags: [problemset, classical-ml, linear-regression]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'linear regression'
hint: 'compute Xw+b'
tools: [NumPy]
---

## Statement

Implement `solve(X, w, b)`. Predict numeric targets for rows of X using coefficient vector w and intercept b.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 1.0], 0.0)
```

Output:

```text
[3.0, 7.0]
```

**Example 2**

Input:

```python
solve([[2.0, 1.0]], [3.0, -1.0], 4.0)
```

Output:

```text
[9.0]
```

## Theory

For each row xᵢ, the linear prediction is xᵢᵀw+b.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
