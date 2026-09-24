---
name: python-sets-objects-unique
title: Set Objects and How They Store Unique Elements
tags: [python-sets]
difficulty: Beginner
---

## Statement

Implement functions that create sets, inspect their contents, and demonstrate that a set stores each distinct element only once.

## Theory

A **set** is a mutable object that stores a collection of **unique elements**, with no ordered sequence — each element appears at most once, and the display order isn't meaningful.

**Creating.** `{1, 2, 3}` and `set(iterable)` both work, but `{}` creates an empty **dictionary**, not a set — `set()` is the only way to write an empty set.

```python
set([1, 2, 2, 3])     # {1, 2, 3}
set("hello")           # {'h', 'e', 'l', 'o'}
```

**Elements must be hashable.** Numbers, strings, and tuples of hashables can be elements; a list cannot (`{[1, 2]}` raises `TypeError`), since it's mutable and can't provide a stable hash.

**Membership** is the operation a set is designed for:

```python
10 in {10, 20, 30}       # True
```

Set membership uses hashing to locate the element, not sequential scanning — this is why a set answers "have I seen this value?" efficiently regardless of size.

**No indexing or slicing.** `s[0]` and `s[1:3]` both raise `TypeError` — a set has no sequence positions.

**Equality.** Two sets are equal when they contain exactly the same elements, regardless of how they were written: `{1, 2, 3} == {3, 1, 2}`.

**Where this matters later.** Sets are useful whenever a program needs uniqueness or repeated membership tests — tracking which IDs have already been processed, removing duplicates, checking whether a token has appeared in a dataset.

## Explanation

`unique_values` and `unique_count` both go through `set(values)` rather than a manual dedup loop — passing any iterable straight to `set()` is exactly what removes duplicates, since a set can never hold two equal elements to begin with. `contains_all` converts `values` to a set before testing membership for each candidate, which is what the spec's own hint calls for — testing membership against a list instead would still be correct, just not exercise the hash-based lookup this topic is about.
