---
name: problem-45-linear-regression-prediction
title: 'Linear Regression Prediction'
tags: [problemset, classical-ml, linear-regression]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'linear regression'
hint: 'X @ w + b'
tools: [NumPy]
---

## Statement

Compute the predictions of a linear model: $\hat y=Xw+b$, where `X` is an $n\times d$ matrix, `w` a length-$d$ weight vector and `b` a scalar bias.

Implement `solve(X, w, b)`.

**Returns.** Return a NumPy array of $n$ predictions.

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
solve([[1.0], [2.0], [3.0]], [2.0], 1.0)
```

Output:

```text
[3.0, 5.0, 7.0]
```

## Theory

### The simple version

A linear model predicts by multiplying each feature by a weight, adding them up, and adding a constant offset (the bias). Doing this for every row at once is a single matrix-vector product.

### The formula

$$\hat y_i=\sum_{j=1}^{d}X_{ij}w_j+b\quad\Longleftrightarrow\quad \hat y=Xw+b\mathbf 1$$

### Why it matters

- Prediction is the forward pass of linear regression, and the same product reappears in every linear layer of a neural network.
- Doing all rows with one matrix product is much faster than a loop.

### How it works

1. Multiply the feature matrix by the weight vector.
2. Add the bias to every prediction.

### Worked example

For rows $(1,2)$ and $(3,4)$ with weights $(1,1)$ and bias $0$: $1+2=3$ and $3+4=7$, so the predictions are [3.0, 7.0].

## Explanation

The matrix product handles all rows in one vectorised call, and the scalar bias is broadcast to every prediction. The shape of `w` must match the number of columns of `X`.
