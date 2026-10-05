---
name: problem-46-linear-regression-normal-equation
title: 'Linear Regression Normal Equation'
tags: [problemset, classical-ml, linear-regression]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'linear regression'
hint: 'augment X with a column of ones and solve the system'
tools: [NumPy]
---

## Statement

Implement `solve(X, y)`. Fit ordinary least-squares linear regression with an intercept by solving the normal equations. The returned vector contains the intercept first, followed by feature coefficients.

### Examples

**Example 1**

Input:

```python
solve([[0.0], [1.0], [2.0]], [1.0, 3.0, 5.0])
```

Output:

```text
[1.0000000000000022, 1.999999999999998]
```

**Example 2**

Input:

```python
solve([[1.0,0.0],[0.0,1.0],[1.0,1.0]], [3.0,4.0,6.0])
```

Output:

```text
[1.000000000000023, 1.9999999999999867, 2.999999999999985]
```

## Theory

With an intercept-augmented design matrix A, the least-squares coefficient vector is (AᵀA)⁺Aᵀy.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
