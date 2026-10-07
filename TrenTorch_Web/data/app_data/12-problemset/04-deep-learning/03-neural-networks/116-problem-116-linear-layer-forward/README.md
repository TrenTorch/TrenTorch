---
name: problem-116-linear-layer-forward
title: 'Linear Layer Forward'
tags: [problemset, dl-core, forward-pass]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'forward pass'
hint: 'X @ W + b'
tools: [NumPy]
---

## Statement

Compute the forward pass of a dense (fully connected) layer for a batch: $Y=XW+b$, where `X` is $n\times d_{in}$, `W` is $d_{in}\times d_{out}$ and `b` has length $d_{out}$.

Implement `solve(X,W,b)`.

**Returns.** Return an $n\times d_{out}$ NumPy array.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0]], [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0])
```

Output:

```text
[[1.0, 2.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], [[1.0], [1.0]], [0.5])
```

Output:

```text
[[3.5], [7.5]]
```

## Theory

### The simple version

A dense layer gives each output neuron a weighted sum of all the inputs plus a bias. Doing this for a whole batch is a single matrix multiplication, which is why GPUs make neural networks fast.

### The formula

$$Y=XW+\mathbf 1b^\top$$

## Explanation

The bias vector is broadcast over the batch dimension. With the identity matrix as weights and a zero bias (first example) the layer returns its input unchanged.
