---
name: python-numpy-bridge-views-vs-copies
title: Views vs Copies
tags: [python-numpy-bridge]
difficulty: Intermediate
---

## Statement

Implement a `View` class that reads and writes a shared list through an index range, and functions that show which operations change the underlying data and which produce independent copies.

## Theory

A **buffer** is the block of memory (here, a list) that actually holds values. A **view** refers to a buffer plus a rule for which positions it exposes — it stores no values of its own. A **copy** has its own separate buffer. Writing through a view changes the buffer, and therefore everything else viewing that same buffer.

**Building a view with `range`.** A `range` supports `len()` and indexing (negative included), and slicing a `range` gives another `range`:

```python
r = range(0, 10)
r[2:8:2]              # range(2, 8, 2)
range(2, 8, 2)[1:]     # range(4, 8, 2) -- a slice of a slice, still a range
```

A view keeps the buffer plus a `range` of buffer positions — element `i` of the view is `buffer[indices[i]]`, and slicing the view slices `indices`, producing another view of the *same* buffer.

**How array libraries behave.** `arr[1:4]` (basic slicing) is a view — writing to it writes into `arr`. `.copy()` (NumPy) / `.clone()` (PyTorch) makes it independent. Selecting by an arbitrary list of positions or a boolean mask produces a copy, since those selections aren't a regular start/stop/step.

**Where this matters later.** Forgetting a slice is a view causes silent bugs — normalizing a slice of a dataset and altering the original, or modifying a cached tensor through a view of it.

## Explanation

`View.__getitem__` slices `self.indices` (a range) rather than building a new list of positions — slicing a range yields another range in $O(1)$, and passing it straight into a new `View` on the *same* `self.buffer` is exactly what makes the slice a view rather than a copy. `scale_in_place` writes back through `view[i] = ...` for every position, so the mutation lands in the shared buffer via `__setitem__`; `scaled_copy` instead reads through `view.to_list()` first (a real, separate list) and builds a brand-new list from that, so nothing it does can touch the buffer.
