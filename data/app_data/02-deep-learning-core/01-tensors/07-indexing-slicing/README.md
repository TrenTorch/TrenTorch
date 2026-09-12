---
name: dl-core-indexing-slicing
title: Indexing / slicing
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

Implement:

```python
def basic_slice(a, start, stop) -> np.ndarray: ...
def boolean_mask(a, mask) -> np.ndarray: ...
def fancy_index(a, indices) -> np.ndarray: ...
def is_a_view_of(child, parent) -> bool: ...
```

## Theory

Three ways of indexing into a tensor/array _look_ similar (all three select a subset of elements) but have a genuinely important difference underneath: **basic slicing** (`a[2:5]`, a contiguous range with a fixed step) returns a **view**, a new array object that shares the same underlying memory as the original, no data is copied. **Boolean masking** (`a[mask]`) and **fancy (integer array) indexing** (`a[[1, 3, 5]]`) both return **copies**, genuinely new, independent memory.

```text
basic slice:        a[2:5]        -> VIEW, shares memory with a
boolean mask:        a[a > 0]      -> COPY, independent memory
fancy index:         a[[1, 3, 5]]  -> COPY, independent memory
```

Why this matters in practice: mutating a basic-slice view (`a[2:5] += 1`) changes the original array too, since they share memory, exactly the mutation-in-place behavior `01-hypothesis-function`'s constraints warned against elsewhere in this curriculum for a different reason. Mutating the result of a boolean mask or fancy index does _not_ affect the original, they're independent copies. This distinction is a real, common source of bugs, code that assumes "any indexed subset behaves the same way" will work fine for slicing and then silently fail (or silently succeed when it shouldn't) for masking or fancy indexing.

## Explanation

`basic_slice`/`boolean_mask`/`fancy_index` are each one line, `a[start:stop]`, `a[mask]`, `a[indices]`, NumPy's own indexing already implements the view/copy distinction Theory describes, there's nothing extra to do to get that behavior, it comes from which _kind_ of indexing expression is used.

`is_a_view_of` calls `np.shares_memory(child, parent)`, NumPy's own tool for checking whether two arrays' underlying memory buffers overlap, this is the actual, verifiable way to answer "is this a view or a copy," rather than relying on assumption or documentation alone.
