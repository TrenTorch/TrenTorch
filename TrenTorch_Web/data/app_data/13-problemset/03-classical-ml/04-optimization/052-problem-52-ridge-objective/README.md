---
name: problem-52-ridge-objective
title: 'Ridge Objective'
tags: [problemset, classical-ml, regularization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Optimization'
topic: 'regularization'
hint: 'mean squared residual plus lam times sum of squared weights (bias excluded)'
tools: [NumPy]
---

## Statement

Evaluate the ridge-regression objective: the mean squared prediction error plus $\lambda$ times the squared L2 norm of the weights. The intercept `b` is **not** penalised.

Implement `solve(X, y, w, b, lam)`.

**Returns.** Return a Python float $\;\frac1n\sum_i(x_i^\top w+b-y_i)^2+\lambda\|w\|_2^2$.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0]], [1.0, 2.0], [1.0, 1.0], 0.0, 0.5)
```

Output:

```text
1.5
```

**Example 2**

Input:

```python
solve([[2.0], [4.0]], [1.0, 2.0], [0.5], 0.0, 10.0)
```

Output:

```text
2.5
```

## Theory

### The simple version

Ridge regression fits the data but also pays a price for large weights. The penalty term shrinks the weights toward zero, which tames overfitting when features are many or correlated. The strength $\lambda$ sets the trade-off: $\lambda=0$ is plain least squares.

### The formula

$$J(w,b)=\frac1n\sum_{i=1}^{n}\big(x_i^\top w+b-y_i\big)^2+\lambda\sum_{j}w_j^2$$

### Why it matters

- Ridge regression trades a little extra training error for smaller weights, which usually generalises better.
- The penalty weight $\lambda$ sets the trade-off, and the intercept is left unpenalised.

### How it works

1. Predictions $Xw+b$.
2. Mean squared residual.
3. Add $\lambda\sum w_j^2$.

### Worked example

With $X=I$, $w=(1,1)$, $b=0$ and $y=(1,2)$ the predictions are $(1,1)$, the residuals $(0,-1)$ and the mean squared error $0.5$. The penalty is $0.5\cdot(1+1)=1$, so the objective is 1.5.

## Explanation

The residuals are computed with the bias included, but only `w` enters the penalty: shrinking the intercept would make the model depend on where the target happens to be centred. Note the penalty here is $\lambda\|w\|^2$ with no factor $\tfrac12$.
