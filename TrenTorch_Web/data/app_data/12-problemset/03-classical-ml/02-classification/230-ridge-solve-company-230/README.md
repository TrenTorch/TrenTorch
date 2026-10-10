---
name: ridge-solve-company-230
title: 'ridge-solve — Discord case'
tags: [problemset, classical-ml, regularization, discord]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Discord'
hint: 'np.linalg.solve(X.T @ X + lam * I, X.T @ y)'
tools: [NumPy]
---

## Statement

Discord-inspired abuse-detection experiment has correlated features that make an ordinary least-squares solution unstable. You need to compute the ridge-regression solution with the supplied regularization strength so the team has a stable baseline.

Solve the ridge-regression problem without an intercept: $\hat w=(X^\top X+\lambda I)^{-1}X^\top y$, computed with a linear solve rather than an explicit inverse.

Implement `solve(X, y, lam)`.

**Returns.** Return the coefficient vector (one entry per column of `X`). `lam` must be non-negative.

Solve the ridge-regression problem without an intercept: $\hat w=(X^\top X+\lambda I)^{-1}X^\top y$, computed with a linear solve rather than an explicit inverse.

Implement `solve(X, y, lam)`.

**Returns.** Return the coefficient vector (one entry per column of `X`). `lam` must be non-negative.

### Examples

**Example 1**

Input:

```python
solve([[1, 0], [0, 1]], [1, 2], 1)
```

Output:

```text
[0.5, 1.0]
```

**Example 2**

Input:

```python
solve([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]], [1.0, 2.0, 3.0], 0.1)
```

Output:

```text
[0.498221, 0.498221]
```

## Theory

### The simple version

When features are strongly correlated, ordinary least squares can produce huge coefficients of opposite sign that cancel out and are extremely sensitive to noise. Ridge regression adds a penalty on the size of the coefficients, which makes the problem well-conditioned and the solution stable.

### The formula

$$\hat w=\arg\min_w\|y-Xw\|^2+\lambda\|w\|^2=(X^\top X+\lambda I)^{-1}X^\top y$$

### Why it matters

- With correlated features, ordinary least squares gives huge, unstable coefficients.
- Adding $\lambda$ to the diagonal makes the system invertible and shrinks the solution.

### How it works

1. Form $X^\top X+\lambda I$.
2. Form $X^\top y$.
3. Solve the linear system (no explicit inverse).

### Worked example

With $X=I$ and $\lambda=1$ the system is $(I+I)w=y$, i.e. $2w=(1,2)$, so $w=[0.5, 1.0]$. Without regularisation it would be $(1,2)$.

## Explanation

Adding $\lambda$ to the diagonal makes $X^\top X+\lambda I$ invertible even when $X^\top X$ is singular (second example, two identical columns, where plain least squares has no unique solution). In the first example the unregularised answer $(1,2)$ is shrunk to $(0.5,1.0)$.
