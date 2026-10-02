---
name: python-lists-indexing-slicing-assignment
title: List Objects, Indexing, Slicing, and Slice Assignment
tags: [python-lists, indexing]
difficulty: Beginner
---

## Statement

Implement functions that read and rewrite sections of a list using indices, slices, and slice assignment, keeping track of when a new list is created and when the existing one is changed.

## Theory

A **list** is a **mutable** object of type `list` that holds an ordered sequence of elements. A list object does not contain its elements' data directly — it contains one **slot** per element, and each slot stores the **address** of an element object.

**Indexing and slicing** follow the same rules as strings: indices start at `0`, negative indices count from the end, and `lst[start:stop:step]` has an inclusive start, exclusive stop, and clamped bounds. Two differences come from mutability:

- `lst[i]` returns the object whose address is stored in slot `i`. The element is not copied.
- A slice builds a **new list** whose slots store the same addresses as the selected slots of the original — the list object is new, the elements are shared.

**Assigning to an index** replaces the address stored in one slot — mutation of the list object:

```python
lst[0] = 99        # slot 0 now stores the address of the int 99; lst keeps its own address
```

**Slice assignment** replaces a section of the list with the elements of an iterable, in place. The replacement may be shorter or longer than the section it replaces, so the list can shrink or grow:

```python
nums = [0, 1, 2, 3, 4]
nums[1:3] = [10, 20, 30]      # [0, 10, 20, 30, 3, 4]   length grew
nums[1:3] = []                # [0, 30, 3, 4]           length shrank
```

With an **extended slice** (a step other than `1`), the replacement must have exactly as many elements as the slice selects, or a `ValueError` is produced:

```python
nums = [0, 1, 2, 3, 4]
nums[::2] = ["a", "b", "c"]   # ["a", 1, "b", 3, "c"]
```

**Where this matters later.** In NumPy, `arr[1:3] = value` writes into the array in place, the same operation — except a NumPy slice selects the _same_ memory instead of building a new list.

## Explanation

`replace_middle` uses slice assignment on `lst[1:-1]` rather than building a brand-new list and reassigning `lst` to it — the whole point is that slice assignment mutates the existing list object in place, which the hidden tests confirm by checking `id(lst)` is unchanged after the call. `set_every_other` needs the replacement to have exactly as many elements as the extended slice selects (`lst[::2]`), so it builds `[value] * len(lst[::2])` rather than a fixed-size list, which would raise `ValueError` on any list whose length doesn't happen to match.
