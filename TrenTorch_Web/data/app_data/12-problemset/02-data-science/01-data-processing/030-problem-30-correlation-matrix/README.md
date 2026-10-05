---
name: problem-30-correlation-matrix
title: 'Correlation Matrix'
tags: [problemset, data-stats-for-ds, eda]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'EDA'
hint: 'center columns, normalize by standard deviations, then form XᵀX'
tools: [NumPy]
---

## Statement

Implement `solve(X)`. Compute the Pearson correlation matrix between feature columns of a 2-D data matrix.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]])
```

Output:

```text
[[1.0, 1.0], [1.0, 1.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 4.0], [2.0, 2.0], [3.0, 0.0]])
```

Output:

```text
[[1.0, -1.0], [-1.0, 1.0]]
```

## Theory

Pearson correlation centers each column and scales covariance by both standard deviations, producing unit diagonal for non-constant features.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.
