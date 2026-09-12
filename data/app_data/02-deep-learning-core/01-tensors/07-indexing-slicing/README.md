---
name: dl-core-indexing-slicing
title: Indexing / slicing
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Three ways of indexing into a tensor/array *look* similar (all three select a subset of elements), but they have a genuinely important difference underneath: some return a *view* into the original memory, others return an independent *copy*. Code that treats every indexed subset the same way will work fine for one kind and silently misbehave for another the moment it mutates the result.

### From theory to code

Implement `basic_slice`, `boolean_mask`, `fancy_index`, and `is_a_view_of` — a way to actually verify, rather than assume, whether a given result shares memory with its source.

### Constraints

- `basic_slice(a, start, stop)` returns `a[start:stop]`, sharing memory with `a`.
- `boolean_mask(a, mask)` and `fancy_index(a, indices)` both return independent copies, not sharing memory with `a`.
- `is_a_view_of(child, parent)` returns a plain `bool`: `True` iff `child` and `parent` share underlying memory.
- None of the four mutate their inputs directly (though a caller mutating a returned *view* will, by definition, affect the original — that's the point being tested).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

None of the three indexing functions need any logic beyond the indexing expression itself — the view-vs-copy behavior comes from NumPy, based purely on which *kind* of indexing syntax is used.

</details>

<details>
<summary>Hint 2</summary>

`is_a_view_of` doesn't need to inspect strides or offsets by hand — NumPy has a function whose entire job is answering exactly this question.

</details>

## Theory

### The simple version

Basic slicing (`a[2:5]`, a contiguous range with a fixed step) returns a **view**, a new array object that shares the same underlying memory as the original — no data is copied. Boolean masking (`a[mask]`) and fancy (integer array) indexing (`a[[1, 3, 5]]`) both return **copies**, genuinely new, independent memory:

```text
basic slice:  a[2:5]        -> VIEW, shares memory with a
boolean mask: a[a > 0]      -> COPY, independent memory
fancy index:  a[[1, 3, 5]]  -> COPY, independent memory
```

### The formula

Why this matters in practice: mutating a basic-slice view (`a[2:5] += 1`) changes the original array too, since they share memory — exactly the mutation-in-place behavior `01-hypothesis-function`'s constraints warned against elsewhere in this curriculum for a different reason. Mutating the result of a boolean mask or fancy index does *not* affect the original — they're independent copies. This distinction is a real, common source of bugs: code that assumes "any indexed subset behaves the same way" will work fine for slicing and then silently fail (or silently succeed when it shouldn't) for masking or fancy indexing.

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch tensors follow the same view-vs-copy split — basic slicing on a tensor returns a view (mutating it affects the original, and it shows up in autograd as sharing the same underlying storage), while boolean masking and advanced indexing return new tensors. `tensor_a.data_ptr()` comparisons (or `.is_set_to()`) are PyTorch's rough equivalent of checking shared storage, analogous to this exercise's `np.shares_memory`.

## Explanation

`basic_slice`/`boolean_mask`/`fancy_index` are each one line, `a[start:stop]`, `a[mask]`, `a[indices]` — NumPy's own indexing already implements the view/copy distinction Theory describes, there's nothing extra to do to get that behavior, it comes from which *kind* of indexing expression is used.

`is_a_view_of` calls `np.shares_memory(child, parent)`, NumPy's own tool for checking whether two arrays' underlying memory buffers overlap — this is the actual, verifiable way to answer "is this a view or a copy," rather than relying on assumption or documentation alone.
