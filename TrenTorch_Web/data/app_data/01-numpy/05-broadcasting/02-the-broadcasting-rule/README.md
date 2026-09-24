---
name: numpy-the-broadcasting-rule
title: The Broadcasting Rule, Precisely
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement a function that determines, given two array shapes, whether they are compatible for broadcasting and what the resulting broadcast shape would be — implementing NumPy's rule directly.

## Theory

NumPy compares two shapes **dimension by dimension, starting from the trailing (rightmost) dimension and working backward**. For each aligned pair, they're compatible if:

- They are exactly equal, **or**
- One of them is exactly `1` (stretched to match), **or**
- One array has no dimension at that position at all (shorter shape, treated as padded with `1`s on the left)

If neither dimension is `1` and they aren't equal at some aligned position, the shapes are **not** broadcastable.

```
matrix shape:  (2, 3)
addend shape:     (3,)
padded addend:  (1, 3)     ← treated as if this leading dim exists

position -1:  3 vs 3  → equal, compatible
position -2:  2 vs 1  → one side is 1, compatible

result shape: (2, 3)
```

The resulting broadcast shape takes, at each position, whichever of the two sizes is **not** `1` (or either, if equal). This applies independently at every dimension position, for any number of dimensions.

## Explanation

Both functions pad the shorter shape with leading `1`s (using `(1,) * (len(longer) - len(shorter))` or by reversing, zipping with `itertools.zip_longest(fillvalue=1)`, and reversing back) so both shapes have equal length, then walk pairs right-to-left. `are_broadcastable` returns `False` as soon as a pair is neither equal nor has a `1`; `broadcast_result_shape` takes `max(a, b)` at each aligned position (valid since compatibility guarantees one side is `1` or they're equal).
