---
name: problem-28-robust-scaling
title: "Robust Scaling"
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Data Processing"
topic: "data cleaning"
hint: "use Q3-Q1 and guard against zero IQR"
tools: [NumPy]
---

# Robust Scaling

## Statement

Implement `solve(X)`. Center each feature on its median and divide by its interquartile range. A zero-IQR feature maps to zero.

## Theory

Robust scaling uses (x−median)/(Q3−Q1), reducing the effect of outliers compared with mean/std scaling.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([[1.0],[2.0],[3.0],[4.0]])
```

Output:
```text
[[-1.0], [-0.3333333333333333], [0.3333333333333333], [1.0]]
```

**Example 2**

Input:
```python
solve([[2.0, 7.0],[4.0, 7.0],[6.0, 7.0]])
```

Output:
```text
[[-1.0, 0.0], [0.0, 0.0], [1.0, 0.0]]
```
