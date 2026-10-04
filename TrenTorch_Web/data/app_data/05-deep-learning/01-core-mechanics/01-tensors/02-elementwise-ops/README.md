---
name: dl-tensor-elementwise-ops
title: 'Element-wise Operations'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Perform element-wise operations: addition, multiplication, power, sqrt, etc. Understand broadcasting and shape alignment. Operations apply independently to each element.

## Theory

### Element-wise operations are independent per element

Operations like +, *, sqrt apply to each element without interaction. Result shape matches input shape.

`python
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])
c = a + b  # [5, 7, 9] (element by element)
d = a * 2  # [2, 4, 6] (scalar broadcast to each element)
`

### Broadcasting: automatic shape alignment

Broadcasting repeats smaller tensors to match larger shapes:

`python
a = torch.ones(3, 1)    # shape (3, 1)
b = torch.ones(1, 4)    # shape (1, 4)
c = a + b               # shape (3, 4): broadcasts both
`

### Common element-wise operations

- Arithmetic: +, -, *, /, // (floor divide), ** (power)
- Activation-like: sqrt, exp, log, sin, cos
- Comparison: ==, !=, <, >, <=, >=
- Boolean: &, |, ~ (and, or, not)

### Why element-wise ops matter

- Vectorized: entire tensor operation in one call (much faster than Python loops)
- Foundation for neural network layers (linear layers apply elementwise after matmul)
- Broadcasting: enables flexible shape handling without explicit reshaping

## Explanation

Solutions apply various element-wise operations, leveraging broadcasting to handle shape mismatches. Key insight: understanding broadcasting eliminates manual reshaping and enables clean, efficient code.
