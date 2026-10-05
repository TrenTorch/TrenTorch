---
name: problem-66-polynomial-features
title: 'Polynomial Features'
tags: [problemset, classical-ml, feature-engineering]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'feature engineering'
hint: 'construct a Vandermonde-style matrix'
tools: [NumPy]
---

## Statement

66 Polynomial Features. For a one-dimensional input vector x and nonnegative degree d, return an (n, d) matrix whose columns are x, x², ..., xᵈ in increasing power order. Do not add a bias/intercept column.

### Function signature

```python
solve(x, degree)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(x=[2, 3], degree=3)
```

**Output**

```python
[[2.0, 4.0, 8.0], [3.0, 9.0, 27.0]]
```

**Example 2**

**Input**

```python
solve(x=[-1, 0], degree=2)
```

**Output**

```python
[[-1.0, 1.0], [0.0, 0.0]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Polynomial features lift each scalar into powers that allow a linear model to represent nonlinear relationships. The feature matrix contains one column per positive integer power through the requested degree.

## Explanation

Compute each output column elementwise from the corresponding power. Powers are in ascending order and no intercept is included.
