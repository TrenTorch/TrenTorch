---
name: dl-tensor-broadcasting-rules
title: 'Broadcasting Rules'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Master the broadcasting rules for shape compatibility. When combining tensors of different shapes, expand dimensions systematically. Identify when broadcasting is impossible.

## Theory

### Broadcasting rules (4 rules, applied right-to-left)

When operating on tensors with different shapes, NumPy/PyTorch broadcast them to a common shape:

1. Dimensions must be compatible: either equal OR one of them is 1
2. Missing dimensions are prepended with size 1
3. Dimensions with size 1 are expanded to match

`
a: (3, 1, 4)
b: (   2, 4)  # missing leading dims → (1, 2, 4)
Result: (3, 2, 4)
`

### Broadcasting examples

`
Shape (5,) + Shape (1,) → (5,)    ✓
Shape (5,) + Shape (5,) → (5,)    ✓
Shape (4, 5) + Shape (5,) → (4, 5) ✓ (expand 5 to 1D row)
Shape (4, 5) + Shape (4, 1) → (4, 5) ✓ (expand 1 to 5)
Shape (4, 5) + Shape (3, 5) → ERROR ✗ (4 ≠ 3, neither is 1)
`

### When broadcasting fails

- Non-singleton dimensions don't match and neither is 1
- Dimension count mismatch + incompatible leading dimensions

### Why broadcasting matters

- Enables operations on different-shaped tensors without manual expansion
- Crucial for batching: batch of shape (B, 1, 1) × weights (1, D, D) → (B, D, D)
- Memory efficient: doesn't actually expand; operations computed virtually

## Explanation

Solutions trace through broadcasting rules step-by-step for various shape combinations. Key skill: quickly identify compatible shapes and predict result shape without trial/error.
