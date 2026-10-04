---
name: problem-116-linear-layer-forward
title: "Linear Layer Forward"
tags: [problemset, dl-core, forward-pass]
difficulty: Intermediate
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "forward pass"
hint: "XW+b"
tools: [NumPy]
---

## Statement

116 Linear Layer Forward. Compute a dense affine layer. X has shape (batch, input_features), W has shape (input_features, output_features), and b has shape (output_features,). Return X@W+b with bias broadcast over the batch.

### Function signature

```python
solve(X, W, b)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(X=[[1, 2], [3, 4]], W=[[1, 0], [0, 2]], b=[1, -1])
```

**Output**

```python
[[2, 3], [4, 7]]
```

**Example 2**

**Input**

```python
solve(X=[[2]], W=[[3]], b=[-1])
```

**Output**

```python
[[5]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

A dense layer applies a linear map to each row and adds the same bias vector to each example.

## Explanation

The matrix product combines input features into outputs; NumPy broadcasts the bias along the batch dimension.
