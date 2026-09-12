---
name: dl-core-backward-matmul
title: Backward for matmul
tags: [neural-networks, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Backward for multiplication` handled scalars, where "sensitivity to `a` depends on `b`" is a single number times a single number. `linear`, this curriculum's very first question, is built on matrix multiplication instead, `input @ weight.T`, and every gradient computed in `linear_regression` and `classification`'s training loops secretly depended on getting THIS backward rule right, even though those tracks derived it by hand for their specific case rather than deriving the fully general matmul backward rule this question builds directly.

The genuinely new difficulty here, beyond `Backward for multiplication`'s scalar case: the SHAPES have to work out. `grad_output` has the shape of the OUTPUT, `C`, but the gradients you need to return must match the shapes of the INPUTS, `A` and `B`, which are generally different shapes entirely. Getting the transpose placement right is what makes those shapes line up correctly.

### From theory to code

Theory derives `dL/dA` and `dL/dB` for `C = A @ B` by generalizing the scalar chain rule to matrices, landing on a formula built entirely from matrix multiplications and transposes, the exact operations `03-matrix-multiplication` and `Transpose, and its role in reshaping without copying data` (both Math & Statistics) already cover individually.

Implement `matmul_backward(grad_output, a, b)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `a` is `(m, k)`, `b` is `(k, n)`, `grad_output` is `(m, n)` (matching `C`'s shape).
- `grad_a` must come out shaped `(m, k)` (matching `a`), `grad_b` shaped `(k, n)` (matching `b`).
- Use only `@` and `.T`, no explicit element-by-element loop.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`grad_a`'s shape must match `a`'s shape, `(m, k)`. Only one arrangement of `grad_output` `(m, n)` and `b.T` `(n, k)` multiplies to that shape.

</details>

<details>
<summary>Hint 2</summary>

`grad_a = grad_output @ b.T`, `grad_b = a.T @ grad_output`, check the shapes yourself: `(m,n)@(n,k) = (m,k)` and `(k,m)@(m,n) = (k,n)`, both match.

</details>

## Theory

### The simple version

`Backward for multiplication`'s rule, "each input's gradient is the upstream gradient times the OTHER input," carries over to matrices almost unchanged, but matrices need a transpose to make the shapes line up, since matrix multiplication (unlike scalar multiplication) isn't symmetric, `A @ B` and `B @ A` aren't even the same shape in general, let alone the same value.

### The formula

For `C = A @ B` (`A` is `(m, k)`, `B` is `(k, n)`, `C` is `(m, n)`):

```text
dL/dA = dL/dC @ B^T
dL/dB = A^T @ dL/dC
```

A quick shape check confirms these are the only arrangements that work: `grad_output` is `(m, n)`, `B^T` is `(n, k)`, so `grad_output @ B^T` is `(m, k)`, matching `A`. Similarly, `A^T` is `(k, m)`, so `A^T @ grad_output` is `(k, n)`, matching `B`. Getting the multiplication ORDER and WHICH operand gets transposed right (rather than, say, `B^T @ grad_output`, which wouldn't even be shape-compatible in general) is the entire difficulty this question adds over the scalar case.

This is precisely the formula every earlier training loop in this curriculum has been using without deriving explicitly: `03-mse-gradient`'s `grad_weight = grad_prediction.T @ input` is exactly this rule, applied to `linear`'s own `input @ weight.T` matmul, with the transpose placement worked out by hand for that specific case rather than stated as a general rule the way this question does.

### How PyTorch actually implements this

Every `@` (or `torch.matmul`) between two `requires_grad=True` tensors registers a `MmBackward0` node computing exactly these two formulas during `.backward()`, this is the single most-executed backward rule in the entirety of deep learning, since nearly every layer in every network (`linear`, attention's query/key/value projections, convolutions reformulated as matmuls) bottoms out in matrix multiplication somewhere. Getting this one backward rule right, once, in a general library, is what lets every higher-level layer built on top of matmul (`linear`, and everything built from it throughout this curriculum) inherit correct gradients automatically, without every layer author needing to re-derive `03-mse-gradient`'s hand-derived transpose placement themselves.

## Explanation

`matmul_backward` computes `grad_output @ b.T` for `grad_a` and `a.T @ grad_output` for `grad_b`, the two formulas from Theory, using only matrix multiplication and transpose, both operations `03-matrix-multiplication` and `Transpose, and its role in reshaping without copying data` already established individually.
