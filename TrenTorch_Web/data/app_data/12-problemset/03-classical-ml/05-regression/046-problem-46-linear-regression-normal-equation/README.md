---
name: problem-46-linear-regression-normal-equation
title: 'Linear Regression Normal Equation'
tags: [problemset, classical-ml, linear-regression]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'linear regression'
hint: 'prepend a ones column, then pinv(A.T @ A) @ A.T @ y'
tools: [NumPy]
---

## Statement

Fit ordinary least-squares linear regression **with an intercept** by solving the normal equations. Prepend a column of ones to `X`, then solve $(\tilde X^\top\tilde X)\beta=\tilde X^\top y$.

Implement `solve(X, y)`.

**Returns.** Return a NumPy vector with the intercept first, followed by one coefficient per feature. The Moore-Penrose pseudo-inverse is used, so perfectly collinear features do not crash.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [2.0], [3.0]], [2.0, 4.0, 6.0])
```

Output:

```text
[3.55271e-15, 2.0]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 1.0]], [1.0, 2.0, 3.0, 4.0])
```

Output:

```text
[3.10862e-15, 1.0, 2.0]
```

## Theory

### The simple version

Least squares chooses the coefficients that minimise the total squared prediction error. Setting the gradient to zero gives a linear system, the normal equations, which can be solved directly.

### The formula

With $\tilde X=[\mathbf 1\;X]$:

$$\tilde X^\top\tilde X\,\beta=\tilde X^\top y\;\Longrightarrow\;\beta=(\tilde X^\top\tilde X)^{+}\tilde X^\top y$$

## Explanation

The column of ones makes the first coefficient the intercept. Using the pseudo-inverse $(\cdot)^+$ instead of a plain inverse gives the minimum-norm solution when $\tilde X^\top\tilde X$ is singular. Forming $\tilde X^\top\tilde X$ squares the condition number, so for badly conditioned data a QR or SVD solver (`np.linalg.lstsq`) is more accurate.
