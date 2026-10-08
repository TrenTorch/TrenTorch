---
name: dense-forward-pass-company-214
title: 'dense-forward-pass — NVIDIA case'
tags: [problemset, dl-core, forward-pass-mechanics, nvidia]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'NVIDIA'
hint: 'X @ W.T + b'
tools: [NumPy]
---

## Statement

NVIDIA-inspired GPU-scheduler team is testing a lightweight neural score used to estimate whether a workload will fit a device profile. You need to implement the dense forward pass exactly, because a shape or bias error here would make every downstream score unreliable.

Compute a fully connected layer $Y=XW^\top+b$ for a batch. `X` has shape `(n, d_in)`, `W` has shape `(d_out, d_in)` (one row of weights per output unit, as in PyTorch's `nn.Linear`) and `b` has length `d_out`.

Implement `solve(X,W,b)`.

**Returns.** Return an array of shape `(n, d_out)`.

Compute a fully connected layer $Y=XW^\top+b$ for a batch. `X` has shape `(n, d_in)`, `W` has shape `(d_out, d_in)` (one row of weights per output unit, as in PyTorch's `nn.Linear`) and `b` has length `d_out`.

Implement `solve(X,W,b)`.

**Returns.** Return an array of shape `(n, d_out)`.

### Examples

**Example 1**

Input:

```python
solve([[1, 2]], [[1, 0], [0, 1]], [1, 2])
```

Output:

```text
[[2, 4]]
```

**Example 2**

Input:

```python
solve([[1.0, 1.0], [2.0, 0.0]], [[1.0, 2.0]], [0.5])
```

Output:

```text
[[3.5], [2.5]]
```

## Theory

### The simple version

Each output unit takes a weighted sum of all inputs and adds a bias. A batch of inputs is processed with a single matrix product. Here each _row_ of `W` holds the weights of one output unit, so `W` is transposed before multiplying.

### The formula

$$Y=XW^\top+\mathbf 1b^\top$$

### Why it matters

- A dense layer is the basic building block of neural networks.
- Mixing up the two weight layouts, `(in, out)` versus `(out, in)`, silently gives wrong scores.

### How it works

1. Transpose `W` so each row of weights becomes a column.
2. Multiply by `X`.
3. Add the bias to every row.

### Worked example

The row $(1,2)$ times the transposed identity is $(1,2)$, and adding the bias $(1,2)$ gives [[2, 4]].

## Explanation

A common bug is mixing up the two weight layouts, `(d_in, d_out)` versus `(d_out, d_in)`: a shape mismatch or silently wrong values would feed bad scores downstream. In the first example the identity weights leave the input unchanged and the bias adds $(1,2)$.
