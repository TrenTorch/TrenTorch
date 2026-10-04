---
name: problem-44-inferential-regression-slope
title: "Inferential Regression Slope"
tags: [problemset, data-stats-for-ds, regression-for-inference]
difficulty: Intermediate
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "regression for inference"
hint: "center x and y and use covariance over variance"
tools: [NumPy]
---

# Inferential Regression Slope

## Statement

Implement `solve(x, y)`. Compute the least-squares slope and intercept for y as a linear function of one predictor x.

## Theory

The slope is the centered cross-product divided by the centered sum of squares; the intercept makes the fitted line pass through both sample means.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.

## Examples

**Example 1**

Input:
```python
solve([1.0, 2.0, 3.0], [2.0, 4.0, 5.0])
```

Output:
```text
(1.5, 0.6666666666666665)
```

**Example 2**

Input:
```python
solve([0.0, 1.0, 2.0], [3.0, 5.0, 7.0])
```

Output:
```text
(2.0, 3.0)
```
