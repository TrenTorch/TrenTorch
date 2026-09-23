---
name: python-tuples-vs-lists
title: "Tuples vs Lists: When Immutability Decides"
tags: [python-tuples, python-lists]
difficulty: Intermediate
---

## Statement

Implement functions that convert between lists and tuples and produce modified copies of either type without changing the original, and that detect when a tuple still contains mutable objects.

## Theory

Lists and tuples both store ordered sequences of addresses. They differ in exactly one property: a list's slots can be changed after creation, a tuple's cannot. That decides which is appropriate — a tuple for a fixed group of related values, a value several places share, a dictionary key, or several return values; a list for anything that grows, shrinks, or is reordered.

**Safety from aliasing.** A list passed to a function can be mutated by that function, and the caller sees it. A tuple cannot be mutated, so the caller's data is guaranteed unchanged unless the function returns a new tuple.

**Immutability is shallow.** A tuple guarantees its **own slots** don't change — it does not guarantee the objects inside it are immutable:

```python
t = ([1, 2], [3])
t[0].append(99)        # t is now ([1, 2, 99], [3]); t's slots never changed
```

**Testing a type.** `isinstance(obj, tuple)` / `isinstance(obj, list)` are the direct way to write code that treats the two differently.

**Converting.** `tuple(seq)` and `list(seq)` build a new object of the other type. Conversions are **shallow**: the elements are shared, not copied — to convert a nested list to a nested tuple, each inner list must be converted too.

**Where this matters later.** Choosing an immutable value for something that should never change removes a category of bugs, and is what makes those values usable as dictionary keys.

## Explanation

`updated` converts `seq` to a plain `list` unconditionally, mutates that working copy (skipping the assignment via a caught `IndexError` when `index` is out of range), then converts back to `tuple` only if the original was a tuple — one code path handles both input types instead of duplicating the "replace, but skip if out of range" logic per type. `has_mutable_element` checks only the tuple's *direct* elements against `(list, dict, set)`, not elements nested inside an inner tuple, matching the spec's own "check only the direct elements" scope.
