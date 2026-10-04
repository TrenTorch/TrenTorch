---
name: problem-119-two-layer-mlp-backward
title: "Two-Layer MLP Backward"
tags: [problemset, dl-core, backpropagation]
difficulty: Advanced
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "backpropagation"
hint: "reverse the forward operations"
tools: [NumPy]
---

## Statement

119 Two Layer Mlp Backward. Backpropagate dY through an affine-ReLU-affine network. cache is the (z1,h) tuple returned by the forward pass. Return (dX,dW1,db1,dW2,db2).

### Function signature

```python
solve(X, dY, W1, W2, cache)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(X=[[1, 2]], dY=[[1]], W1=[[1, 0], [0, 1]], W2=[[2], [3]], cache=([[1, -1]], [[1, 0]]))
```

**Output**

```python
([[2, 0]], [[2, 0], [4, 0]], [2, 0], [[1], [0]], [1])
```

**Example 2**

**Input**

```python
solve(X=[[2]], dY=[[3]], W1=[[1]], W2=[[4]], cache=([[1]], [[1]]))
```

**Output**

```python
([[12]], [[24]], [12], [[3]], [3])
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Backpropagation applies the chain rule in reverse order. The ReLU derivative gates the hidden-layer gradient according to cached preactivation.

## Explanation

Compute output-layer gradients and propagate through W2; apply the ReLU mask, then compute input and first-layer gradients. Bias gradients sum over the batch.
