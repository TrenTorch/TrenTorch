---
name: center-features-for-pca-company-212
title: 'center-features-for-pca — Apple case'
tags: [problemset, unsupervised-ml, pca, apple]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'Classic ML'
caseCompany: 'Apple'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

Center every feature column of X by subtracting that column's arithmetic mean.

Signature: `def solve(X)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
```

Returns:

```python
[[-2.0, -2.0], [0.0, 0.0], [2.0, 2.0]]
```

### Example 2

```python
solve([[3.0, 4.0]])
```

Returns:

```python
[[0.0, 0.0]]
```

## Theory

For each feature j return X[:,j]-mean(X[:,j]); centered columns have mean zero.

## Explanation

Center every feature column of X by subtracting that column's arithmetic mean. The examples show concrete inputs and expected returned values.
