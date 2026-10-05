---
name: problem-47-mean-squared-error
title: 'Mean Squared Error'
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'average squared residuals'
tools: [NumPy]
---

## Statement

Implement `solve(y_true, y_pred)`. Compute mean squared error between aligned numeric targets and predictions.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], [1.0, 4.0, 2.0])
```

Output:

```text
1.6666666666666667
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

MSE is the arithmetic mean of squared residuals; squaring penalizes larger errors more strongly.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
