---
name: numpy-the-base-attribute
title: The .base Attribute
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that use an array's `.base` attribute to determine whether it owns its data or is a view into another array, and to locate the ultimate original array at the root of a chain of views.

## Theory

Every ndarray has a `.base` attribute:

- If an array **owns** its data, `.base` is `None`.
- If an array **is a view**, `.base` refers to the array it was derived from.

```python
arr = np.arange(10)
arr.base          # None — arr owns its buffer

view = arr[2:5]
view.base is arr   # True
```

**For a chain of views, `.base` does not necessarily point all the way back to the ultimate original** — it points only to whatever it was most directly created from, which might itself be a view.

```python
view1 = arr[1:8]
view2 = view1[2:5]

view2.base is view1     # True — immediate base
view2.base is arr        # False — not directly
```

To find the true root, follow `.base` repeatedly until reaching an array whose `.base` is `None`.

## Explanation

`owns_its_data` checks `arr.base is None`. `find_ultimate_owner` walks a `while current.base is not None: current = current.base` loop starting from `arr`, returning `current` once the loop ends — if `arr` already owns its data, the loop body never runs and `arr` itself is returned.
