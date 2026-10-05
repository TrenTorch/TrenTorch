---
name: kmeans-assignment-company-211
title: 'kmeans-assignment — Meta case'
tags: [problemset, unsupervised-ml, k-means-clustering, meta]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Meta'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

For each point in X return nearest-centroid index by squared Euclidean distance; ties choose lowest index.

Signature: `def solve(X, C)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([[0.0, 0.0], [2.0, 2.0]], [[0.0, 1.0], [3.0, 3.0]])
```

Returns:

```python
[0, 1]
```

### Example 2

```python
solve([[1.0, 0.0]], [[0.0, 0.0], [2.0, 0.0]])
```

Returns:

```python
[0]
```

## Theory

Assign each point to argmin_j sum_d (X[i,d]-C[j,d])².

## Explanation

For each point in X return nearest-centroid index by squared Euclidean distance; ties choose lowest index. The examples show concrete inputs and expected returned values.
