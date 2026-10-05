---
name: numpy-shared-memory-copies
title: 'Shared Memory & Independent Copies'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that deliberately use a view's shared-memory behavior to mutate an original array indirectly, show how mutation through one view appears in another and break the sharing relationship with an explicit copy.

## Theory

### Mutating through a view

Because a view shares its buffer with its source, mutating a view's contents mutates that shared buffer, visible through every other array describing the same region.

```python
arr = np.arange(10)
first_half = arr[:5]        # a view
first_half[:] = 0            # mutate every element of the view
print(arr)     # [0, 0, 0, 0, 0, 5, 6, 7, 8, 9]
```

`first_half[:] = 0` mutates the shared buffer; `first_half = 0` would just rebind the Python variable and touch nothing shared. The `[:]` (or any indexing on the left of `=`) is what makes it an in-place mutation.

**Views can be chained**, and mutating at any point affects everything else in the chain:

```python
arr = np.arange(10)
view1 = arr[2:8]
view2 = view1[1:4]     # a view of a view

view2[0] = -1
print(arr)     # corresponding position is now -1
print(view1)   # also reflects the change
```

### Forcing an independent copy

`.copy()` produces a completely independent array: a fresh buffer holding the same values, with no ongoing connection to the array it was called on.

```python
arr = np.arange(6)
view = arr[2:5]           # shares memory with arr
independent = view.copy()  # does NOT share memory with arr

independent[0] = 99
print(arr)     # unaffected
```

`.copy()` works regardless of whether the array it's called on is itself a view or already owns its data, either way, the result is a new, independent buffer. A common pattern combines cheap slicing with `.copy()` only at the exact point independence is actually needed:

```python
region = data[10:20].copy()
```

## Explanation

`zero_out_via_view` slices `arr[start:stop]` to get a view, then assigns `view[:] = 0`, writing through the view mutates `arr`'s shared buffer directly, no reassignment of `arr` itself. `chained_view_mutation` builds `view1 = arr[1:7]`, `view2 = view1[2:5]`, mutates `view2[:] = -1`, and returns all three post-mutation, since `view2`'s buffer positions are also covered by `view1` and `arr`, all three reflect the change at the overlapping positions.

`get_independent_slice` chains a slice with `.copy()` in one expression (`arr[start:stop].copy()`). `safe_modify_first_n` calls `.copy()` on `arr` first to get an independent array, then mutates the first `n` elements of that copy via slice assignment (`result[:n] = new_value`) and returns it, `arr` itself is never touched.
