---
name: problem-117-linear-layer-backward
title: "Linear Layer Backward"
tags: [problemset, dl-core, backpropagation]
difficulty: Advanced
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "backpropagation"
hint: "apply chain rule to matrix products"
tools: [NumPy]
---

## Statement

117 Linear Layer Backward. Backpropagate through Y=X@W+b, given X, upstream derivative dY, and W. Return (dX, dW, db), where dX=dY@W.T, dW=X.T@dY, and db sums dY over the batch.

### Function signature

```python
solve(X, dY, W)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(X=[[1, 2], [3, 4]], dY=[[1], [2]], W=[[2], [3]])
```

**Output**

```python
([[2, 3], [4, 6]], [[7], [10]], [3])
```

**Example 2**

**Input**

```python
solve(X=[[2]], dY=[[3]], W=[[4]])
```

**Output**

```python
([[12]], [[6]], [3])
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

The chain rule sends the upstream derivative through the weight matrix, while parameter derivatives aggregate contributions across examples.

## Explanation

Apply matrix derivatives of the affine transform. Summing dY over rows accounts for the shared bias parameter.
