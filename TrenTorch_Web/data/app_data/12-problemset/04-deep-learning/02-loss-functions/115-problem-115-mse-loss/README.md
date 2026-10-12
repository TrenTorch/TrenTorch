---
name: problem-115-mse-loss
title: 'MSE Loss'
tags: [problemset, dl-core, loss-functions]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Loss Functions'
topic: 'loss functions'
hint: 'mean of (y - pred) squared'
tools: [NumPy]
---

## Statement

Compute the mean squared error between targets `y` and predictions `pred`.

Implement `solve(y,pred)`.

**Returns.** Return a non-negative float.

### Examples

**Example 1**

Input:

```python
solve([1, 3], [2, 2])
```

Output:

```text
1.0
```

**Example 2**

Input:

```python
solve([2.0, 2.0], [2.0, 2.0])
```

Output:

```text
0.0
```

## Theory

### The simple version

MSE is the standard regression loss: the average of the squared differences between prediction and truth. Squaring punishes big mistakes heavily and gives a smooth, convex objective whose gradient is simply proportional to the error.

### The formula

$$\text{MSE}=\frac1n\sum_i(\hat y_i-y_i)^2,\qquad \frac{\partial\,\text{MSE}}{\partial\hat y_i}=\frac2n(\hat y_i-y_i)$$

### Why it matters

- MSE is the standard regression loss, smooth and easy to differentiate.
- Squaring punishes large errors more.

### How it works

1. Subtract.
2. Square.
3. Average.

### Worked example

Errors $-1$ and $1$ square to $1$ and $1$, so the mean is 1.0.

## Explanation

In the first example the errors are $+1$ and $-1$, whose squares are both $1$, so the mean is $1$. A perfect prediction gives $0$.
