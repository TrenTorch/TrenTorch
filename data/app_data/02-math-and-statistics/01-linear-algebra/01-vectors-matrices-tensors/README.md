---
name: math-vectors-matrices-tensors
title: 'Vectors, matrices and tensors: shapes and basic operations'
tags: [linear-algebra, tensors]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A single temperature reading is one number. A week of daily readings is a list of seven numbers. A month of readings across ten cities is a grid, ten rows, thirty-ish columns. A year of that, split by morning/afternoon/evening, stacks another axis on top of the grid. Nothing about the _idea_ changes as you add axes, only how many numbers you need to address one value: none, one, two, three.

That single idea, "a number, or numbers indexed by however many axes," is the entire foundation this curriculum builds on. Before touching gradients or neural networks, you need the vocabulary for describing the _shape_ of data and the two operations simple enough to define with no ambiguity at all: adding two same-shaped things, and multiplying them position by position.

### From theory to code

Theory names the ranks (scalar, vector, matrix, tensor) and the two attributes every one of them has: `shape` (how many entries along each axis) and `ndim` (how many axes there are). Implement four small functions that expose this vocabulary directly, plus the two operations that only ever touch matching positions.

Implement `shape_of`, `ndim_of`, `elementwise_add` and `elementwise_multiply` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `shape_of` returns a plain tuple, e.g. `(3,)` for a length-3 vector, `()` for a scalar.
- `ndim_of` returns a plain `int`.
- `elementwise_add` and `elementwise_multiply` assume `a` and `b` already share a shape (broadcasting is a later question's job).
- `elementwise_multiply` is NOT matrix multiplication: it must never reduce a vector down to a scalar.
- No Python loop over positions anywhere, this is meant to be vectorized.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Every one of these already exists as a NumPy array attribute or operator. You're exposing vocabulary, not computing anything new.

</details>

<details>
<summary>Hint 2</summary>

`*` on two NumPy arrays is elementwise by default. Matrix multiplication is a separate operator (`@`), covered in a later question, don't reach for it here.

</details>

## Theory

### The simple version

Think of a spreadsheet. One cell is a single number. One row is a list of numbers. The whole sheet is a grid. Now imagine several sheets stacked into a workbook, that's one axis deeper still. At no point did the _kind_ of thing change, only how many "which row, which column, which sheet" numbers you need to point at one value.

That's a **tensor**: a number, addressed by zero or more axis-indices.

### The formula

```text
rank 0 (scalar):  5.0                        shape = ()
rank 1 (vector):  [1, 2, 3]                  shape = (3,)
rank 2 (matrix):  [[1, 2], [3, 4]]           shape = (2, 2)
rank 3+ (tensor): a stack of matrices, etc.  shape = (n, 2, 2), ...
```

A tensor's **shape** is the tuple of its axis lengths, and its **number of dimensions** (`ndim`, sometimes called "rank") is just `len(shape)`. This vocabulary, scalar/vector/matrix/tensor, shape, ndim, is used identically in NumPy and PyTorch, and everywhere in deep learning: a "batch of 32 RGB images, 64x64 pixels" is a rank-4 tensor with shape `(32, 3, 64, 64)`, no different in kind from the scalar `5.0`.

The two most basic operations, elementwise addition and elementwise multiplication, both require their inputs to share a shape (ignoring, for now, the broadcasting rules a later track covers): the operation is applied independently at every matching position, so the output has that same shape too.

```text
elementwise_add([1, 2, 3], [10, 20, 30]) = [11, 22, 33]
elementwise_multiply([1, 2, 3], [10, 20, 30]) = [10, 40, 90]
```

Elementwise multiplication is deliberately NOT the same thing as matrix multiplication (`a @ b`), a different, less positionally-obvious operation that a later question in this track covers on its own.

### How PyTorch actually implements this

`x.shape` and `x.ndim` on a real `torch.Tensor` aren't Python bookkeeping bolted on after the fact, they're read directly off the tensor's C++ metadata (`TensorImpl`'s `sizes()` and `dim()`), the same metadata every kernel (matmul, convolution, elementwise add) consults before it ever touches a single number, to decide how to walk the underlying memory buffer. `+` and `*` on two tensors dispatch to fused elementwise CUDA/CPU kernels rather than a Python loop, which is exactly why "vectorized" code is both simpler to write and orders of magnitude faster than looping over positions yourself.

## Explanation

`shape_of` and `ndim_of` just expose NumPy's own `.shape` and `.ndim` attributes: no computation, only the vocabulary this whole curriculum is built on.

`elementwise_add` and `elementwise_multiply` use NumPy's own `+` and `*` operators, which are already elementwise by default (this is exactly what "vectorized" means: no explicit Python loop over positions).
