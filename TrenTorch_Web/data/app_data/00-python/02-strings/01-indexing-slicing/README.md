---
name: python-strings-indexing-slicing
title: String Objects, Indexing, and Slicing
tags: [python-strings, indexing]
difficulty: Beginner
---

## Statement

Implement functions that read individual characters and sub-sections out of a string using indices and slices, including negative positions and steps.

## Theory

A string is an object of type `str`. Its value is an ordered sequence of characters. Every character is itself a `str` object of length 1, so there is no separate "character" type.

`len(s)` returns the number of characters as an `int`.

**Indexing.** Each character has a position, called an index. Indices start at `0`. A negative index counts from the end, so `-1` is the last character.

```
 index      0    1    2    3    4    5
          ┌────┬────┬────┬────┬────┬────┐
 "python" │ p  │ y  │ t  │ h  │ o  │ n  │
          └────┴────┴────┴────┴────┴────┘
 negative  -6   -5   -4   -3   -2   -1
```

`s[0]` is `"p"` and `s[-1]` is `"n"`. Using an index outside the valid range produces an `IndexError` (error handling is covered later in this module set).

**Slicing.** `s[start:stop:step]` builds a **new string** from the characters at positions `start`, `start + step`, `start + 2*step`, ... up to but **not including** `stop`.

```python
s[1:4]      # "yth"   positions 1, 2, 3
s[:3]       # "pyt"   start defaults to the beginning
s[3:]       # "hon"   stop defaults to the end
s[-3:]      # "hon"   the last three characters
s[::2]      # "pto"   every second character
s[::-1]     # "nohtyp" negative step walks backward; whole string reversed
```

Rules for the three parts:

- A negative `start` or `stop` has `len(s)` added to it.
- A `start` or `stop` beyond the string is **clamped** to the valid range — it never causes an error, unlike a single out-of-range index. `"abc"[1:100]` is `"bc"`.
- With a positive step, defaults are `start = 0` and `stop = len(s)`. With a negative step, defaults are `start = len(s) - 1` and the slice runs back past index `0`.
- `step` cannot be `0`.

A slice always creates a new object at a new address; the original is never changed.

**Where this matters later.** The `start:stop:step` syntax is the same syntax lists use and the same syntax NumPy arrays use for selecting regions of tensors.

## Explanation

`first_and_last` handles the empty and single-character cases as explicit early returns rather than trying to make `s[0]`/`s[-1]` "just work" for them — indexing an empty string always raises `IndexError`, so those cases can't be folded into the general path. `every_kth_from` relies entirely on Python's own slice clamping (`s[start::k]`) rather than manually validating `start`, since the clamping rule the theory describes already produces `""` for an out-of-range `start` without any extra code.
