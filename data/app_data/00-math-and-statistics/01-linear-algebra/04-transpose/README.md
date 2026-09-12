---
name: math-transpose
title: 'Transpose, and its role in reshaping without copying data'
tags: [linear-algebra, matrices]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`03-matrix-multiplication` required `a`'s columns to match `b`'s rows. Real data doesn't always arrive in the shape an operation needs: `weight` in a linear layer is stored as `(out_features, in_features)`, one row per output neuron, but matrix-multiplying it against a `(batch, in_features)` input needs `in_features` to line up as the _shared_ dimension on both sides. Something has to flip `weight`'s two axes first, without which `linear` (this curriculum's very first question) simply couldn't be written as one matmul.

That flip is the transpose. The part that makes it worth its own question, beyond "flip the axes", is that a correct implementation does this essentially for free: no new memory allocated, no numbers moved, just a different way of reading the same bytes.

### From theory to code

Theory defines the transpose (`x[i, j] -> x.T[j, i]`) and explains, at the memory level, why it costs nothing. Implement `transpose`, and a helper that verifies the "no copy" claim directly by checking shared memory.

Implement `transpose(x)` and `is_a_view_of(original, derived)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `transpose` only needs to handle 2D input (a full N-D `.transpose(dims)` is a later Deep Learning Core question).
- `is_a_view_of` must check actual shared memory, not just equal values, two separately-allocated arrays holding identical numbers are not "the same view."

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

NumPy arrays already expose the transpose as a one-character attribute. You are not asked to build it from index arithmetic.

</details>

<details>
<summary>Hint 2</summary>

There's a NumPy function whose entire job is answering "do these two arrays' buffers overlap," which is exactly what "is this a view" means.

</details>

## Theory

### The simple version

Picture a spreadsheet with rows for students and columns for exam scores. Now imagine you need the same information laid out the other way, rows for exams, columns for students, without literally retyping every number into a new sheet. Transpose is exactly that: read the same data, indexed the other way around.

### The formula

The transpose of an `(m, n)` matrix is the `(n, m)` matrix obtained by flipping it over its diagonal:

```text
x[i, j]  ->  x.T[j, i]
```

`linear`, this curriculum's very first question, already uses this: `input @ weight.T` transposes `weight` so its rows (one per output feature) become columns, making the shapes line up for matrix multiplication.

The detail worth internalizing here, not just the definition: **transpose does not copy data.** An array in memory is a flat buffer of numbers plus a "stride" (how many bytes to skip to move one step along each axis). Transposing just swaps the strides, it hands back a new array _object_ that reads the exact same bytes in a different order, without moving a single number. This is why transpose is essentially free no matter how large the matrix is, and why it composes so cheaply with other operations: a chain of `.T` calls costs nothing until something actually forces a read (like `+` or `@`).

This "view, not copy" behavior is not unique to transpose, `02-deep-learning-core`'s own indexing/slicing question covers the general view-vs-copy distinction across NumPy operations; transpose is simply the first, most common place a student runs into it.

### How PyTorch actually implements this

`x.T` (or `x.transpose(0, 1)`) on a real `torch.Tensor` mutates only the tensor's metadata, its `sizes` and `strides` fields, and leaves the underlying `Storage` untouched, exactly the "same buffer, different reading order" idea from Theory. This is why PyTorch has an entire category of methods called "view operations" (`.view()`, `.transpose()`, `.permute()`, `.squeeze()`), and why one of the most common real PyTorch errors is calling `.view()` on a tensor whose strides a prior transpose made non-contiguous, `.reshape()` or an explicit `.contiguous()` call is needed there instead, precisely because the data underneath is still laid out in its original order.

## Explanation

`transpose` returns `x.T`, NumPy's own view-based transpose.

`is_a_view_of` calls `np.shares_memory(original, derived)`, which inspects the two arrays' underlying buffers directly rather than comparing values, the correct way to check "is this the same data, read differently" instead of "do these two arrays currently hold equal numbers" (two independently-copied arrays could hold equal values without sharing memory at all).
