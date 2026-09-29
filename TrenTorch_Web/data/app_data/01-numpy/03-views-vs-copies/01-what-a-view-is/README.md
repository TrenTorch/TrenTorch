---
name: numpy-what-a-view-is
title: What a View Actually Is
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement a function that inspects two ndarray objects and reports whether one is a view of the other's underlying buffer.

## Theory

A **view** is a second, independent ndarray object — with its own shape and starting position — that describes the _same underlying buffer_ as another array, rather than owning a freshly allocated buffer of its own.

```
buffer:            [ 0 | 1 | 2 | 3 | 4 | 5 ]
arr    shape (6,)  starts at position 0
view   shape (3,)  starts at position 3
```

`arr` and `view` are two distinct Python objects, but they are not two distinct sets of data — reading or writing through either reads or writes the same memory cells. This is exactly why a slice can behave like an alias despite being a "new" ndarray object: the object is new, the buffer it points at is not.

## Explanation

`is_view_of` is a one-line call to `np.shares_memory(candidate, source)`, which answers exactly this question directly rather than needing any manual reasoning about slices or offsets. Sharing a buffer is symmetric, so the check gives the same answer regardless of argument order.
