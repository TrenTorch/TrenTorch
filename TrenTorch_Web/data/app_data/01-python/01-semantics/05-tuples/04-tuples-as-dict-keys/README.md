---
name: python-tuples-as-dict-keys
title: Tuples as Dictionary Keys
tags: [python-tuples, python-dicts]
difficulty: Intermediate
---

## Statement

Implement functions that use tuples as keys in a dictionary, relying on the fact that equal immutable tuples are interchangeable as keys.

## Theory

A **dictionary** stores key-value pairs; lookup by key is direct, without scanning. Reading a key that isn't present produces a `KeyError`, which is why code tests with `in` first.

**Hashing.** A dictionary locates a key by computing an integer from it with `hash()`. This requires: equal objects have equal hashes, and an object's hash must never change while it's in use as a key. Mutable containers (lists, dicts, sets) can't provide a stable hash, so they aren't allowed as keys:

```python
hash((1, 2))           # an int
hash([1, 2])           # TypeError: unhashable type: 'list'
```

**Tuples as keys.** A tuple is hashable **if all of its elements are hashable**. Two separately created tuples with equal contents are equal and have equal hashes, so they select the **same** dictionary entry even though they are different objects:

```python
grid = {}
grid[(2, 5)] = "wall"
grid[(2, 5)]          # "wall"    a different tuple object with equal contents finds the entry
```

A tuple containing a list is **not** hashable.

**Practical use.** Coordinates `(row, col)` are natural keys. When order shouldn't matter, build a **canonical** tuple (e.g. the smaller value first) before using it as a key.

**Floor division.** `a // b` divides and rounds **down** to an `int`: `7 // 2` is `3`, and `-7 // 2` is `-4` — useful for mapping coordinates to grid cells.

## Explanation

`edge_key` returns `(min(a, b), max(a, b))` rather than an `if`/`else` on `a < b`, since that already guarantees the symmetric property the spec requires (`edge_key(a, b) == edge_key(b, a)`) including the equal-endpoints case, without a separate branch. `group_points_by_cell` computes each cell key with plain `//` (not a rounding function), which is exactly why a coordinate like `-1` maps to cell `-1` rather than `0` — `//` always rounds toward negative infinity, unlike truncating division.
