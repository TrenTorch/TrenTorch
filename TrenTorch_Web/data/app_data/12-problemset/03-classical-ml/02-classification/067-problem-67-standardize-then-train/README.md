---
name: problem-67-standardize-then-train
title: 'Standardize Then Train'
tags: [problemset, classical-ml, feature-engineering]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'feature engineering'
hint: 'never use test statistics'
tools: [NumPy]
---

## Statement

67 Standardize Then Train. Standardize each feature column in a two-dimensional training matrix x using its column mean and population standard deviation. Return (x−mean)/std. A constant column maps to zeros. This function only transforms the supplied matrix; it does not fit a model or use test-set statistics.

### Function signature

```python
solve(x)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(x=[[1, 10], [3, 14], [5, 18]])
```

**Output**

```python
[[-1.2247448714, -1.2247448714], [0.0, 0.0], [1.2247448714, 1.2247448714]]
```

**Example 2**

**Input**

```python
solve(x=[[2, 7], [2, 9]])
```

**Output**

```python
[[0.0, -1.0], [0.0, 1.0]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Feature standardization centers each feature and scales it to unit population variance, making feature scales comparable. Statistics are computed column-wise from the supplied training matrix only.

## Explanation

Compute each column mean and standard deviation, replace zero standard deviations with one, and broadcast the normalization across rows. A constant feature therefore remains zero after centering.
