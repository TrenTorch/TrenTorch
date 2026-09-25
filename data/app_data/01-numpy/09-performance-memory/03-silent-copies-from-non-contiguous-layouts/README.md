---
name: numpy-silent-copies-from-non-contiguous-layouts
title: Silent Copies From Non-Contiguous Layouts
tags: [numpy-memory]
difficulty: Advanced
---

## Statement

Implement functions that detect when `reshape` or `ravel` silently copies because of a non-contiguous layout, force contiguity once when it is needed, and observe how a silent copy breaks write-through behavior.

## Theory

A view can only describe data arranged by **one fixed stride per axis**. If the requested reshape's logical order cannot be described that way over the existing buffer, NumPy allocates a new buffer and copies — **silently**, with no error or warning.

```python
arr = np.arange(6).reshape(2, 3)
t = arr.T                    # shape (3, 2), strides (8, 24)
t.reshape(6)                  # no single stride visits 0,3,1,4,2,5 — must copy
```

A C-contiguous array can always be reshaped to any valid shape as a view.

**Detecting copies.** Use `np.shares_memory(a, b)` — a reshape copied exactly when `np.shares_memory(arr, arr.reshape(new_shape))` is `False`. `.base` is not reliable for this, since a copying result can still report a base.

**Paying for contiguity once.** `np.ascontiguousarray(arr)` returns `arr` itself (no copy) if already C-contiguous, otherwise a C-contiguous copy.

`ravel` follows the same view-or-copy rule as `reshape`; `flatten` always copies regardless of layout.

## Explanation

`reshape_copies` and `ravel_copies` perform the operation and check `not np.shares_memory(arr, result)`. `ensure_contiguous` is `np.ascontiguousarray(arr)` directly — it never mutates `arr`, since it either returns `arr` unchanged or a fresh copy. `reshape_write_propagates` reshapes, writes `result[:] = value`, then checks whether `arr` itself now contains `value` everywhere — `True` only when the reshape was a view (write-through), `False` when it silently copied.
