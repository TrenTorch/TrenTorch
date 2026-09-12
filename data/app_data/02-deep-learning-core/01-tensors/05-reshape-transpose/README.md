---
name: dl-core-reshape-transpose
title: Reshape / transpose
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

Implement:

```python
def reshape(a, shape) -> np.ndarray: ...
def transpose(a, dim0, dim1) -> np.ndarray: ...
def permute(a, dims) -> np.ndarray: ...
```

- `shape` may contain a single `-1`, meaning "infer this dimension from the total element count."
- `transpose` swaps exactly the two named dimensions. `permute` reorders every dimension at once, according to `dims`, a genuinely different operation, not just a generalization with a default.

## Theory

`reshape` changes how the _same_ underlying elements are grouped into dimensions, `12` elements can be viewed as `(12,)`, `(3, 4)`, `(2, 2, 3)`, or anything else whose sizes multiply to `12`, without moving or copying any actual values conceptually (though the real underlying memory layout may or may not need an actual copy, depending on whether the requested shape is compatible with the existing memory strides). `-1` in one position means "figure this dimension out from everything else," `reshape((2, -1))` on `12` elements infers `6` for the second dimension.

`transpose` and `permute` are a common source of confusion because they look similar but do different things:

```text
transpose(a, 0, 2):   swaps ONLY dimensions 0 and 2, dimension 1 (and any others) stay exactly where they are
permute(a, (2, 0, 1)): dimension 2 becomes the new dim 0, dimension 0 becomes the new dim 1, dimension 1 becomes the new dim 2 -- ALL dimensions move at once
```

`transpose` is the right tool when exactly two axes need to swap (a very common single-swap case, like moving a "channels" dimension). `permute` is the right tool for an arbitrary full reordering, and it's a strict generalization, any `transpose` call can be written as a `permute` call, but not vice versa in general (a 3+ dimensional permutation can move three or more axes simultaneously in a way no single two-axis swap achieves).

## Explanation

`reshape` is `a.reshape(shape)` directly, NumPy's own `-1` inference rule already matches `torch.reshape`'s.

`transpose` calls `np.swapaxes(a, dim0, dim1)`, which does exactly the "swap these two, leave everything else" operation `torch.transpose` performs, not a full reversal of every axis.

`permute` calls `np.transpose(a, dims)` (NumPy's `np.transpose` with an explicit `axes` argument is the general permutation operation, confusingly sharing its name with the two-axis `torch.transpose`, they are not the same operation despite the name overlap), reordering every dimension according to `dims` in one call.
