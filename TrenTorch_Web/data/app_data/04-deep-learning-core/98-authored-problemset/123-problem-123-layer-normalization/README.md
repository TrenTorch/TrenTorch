---
name: problem-123-layer-normalization
title: "Layer Normalization"
tags: [problemset, dl-core, normalization]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "normalization"
hint: "compute mean and variance per row"
tools: [NumPy]
---

## Statement

123 Layer Normalization. Apply layer normalization to a 2D batch by computing each row’s mean and population variance across feature columns. Normalize with sqrt(var+eps), then apply featurewise gamma and beta.

### Function signature

```python
solve(X, gamma, beta, eps=1e-05)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(X=[[1, 3], [2, 6]], gamma=[1, 2], beta=[0, 1], eps=0)
```

**Output**

```python
[[-1.0, 3.0], [-1.0, 3.0]]
```

**Example 2**

**Input**

```python
solve(X=[[2, 2]], gamma=[3, 4], beta=[1, -1])
```

**Output**

```python
[[1.0, -1.0]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Layer normalization normalizes each example independently, rather than aggregating statistics across examples. It is independent of batch composition.

## Explanation

Reduce each row along its feature axis, retain dimensions for broadcasting, normalize, and apply scale and shift.
