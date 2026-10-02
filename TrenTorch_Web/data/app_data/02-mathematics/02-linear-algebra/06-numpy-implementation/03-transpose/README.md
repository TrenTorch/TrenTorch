---
name: numpy-transpose-in-linear-algebra
title: Transpose in a Linear-Algebra Context
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions using transpose specifically as part of matrix-multiplication-based computations.

## Theory

**A common pattern: computing all pairwise dot products between the rows of a matrix and the rows of another matrix.** Matrix multiplication pairs row $i$ of the first matrix with **column** $j$ of the second. Transposing the second matrix converts its rows into columns, so "column $j$" becomes exactly "row $j$ of the original second matrix."

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B.T
# result[i, j] = dot product of A's row i and B's row j
# result[0,0] = 1*5 + 2*6 = 17
# result[0,1] = 1*7 + 2*8 = 23
```

This `A @ B.T` pattern comes up constantly in ML (comparing every example against every other example, every query against every key).

**Matrix-vector products**: a 1D vector works directly with `@` against a matrix — no explicit transpose or reshape needed.

```python
A = np.array([[1, 2], [3, 4]])     # shape (2, 2)
v = np.array([5, 6])                  # shape (2,)
A @ v                                    # 1D result, shape (2,)
```

## Explanation

`pairwise_row_dots` returns `a @ b.T` directly — no loop needed, since matrix multiplication with a transposed second operand already computes every row-pair dot product in one call. `matrix_vector_product` returns `matrix @ vector`, relying on NumPy treating the 1D vector correctly without any reshape.
