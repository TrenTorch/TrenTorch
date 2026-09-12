---
name: math-matrix-multiplication
title: Matrix multiplication from first principles
tags: [linear-algebra, matrices]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-vectors-matrices-tensors` already warned that `elementwise_multiply` is not matrix multiplication. Here's why they're genuinely different operations, not just different names for the same thing.

Say a small store sells 3 products, and you track how many units of each product 4 different customers bought, a `(4, 3)` matrix. Separately, each product has a price, a length-3 vector. "How much did each customer spend in total" is not an elementwise operation, customer 1's spending depends on ALL three of their quantities combined with ALL three prices, not one quantity paired with one price. That "combine an entire row with an entire column" operation, repeated for every customer, is matrix multiplication, and every entry of the result is its own independent dot product.

### From theory to code

Theory derives the shape rule (`a`'s columns must equal `b`'s rows) and the exact formula for one output entry: row `i` of `a`, dotted against column `j` of `b`. Implement that directly, one dot product per output position, using explicit loops over positions rather than `np.matmul`/`@` so the row/column mechanism is visible in the code itself, once, before you rely on a library to do it silently for the rest of the curriculum.

Implement `matmul_from_scratch(a, b)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `a` is `(m, k)`, `b` is `(k, n)`, result is `(m, n)`.
- Raise `ValueError` if `a`'s columns don't match `b`'s rows.
- No `np.matmul`, `np.dot` on the full matrices, or `@` anywhere in your implementation, loop over output positions `(i, j)` explicitly.
- The inner reduction (summing one row-times-column product) may use NumPy's own elementwise multiply and sum, reimplementing that with a third loop isn't the point of this question.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Every entry `result[i, j]` only ever needs `a`'s row `i` and `b`'s column `j`, nothing else from either matrix.

</details>

<details>
<summary>Hint 2</summary>

`a[i, :] * b[:, j]` lines up two same-length 1D vectors elementwise. What single reduction turns that into the number that goes in `result[i, j]`?

</details>

## Theory

### The simple version

Picture a small store with 3 products and 4 customers. You know how many units of each product each customer bought (a 4x3 grid of quantities) and how much each product costs (a list of 3 prices). "How much did each customer spend" isn't a per-cell operation: customer 1's total pulls together all three of their quantities and all three prices at once. Do that combine-a-whole-row-with-a-whole-column step for every customer, and you've just done matrix multiplication.

### The formula

```text
a: (m, k)   b: (k, n)   ->   result: (m, n)

result[i, j] = a[i, 0]*b[0, j] + a[i, 1]*b[1, j] + ... + a[i, k-1]*b[k-1, j]
             = dot_product(a's row i, b's column j)
```

Every single entry of the output is its own dot product: row `i` of `a`, dotted against column `j` of `b`. This is the mechanism behind `linear`, the very first question this entire curriculum starts with (`input @ weight.T`): each output feature is one row of the weight matrix, dotted against the input.

The shape rule (`a`'s columns must equal `b`'s rows) is not a technicality, it is what makes the dot product well-defined at every position: `a`'s row `i` and `b`'s column `j` need the same length (`k`) to be dotted together at all.

### How PyTorch actually implements this

`a @ b` never runs the triple-nested loop this question asks you to write by hand. `torch.matmul` dispatches to a highly-tuned BLAS routine (`cblas_sgemm`/`dgemm` on CPU, cuBLAS on GPU), which tiles the computation to keep data in cache, uses SIMD/tensor-core instructions to compute many multiply-adds per cycle, and on GPU runs thousands of these dot products in parallel across cores. This is precisely why the naive `O(m*n*k)` loop this question implements is fine for teaching but would be catastrophically slow for a real `(4096, 4096) @ (4096, 4096)` layer, the mathematical operation is identical, only the execution strategy differs, by many orders of magnitude.

## Explanation

`matmul_from_scratch` reads off `a`'s shape as `(m, k)` and `b`'s as `(k2, n)`, raising a clear error if `k != k2` (the shape rule from Theory). It then loops over every output position `(i, j)` and fills it with `np.sum(a[i, :] * b[:, j])`, exactly the row-dotted-with-column definition, using NumPy's own elementwise multiply and sum for the inner reduction rather than a third explicit loop (the point of this exercise is the row/column structure, not reimplementing summation).
