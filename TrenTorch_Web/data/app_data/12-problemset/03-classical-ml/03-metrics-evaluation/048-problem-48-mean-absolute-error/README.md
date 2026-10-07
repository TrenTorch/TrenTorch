---
name: problem-48-mean-absolute-error
title: 'Mean Absolute Error'
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'mean of the absolute differences'
tools: [NumPy]
---

## Statement

Compute the mean absolute error between aligned arrays of true targets and predictions.

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
0.5
```

**Example 2**

Input:

```python
solve([0.0, 0.0], [10.0, -10.0])
```

Output:

```text
10.0
```

## Theory

### The simple version

MAE is the average size of the error, ignoring direction. It is in the same units as the target and, unlike MSE, treats an error of 4 as exactly four times an error of 1, so it is less sensitive to outliers.

### The formula

$$\text{MAE}=\frac1n\sum_{i=1}^{n}|\hat y_i-y_i|$$

## Explanation

Absolute values stop positive and negative errors from cancelling. In the second example the errors $+10$ and $-10$ cancel in a plain mean but give an MAE of $10$.
