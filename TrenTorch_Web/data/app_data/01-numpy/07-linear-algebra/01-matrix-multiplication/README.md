---
name: numpy-matrix-multiplication
title: Matrix Multiplication with @ / matmul
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement matrix multiplication from its definition, then use NumPy's `@` operator, directly contrasting it with element-wise `*`.

## Theory

For matrix $A$ of shape $(m, n)$ and $B$ of shape $(n, p)$, the product $C = A @ B$ has shape $(m, p)$:

$$
C_{i,j} = \sum_{k=0}^{n-1} A_{i,k} \cdot B_{k,j}
$$

Element $(i, j)$ pairs row $i$ of $A$ with column $j$ of $B$, multiplies corresponding entries, and sums. $A$'s column count must match $B$'s row count.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
A @ B     # [[19, 22], [43, 50]]
```

**Contrast with element-wise `*`** on the same matrices: `A * B` gives `[[5, 12], [21, 32]]` — same-position pairing, no summation. These are different operations with different shape requirements: `*` needs broadcast compatibility, `@` needs inner dimensions to match.

Matrix multiplication is **not commutative**: `A @ B != B @ A` in general.

`np.matmul(A, B)` is equivalent to `A @ B`.

## Explanation

`matmul_from_scratch` uses three nested loops over `i`, `j`, `k`, accumulating `a[i, k] * b[k, j]` into `result[i, j]`. `matmul_builtin` is the single expression `a @ b`. `compare_matmul_and_elementwise` computes both `a @ b` and `a * b` and reports whether `np.array_equal` says they differ (checked directly, not assumed).
