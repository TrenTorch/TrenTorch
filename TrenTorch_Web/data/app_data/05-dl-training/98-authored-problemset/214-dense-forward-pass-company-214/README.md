---
name: dense-forward-pass-company-214
title: "dense-forward-pass — NVIDIA case"
tags: [problemset, dl-core, forward-pass-mechanics, nvidia]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "Optimization"
caseCompany: "NVIDIA"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Compute dense batch forward pass X @ W.T + b.

Signature: `def solve(X, W, b)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([[1.0, 2.0], [3.0, 4.0]], [[1.0, -1.0], [0.5, 2.0]], [0.5, -1.0])
```

Returns:

```python
[[-0.5, 3.5], [-0.5, 8.5]]
```

### Example 2

```python
solve([[1.0, -1.0]], [[2.0, 1.0]], [0.0])
```

Returns:

```python
[[1.0]]
```

## Theory

Each input row multiplies each output unit's weights; bias is broadcast over rows.

## Explanation

Compute dense batch forward pass X @ W.T + b. The examples show concrete inputs and expected returned values.
