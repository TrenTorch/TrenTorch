---
name: dl-core-matmul
title: Matmul
tags: [deep-learning, tensors, linear-algebra]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-hypothesis-function`'s `input @ weight.T` was one specific case of matrix multiplication: two 2D arrays combining into a 2D result. Real networks don't stop there — sometimes you multiply a single vector against a matrix, sometimes you multiply a whole batch of matrices against one shared matrix in a single call, and each of those situations has a slightly different rule for what shape comes out. `torch.matmul` is the one function that has to make all of these cases behave sensibly, and predicting its output shape correctly is what this question is really testing.

### From theory to code

Implement `matmul(a, b)`, mirroring `torch.matmul`. Theory lays out the dimension-dependent rules (1D-1D, 2D-1D, 1D-2D, 2D-2D, batched); the function itself doesn't need to branch on any of them explicitly, because `03-broadcasting-rules`'s broadcasting logic and NumPy's own `@` operator already implement every one of those cases identically to `torch.matmul`.

### Constraints

- `a` and `b` can each be 1D, 2D, or higher-dimensional (batched).
- 1D-1D input produces a 0-dimensional scalar result (a dot product).
- 2D-1D and 1D-2D inputs produce a 1D result, the temporary extra dimension is squeezed out, not left as a size-1 dimension.
- 2D-2D inputs follow standard `(m,n)@(n,p)->(m,p)` matrix multiplication.
- Higher-than-2D inputs batch-multiply over their trailing two dimensions, with every leading dimension broadcasting per `03-broadcasting-rules`.
- One expression, no manual branching on `a.ndim`/`b.ndim`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

You don't need to write five different code paths for five different dimensionality cases. Is there a single NumPy operator that already implements all of `torch.matmul`'s dimension-dependent rules?

</details>

<details>
<summary>Hint 2</summary>

`a @ b` is it — `@` calls `np.matmul` under the hood, and `np.matmul` follows the exact same 1D/2D/batched convention `torch.matmul` documents. The work in this question is recognizing which rule applies to which test case, not writing more code.

</details>

## Theory

### The simple version

Think of `matmul` as one operator that quietly adapts its behavior to how "flat" or "stacked" its inputs are. Two plain lists of numbers multiply into a single number (a dot product). A grid of numbers times a plain list gives back a plain list. Two grids give back a grid. And a stack of grids times one shared grid multiplies each grid in the stack independently against that shared grid, all in one call.

### The formula

```text
1D @ 1D:  dot product        -> scalar (a single number, 0-dimensional)
2D @ 1D:  matrix-vector      -> 1D result
1D @ 2D:  vector-matrix      -> 1D result
2D @ 2D:  standard matmul    -> 2D result, the (m,n)@(n,p)->(m,p) rule 01-hypothesis-function used
>2D:      BATCHED matmul     -> the last two dimensions matrix-multiply, every
                                 leading dimension broadcasts (03-broadcasting-rules)
```

The `1D @ 2D` and `2D @ 1D` cases work by temporarily treating the 1D array as a `(1, n)` or `(n, 1)` matrix, doing the multiplication, then squeezing that temporary dimension back out of the result — this is why a `2D @ 1D` result comes back as a plain 1D array, not a `(m, 1)` matrix; `01-hypothesis-function`'s "never squeeze" convention is specific to `linear`'s own output shape, not to `matmul` itself, which has this different, dimension-dependent squeezing baked into its definition.

### How PyTorch actually implements this

`torch.matmul(a, b)` documents exactly these dimension-dependent rules, including the batched case broadcasting leading dimensions the way `03-broadcasting-rules` describes. `tests.py` doesn't bake in a PyTorch-generated numeric oracle here, the hand-computed values in the tests (e.g. `[1,2,3]·[4,5,6] = 32`) are plain arithmetic, verifiable independent of any PyTorch run, so this section stays a general description of the documented API, not a numeric claim beyond that.

## Explanation

`matmul` in `solution.py` is `a @ b` directly. NumPy's `@` operator (and the `np.matmul` function it calls) implements every one of the rules from Theory identically to `torch.matmul`, this isn't a coincidence or a simplification, `@`'s behavior _is_ the specification `torch.matmul` follows. `tests.py` exercises each rule separately: `test_1d_dot_1d_gives_a_scalar` checks the 0-dimensional dot-product case, `test_2d_matmul_1d_gives_1d_result`/`test_1d_matmul_2d_gives_1d_result` check the squeezed-vector cases, and `test_batched_matmul_broadcasts_the_leading_dimension` checks that a `(2, 3, 4)` batch against a shared `(4, 5)` weight matrix produces `(2, 3, 5)`, matching each batch element's own `batch[i] @ shared_weight`. The work in this question is in recognizing which rule applies to which shapes, exercised by the test suite's coverage of each case, not in writing more code.
