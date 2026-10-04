---
name: problem-26-min-max-scaling
title: "Min-Max Scaling"
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Data Processing"
topic: "data cleaning"
hint: "protect constant columns from division by zero"
tools: [NumPy]
---

# Min-Max Scaling

## Statement

Implement `solve(X)`. Scale each feature column to [0,1] using that column’s minimum and maximum. Constant columns map to zero.

## Theory

Each feature is shifted by its minimum and divided by its range. A zero range is assigned all zeros.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([[1.0, 10.0], [2.0, 10.0], [3.0, 10.0]])
```

Output:
```text
[[0.0, 0.0], [0.5, 0.0], [1.0, 0.0]]
```

**Example 2**

Input:
```python
solve([[0.0, 2.0], [4.0, 6.0]])
```

Output:
```text
[[0.0, 0.0], [1.0, 1.0]]
```
