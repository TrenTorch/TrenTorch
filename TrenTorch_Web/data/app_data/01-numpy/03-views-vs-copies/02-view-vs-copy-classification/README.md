---
name: numpy-view-vs-copy-classification
title: Which Operations Return a View vs a Copy
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement a function that classifies a range of NumPy operations as producing a view or a copy, by actually performing the operation and checking shared memory.

## Theory

Whether an operation returns a view or a copy comes down to one question: **can the resulting selection be described purely as a starting position plus a fixed step pattern within the existing buffer?** If yes, it's a view. If the selection is irregular, reordered, or requires computing new values, NumPy must allocate a new buffer.

**Returns a view:** basic slicing (`arr[2:5]`, `arr[::2]`), `.T`/`transpose()`, `reshape()`/`ravel()` when the layout allows it.

**Returns a copy:** `np.array()` on an existing array, fancy indexing (`arr[[0, 2, 4]]`), boolean masking (`arr[arr > 5]`), any arithmetic (`arr + 1`), `.copy()`, `flatten()`.

**The rule:** selecting a regular pattern of existing values → view. Selecting an irregular pattern, or computing new values → copy.

## Explanation

Perform the named operation, then check `np.shares_memory(result, arr)` — `"view"` if `True`, `"copy"` if `False`. This checks the real observed behavior rather than relying on a hardcoded lookup table, which also correctly handles the boolean-mask case where the mask happens to select every element (it's still a copy, since the operation itself is the deciding factor, not how much data it selects).
