---
name: problem-24-median-imputation
title: "Median Imputation"
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Advanced
kind: problemset
relatedModule: "part-data-foundations|Data Processing"
topic: "data cleaning"
hint: "sort the observed values or use np.median"
tools: [NumPy]
---

# Median Imputation

## Statement

Implement `solve(x)`. Replace missing entries in a numeric array with the median of its observed entries.

## Theory

The median is robust to extreme values; each NaN is replaced by the median of non-NaN observations.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([1.0, float("nan"), 3.0, 4.0])
```

Output:
```text
[1.0, 3.0, 3.0, 4.0]
```

**Example 2**

Input:
```python
solve([1.0, float("nan"), 100.0])
```

Output:
```text
[1.0, 50.5, 100.0]
```
