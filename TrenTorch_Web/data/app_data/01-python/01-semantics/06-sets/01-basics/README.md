---
name: python-sets-basics
title: 'Set Basics & Mutation'
tags: [python-sets, python-set-mutation]
difficulty: Beginner
---

## Statement

Implement functions that create sets, inspect their contents, demonstrate that a set stores each distinct element only once and add and remove elements with `add`, `remove`, `discard`, `pop` and `clear`. The key distinction is whether an operation requires the element to exist before it can be removed.

## Theory

### Set objects & uniqueness

A **set** is a mutable object that stores a collection of **unique elements**, with no ordered sequence, each element appears at most once and the display order isn't meaningful.

**Creating.** `{1, 2, 3}` and `set(iterable)` both work, but `{}` creates an empty **dictionary**, not a set, `set()` is the only way to write an empty set.

```python
set([1, 2, 2, 3])     # {1, 2, 3}
set("hello")           # {'h', 'e', 'l', 'o'}
```

**Elements must be hashable.** Numbers, strings, and tuples of hashables can be elements; a list cannot (`{[1, 2]}` raises `TypeError`), since it's mutable and can't provide a stable hash.

**Membership** is the operation a set is designed for:

```python
10 in {10, 20, 30}       # True
```

Set membership uses hashing to locate the element, not sequential scanning, this is why a set answers "have I seen this value?" efficiently regardless of size.

**No indexing or slicing.** `s[0]` and `s[1:3]` both raise `TypeError`, a set has no sequence positions.

**Equality.** Two sets are equal when they contain exactly the same elements, regardless of how they were written: `{1, 2, 3} == {3, 1, 2}`.

**Where this matters later.** Sets are useful whenever a program needs uniqueness or repeated membership tests, tracking which IDs have already been processed, removing duplicates, checking whether a token has appeared in a dataset.

### Adding & removing elements

| Method       | Effect                                                           | Returns             |
| ------------ | ---------------------------------------------------------------- | ------------------- |
| `add(x)`     | Inserts `x`; no effect if already present.                       | `None`              |
| `remove(x)`  | Removes `x`; `KeyError` if absent.                               | `None`              |
| `discard(x)` | Removes `x` if present; otherwise does nothing.                  | `None`              |
| `pop()`      | Removes and returns an _arbitrary_ element; `KeyError` if empty. | the removed element |
| `clear()`    | Removes every element; the set object stays, empty.              | `None`              |

The distinction between `remove` and `discard`:

```text
remove(x)   -> remove it; error if absent
discard(x)  -> remove it if present; otherwise do nothing
```

Use `remove` when the program expects the element to exist (absence is a bug); use `discard` when the desired end state is simply "the element should not be present."

`clear()` empties the _existing_ set object, a second variable referring to the same set sees it become empty too, unlike `s = set()`, which only repoints one variable.

**Where this matters later.** Set mutation maintains state such as visited nodes, processed IDs, or active features, and the mutation-vs-reassignment distinction is the same one from the very first module, applied here to sets.

## Explanation

`unique_values` and `unique_count` both go through `set(values)` rather than a manual dedup loop, passing any iterable straight to `set()` is exactly what removes duplicates, since a set can never hold two equal elements to begin with. `contains_all` converts `values` to a set before testing membership for each candidate, which is what the spec's own hint calls for, testing membership against a list instead would still be correct, just not exercise the hash-based lookup this topic is about.

`add_values` builds `set(values)` first rather than mutating the caller's `values` directly, since the spec requires the original untouched, the copy is the new set that gets mutated with `.add()` for each addition. `remove_if_present` uses `discard`, never `remove`, specifically because the spec calls for no exception on an absent value; `remove_required` uses `remove` specifically because the spec wants the `KeyError` to propagate when the value is genuinely expected to exist.
