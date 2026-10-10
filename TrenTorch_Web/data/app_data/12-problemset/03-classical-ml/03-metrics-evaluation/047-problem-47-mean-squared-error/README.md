---
name: problem-47-mean-squared-error
title: 'Mean Squared Error'
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'mean of (pred - true) squared'
tools: [NumPy]
---

## Statement

Compute the mean squared error between aligned arrays of true targets and predictions.

Implement `solve(y_true, y_pred)`.

**Returns.** Return a non-negative Python float, $0$ for a perfect prediction.

### Examples

**Example 1**

Input:

```python
solve([3.0, -0.5, 2.0, 7.0], [2.5, 0.0, 2.0, 8.0])
```

Output:

```text
0.375
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
```

Output:

```text
0.0
```

## Theory

### The simple version

MSE is the average of the squared errors. Squaring makes every error positive and punishes large mistakes much more than small ones: an error of 4 costs 16 times more than an error of 1.

### The formula

$$\text{MSE}=\frac1n\sum_{i=1}^{n}(\hat y_i-y_i)^2$$

### Why it matters

- MSE is the standard regression loss, and squaring punishes large errors much harder than small ones.
- It is smooth and convex for linear models, so gradient descent works well.

### How it works

1. Subtract the targets from the predictions.
2. Square each error.
3. Average.

### Worked example

The errors are $-0.5,\,0.5,\,0,\,1$ (prediction minus target), their squares $0.25,\,0.25,\,0,\,1$ add to $1.5$, and $1.5/4=0.375$.

## Explanation

The errors are computed element-wise, squared, and averaged. Because of the squaring, MSE is in squared units of the target; take the square root (RMSE) to get back to the original units.
