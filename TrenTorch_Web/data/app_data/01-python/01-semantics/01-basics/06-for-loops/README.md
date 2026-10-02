---
name: python-for-loops
title: for Loops
tags: [python-core, control-flow, loops]
difficulty: Intermediate
---

## Statement

Implement functions using `for` loops over different collection types, and a function that manually replicates what a `for` loop does internally using the lower-level mechanism it's built on.

## Theory

A `for` loop in Python iterates directly over the elements of an iterable object — a list, string, tuple, dict, set, or range — assigning each element in turn to the loop variable.

```python
for item in [10, 20, 30]:
    print(item)
```

Internally, a `for` loop is built on the same iterator mechanism you'd use manually with `iter()` and `next()` (covered fully in the Iteration Internals module) — but at this stage, the important fact is simply this: `for` requests elements from the collection one at a time, in order, and stops automatically once the collection is exhausted. You never need to track an index or a stopping condition yourself, unlike a `while` loop.

`for` loops also support `break`, `continue`, and the loop `else` clause, with identical meaning to their use in `while` loops covered in the previous topic.

**Iterating with both index and value** uses `enumerate()`, which pairs each element with its position:

```python
for index, value in enumerate(["a", "b", "c"]):
    print(index, value)
# 0 a
# 1 b
# 2 c
```

`enumerate()` returns pairs (specifically, tuples of `(index, value)`), and the `for` loop unpacks each pair directly into the two loop variables `index` and `value` — this is the same unpacking mechanism used for tuples generally (covered fully in the Tuples module).

**Iterating over a dictionary** by default iterates over its keys only:

```python
d = {"a": 1, "b": 2}
for key in d:
    print(key)     # "a", then "b"
```

To get both keys and values together, `.items()` is used (covered fully in the Dictionaries module).

## Explanation

`sum_with_index` uses `enumerate()` specifically because the required output keys ARE the indices — this is the exact case `enumerate()` exists for, needing the position alongside the value rather than just the value. `manual_iteration_trace` calls `iter()` once to get an iterator object, then calls `next()` repeatedly inside its own `while True:` loop, catching `StopIteration` to detect exhaustion — this is deliberately the lower-level mechanism a `for` loop hides, made explicit here to demystify it ahead of the Iteration Internals module.
