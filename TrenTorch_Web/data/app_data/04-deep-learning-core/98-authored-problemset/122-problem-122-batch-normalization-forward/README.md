---
name: problem-122-batch-normalization-forward
title: "Batch Normalization Forward"
tags: [problemset, dl-core, normalization]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "normalization"
hint: "use batch mean and variance"
tools: [NumPy]
---

## Statement

122 Batch Normalization Forward. Apply training-mode batch normalization to a 2D batch. Compute per-feature population mean and variance over axis 0, normalize using sqrt(var+eps), then apply featurewise scale gamma and shift beta.

### Function signature

```python
solve(X, gamma, beta, eps=1e-05)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(X=[[1, 2], [3, 4]], gamma=[1, 2], beta=[0, 1], eps=0)
```

**Output**

```python
[[-1.0, -1.0], [1.0, 3.0]]
```

**Example 2**

**Input**

```python
solve(X=[[2], [2]], gamma=[3], beta=[4])
```

**Output**

```python
[[4.0], [4.0]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Batch normalization uses batch statistics independently for each feature. Epsilon keeps the denominator defined for constant features.

## Explanation

Compute columnwise mean and population variance, normalize each row, then apply gamma and beta by broadcasting.
