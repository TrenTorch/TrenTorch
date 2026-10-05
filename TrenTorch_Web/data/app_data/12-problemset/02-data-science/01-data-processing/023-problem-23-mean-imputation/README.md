---
name: problem-23-mean-imputation
title: 'Mean Imputation'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Advanced
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'compute the mean ignoring missing values'
tools: [NumPy]
---

## Statement

Implement `solve(x)`. Replace missing entries in a numeric array with the mean of its observed entries.

### Examples

**Example 1**

Input:

```python
solve([1.0, float("nan"), 3.0, 4.0])
```

Output:

```text
[1.0, 2.6666666666666665, 3.0, 4.0]
```

**Example 2**

Input:

```python
solve([2.0, float("nan"), 6.0])
```

Output:

```text
[2.0, 4.0, 6.0]
```

## Theory

Compute the mean over non-missing values, then substitute that value at every NaN position.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.
