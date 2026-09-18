---
name: dl-core-reshape-transpose
title: Reshape / transpose
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The same set of numbers can be organized into many different shapes — 12 elements can be viewed as a flat vector of 12, a 3x4 grid, or a 2x2x3 block — without changing which numbers exist, only how they're grouped into dimensions. Every layer in a real network reshapes and reorders its tensors constantly (flattening before a `Linear` layer, moving a "channels" dimension around for a convolution), so these three operations are the vocabulary everything else in this curriculum is built out of.

### From theory to code

Implement `reshape(a, shape)`, `transpose(a, dim0, dim1)`, and `permute(a, dims)`. `transpose` and `permute` look similar but are genuinely different operations, not a generalization with a default — implement each exactly, not one in terms of the other.

### Constraints

- `a`: any NumPy array. `shape` may contain a single `-1`, meaning "infer this dimension from the total element count."
- `transpose(a, dim0, dim1)` swaps exactly the two named dimensions; every other dimension stays exactly where it is.
- `permute(a, dims)` reorders every dimension at once according to `dims` — a full reordering, not a two-axis swap.
- `reshape` preserves element order (the same flat sequence of values, regrouped).
- None of the three mutate `a`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`reshape` needs no manual `-1` handling — NumPy's own `.reshape()` already supports a single inferred dimension, the same convention `torch.reshape` uses.

</details>

<details>
<summary>Hint 2</summary>

`transpose` and `permute` are two different NumPy functions, not the same function called two ways: one swaps a pair of axes, the other takes a full axis ordering.

</details>

## Theory

### The simple version

`reshape` changes how the _same_ underlying elements are grouped into dimensions — 12 elements can be viewed as `(12,)`, `(3, 4)`, `(2, 2, 3)`, or anything else whose sizes multiply to `12`, without moving or copying any actual values conceptually (though the real underlying memory layout may or may not need an actual copy, depending on whether the requested shape is compatible with the existing memory strides). `-1` in one position means "figure this dimension out from everything else" — `reshape((2, -1))` on `12` elements infers `6` for the second dimension.

`transpose` and `permute` are a common source of confusion because they look similar but do different things:

```text
transpose(a, 0, 2):   swaps ONLY dimensions 0 and 2, dimension 1 (and any others) stay exactly where they are
permute(a, (2, 0, 1)): dimension 2 becomes the new dim 0, dimension 0 becomes the new dim 1, dimension 1 becomes the new dim 2 -- ALL dimensions move at once
```

### The formula

`transpose` is the right tool when exactly two axes need to swap (a very common single-swap case, like moving a "channels" dimension). `permute` is the right tool for an arbitrary full reordering, and it's a strict generalization — any `transpose` call can be written as a `permute` call, but not vice versa in general (a 3+ dimensional permutation can move three or more axes simultaneously in a way no single two-axis swap achieves).

### How PyTorch actually implements this

Context only, untested by your submission: `torch.reshape`, `torch.transpose(a, dim0, dim1)`, and `a.permute(*dims)` are exactly these three operations, with the same `-1`-infers-a-dimension convention for reshape and the same swap-vs-full-reorder distinction between `transpose` and `permute`.

## Explanation

`reshape` is `a.reshape(shape)` directly — NumPy's own `-1` inference rule already matches `torch.reshape`'s.

`transpose` calls `np.swapaxes(a, dim0, dim1)`, which does exactly the "swap these two, leave everything else" operation `torch.transpose` performs, not a full reversal of every axis.

`permute` calls `np.transpose(a, dims)` (NumPy's `np.transpose` with an explicit `axes` argument is the general permutation operation — confusingly sharing its name with the two-axis `torch.transpose`, they are not the same operation despite the name overlap), reordering every dimension according to `dims` in one call.
