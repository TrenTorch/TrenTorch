---
name: numpy-np-dot
title: np.dot
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions using `np.dot` for both vector dot products and matrix multiplication, and clarify how `dot` relates to `@`.

## Theory

**For two 1D arrays**, `np.dot` computes the **dot product**: pairing elements, multiplying, summing to a single scalar.

$$
a \cdot b = \sum_{k=0}^{n-1} a_k \cdot b_k
$$

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
np.dot(a, b)     # 1*4 + 2*5 + 3*6 = 32
```

**For two 2D arrays**, `np.dot(A, B)` behaves identically to `A @ B` — same matrix multiplication definition, same shape requirements.

Since `np.dot`'s meaning depends on input shapes, `@` is generally preferred for matrix multiplication (its meaning is fixed). `np.dot` remains the standard way to name a plain vector dot product explicitly — `@` between two 1D arrays also falls back to the same dot-product behavior.

## Explanation

`vector_dot_product` is `np.dot(a, b)` on 1D inputs — a scalar. `matrix_product_via_dot` is `np.dot(a, b)` on 2D inputs, confirming it matches `a @ b` for that case.
