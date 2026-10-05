---
name: problem-118-two-layer-mlp-forward
title: 'Two-Layer MLP Forward'
tags: [problemset, dl-core, forward-pass]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'forward pass'
hint: 'cache hidden preactivation for backward'
tools: [NumPy]
---

## Statement

118 Two Layer Mlp Forward. Compute an affine-ReLU-affine network. Return (Y, cache), where z1=X@W1+b1, h=max(z1,0), Y=h@W2+b2, and cache=(z1,h).

### Function signature

```python
solve(X, W1, b1, W2, b2)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(X=[[1, 2]], W1=[[1, 0], [0, 1]], b1=[-1, 1], W2=[[2], [3]], b2=[0])
```

**Output**

```python
([[9]], ([[0, 3]], [[0, 3]]))
```

**Example 2**

**Input**

```python
solve(X=[[2]], W1=[[1]], b1=[-1], W2=[[4]], b2=[1])
```

**Output**

```python
([[5]], ([[1]], [[1]]))
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

A two-layer multilayer perceptron composes an affine transform, a nonlinear activation, and a second affine transform.

## Explanation

Compute and cache the first preactivation and its ReLU output. The cache is returned for use by the backward pass.
