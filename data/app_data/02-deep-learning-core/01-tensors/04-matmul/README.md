---
name: dl-core-matmul
title: Matmul
tags: [deep-learning, tensors, linear-algebra]
difficulty: Intermediate
---

## Statement

Implement:

```python
def matmul(a, b) -> np.ndarray:
    """Mirrors torch.matmul(a, b)."""
```

## Theory

`01-hypothesis-function`'s `input @ weight.T` was one specific case of matrix multiplication: two 2D arrays. `torch.matmul` (and NumPy's `@`, which follows the identical convention) actually has several different rules depending on how many dimensions `a` and `b` have:

```text
1D @ 1D:  dot product        -> scalar (a single number, 0-dimensional)
2D @ 1D:  matrix-vector      -> 1D result
1D @ 2D:  vector-matrix      -> 1D result
2D @ 2D:  standard matmul    -> 2D result, the (m,n)@(n,p)->(m,p) rule Q1 used
>2D:      BATCHED matmul     -> the last two dimensions matrix-multiply, every
                                 leading dimension broadcasts (03-broadcasting-rules)
```

The `1D @ 2D` and `2D @ 1D` cases work by temporarily treating the 1D array as a `(1, n)` or `(n, 1)` matrix, doing the multiplication, then removing (squeezing) that temporary dimension from the result, this is why a `2D @ 1D` result comes back as a plain 1D array, not a `(m, 1)` matrix, `01-hypothesis-function`'s own "never squeeze" rule applies to `linear`'s own output convention specifically, not to `matmul` itself, which has this different, dimension-dependent behavior baked into its definition.

The batched case is what actually shows up throughout real neural networks: a batch of `(seq_len, d_model)` matrices, one per sample, all multiplied by the same shared weight matrix in a single call, the leading `batch_size` dimension broadcasts exactly the way `03-broadcasting-rules` describes, while the trailing two dimensions do the actual matrix multiplication.

## Explanation

`matmul` is `a @ b` directly, NumPy's `@` operator (and the `np.matmul` function it calls) implements every one of these rules identically to `torch.matmul`, this isn't a coincidence or a simplification, `@`'s behavior _is_ the specification `torch.matmul` follows. The work in this question is in recognizing which rule applies to which shapes, exercised by the test suite's coverage of each case, not in writing more code.
