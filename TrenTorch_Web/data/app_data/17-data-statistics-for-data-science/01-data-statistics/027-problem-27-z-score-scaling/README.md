---
name: problem-27-z-score-scaling
title: "Z-Score Scaling"
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Data Processing"
topic: "data cleaning"
hint: "use training statistics only"
tools: [NumPy]
---

# Z-Score Scaling

## Statement

Implement `solve(X)`. Standardize each feature using its column mean and population standard deviation. Constant columns map to zero.

## Theory

For each feature, subtract the mean and divide by the population standard deviation (ddof=0).

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([[1.0, 5.0], [2.0, 5.0], [3.0, 5.0]])
```

Output:
```text
[[-1.224744871391589, 0.0], [0.0, 0.0], [1.224744871391589, 0.0]]
```

**Example 2**

Input:
```python
solve([[2.0], [4.0]])
```

Output:
```text
[[-1.0], [1.0]]
```
