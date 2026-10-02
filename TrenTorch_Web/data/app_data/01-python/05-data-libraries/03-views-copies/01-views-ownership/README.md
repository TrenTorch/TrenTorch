---
name: numpy-views-ownership
title: 'Views & Ownership'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that inspect two arrays and report whether one is a view of the other's underlying buffer, and that determine whether an array owns its data or is a view into another array, locating the ultimate owner.

## Theory

### What a view is

A **view** is a second, independent ndarray object, with its own shape and starting position, that describes the _same underlying buffer_ as another array, rather than owning a freshly allocated buffer of its own.

```
buffer:            [ 0 | 1 | 2 | 3 | 4 | 5 ]
arr    shape (6,)  starts at position 0
view   shape (3,)  starts at position 3
```

`arr` and `view` are two distinct Python objects, but they are not two distinct sets of data, reading or writing through either reads or writes the same memory cells. This is exactly why a slice can behave like an alias despite being a "new" ndarray object: the object is new, the buffer it points at is not.

### Who owns the data

Every ndarray has a `.base` attribute:

- If an array **owns** its data, `.base` is `None`.
- If an array **is a view**, `.base` refers to the array it was derived from.

```python
arr = np.arange(10)
arr.base          # None, arr owns its buffer

view = arr[2:5]
view.base is arr   # True
```

**For a chain of views, `.base` does not necessarily point all the way back to the ultimate original**, it points only to whatever it was most directly created from, which might itself be a view.

```python
view1 = arr[1:8]
view2 = view1[2:5]

view2.base is view1     # True, immediate base
view2.base is arr        # False, not directly
```

To find the true root, follow `.base` repeatedly until reaching an array whose `.base` is `None`.

## Explanation

`is_view_of` is a one-line call to `np.shares_memory(candidate, source)`, which answers exactly this question directly rather than needing any manual reasoning about slices or offsets. Sharing a buffer is symmetric, so the check gives the same answer regardless of argument order.

`owns_its_data` checks `arr.base is None`. `find_ultimate_owner` walks a `while current.base is not None: current = current.base` loop starting from `arr`, returning `current` once the loop ends, if `arr` already owns its data, the loop body never runs and `arr` itself is returned.
