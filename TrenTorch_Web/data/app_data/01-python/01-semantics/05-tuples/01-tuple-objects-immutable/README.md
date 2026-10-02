---
name: python-tuples-objects-immutable
title: Tuple Objects and Why They Are Immutable
tags: [python-tuples]
difficulty: Beginner
---

## Statement

Implement functions that create tuples, read from them, and produce "modified" versions, making clear that a tuple's slots can never be reassigned.

## Theory

A **tuple** is an **immutable** object of type `tuple` that holds an ordered sequence of elements, exactly like a list except its slots are fixed after creation.

**Writing tuples.** It is the **comma** that makes a tuple, not the parentheses:

```python
()              # the empty tuple
(5,)            # a one-element tuple: the trailing comma is required
(5)             # NOT a tuple: this is just the int 5 in parentheses
tuple([1, 2])   # converts any iterable to a tuple
```

**Reading.** Tuples support everything a list supports that does not change the contents: `len(t)`, indexing, slicing (which builds a new tuple), `x in t`, `t.count(x)`, `t.index(x)`, `+`, and `*` with an `int`.

**Why immutable.** A tuple has no `append`, `remove`, `sort`, or slot assignment. Trying `t[0] = 99` produces a `TypeError`. A tuple's immutability applies to **its own slots only** — if a slot stores the address of a mutable object such as a list, that list can still be mutated.

**"Modifying" a tuple** means building a new tuple from pieces and reassigning the variable:

```python
t = (1, 2, 3)
t = t[:1] + (99,) + t[2:]      # new tuple (1, 99, 3); t now stores its address
```

**Where this matters later.** Array shapes in NumPy and PyTorch are tuples (e.g. `(3, 4)`), which stops code from accidentally changing a shape in place.

## Explanation

`tuple_replace` is built the same way the theory's own "modifying a tuple" example is: `t[:index] + (value,) + t[index+1:]`, three pieces around the target position, never a list conversion — the exercise's own constraint rules that out anyway. `count_and_first_index` checks `x in t` before calling `.index()`, avoiding a `ValueError` for an absent value rather than catching it after the fact.
