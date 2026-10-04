---
name: problem-48-mean-absolute-error
title: "Mean Absolute Error"
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: "part-classical-unsupervised|Metrics & Evaluation"
topic: "metrics"
hint: "average absolute residuals"
tools: [NumPy]
---

# Mean Absolute Error

## Statement

Implement `solve(y_true, y_pred)`. Compute mean absolute error between aligned numeric targets and predictions.

## Theory

MAE averages the absolute residuals, so each unit error contributes linearly.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.

## Examples

**Example 1**

Input:
```python
solve([1.0, 2.0, 3.0], [1.0, 4.0, 2.0])
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
