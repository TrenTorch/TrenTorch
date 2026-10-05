---
name: problem-29-iqr-outlier-flagging
title: 'IQR Outlier Flagging'
tags: [problemset, data-stats-for-ds, eda]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'EDA'
hint: 'compute Q1 and Q3 and compare bounds'
tools: [NumPy]
---

## Statement

Implement `solve(x)`. Flag values strictly outside the Tukey fences Q1−1.5·IQR and Q3+1.5·IQR.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 10.0])
```

Output:

```text
[False, False, False, True]
```

**Example 2**

Input:

```python
solve([-100.0, 0.0, 1.0, 2.0, 3.0])
```

Output:

```text
[True, False, False, False, False]
```

## Theory

The interquartile range measures the middle half of the data; values beyond 1.5 IQR from either quartile are flagged.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.
