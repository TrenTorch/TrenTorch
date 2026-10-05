---
name: python-tuples-immutability
title: 'Immutability & Tuples vs Lists'
tags: [python-tuples, python-lists]
difficulty: Intermediate
---

## Statement

Implement functions that create tuples, read from them and produce "modified" versions without reassigning slots, convert between lists and tuples and detect when a tuple still contains mutable objects.

## Theory

### Tuple objects & immutability

A **tuple** is an **immutable** object of type `tuple` that holds an ordered sequence of elements, exactly like a list except its slots are fixed after creation.

**Writing tuples.** It is the **comma** that makes a tuple, not the parentheses:

```python
()              # the empty tuple
(5,)            # a one-element tuple: the trailing comma is required
(5)             # NOT a tuple: this is just the int 5 in parentheses
tuple([1, 2])   # converts any iterable to a tuple
```

**Reading.** Tuples support everything a list supports that does not change the contents: `len(t)`, indexing, slicing (which builds a new tuple), `x in t`, `t.count(x)`, `t.index(x)`, `+` and `*` with an `int`.

**Why immutable.** A tuple has no `append`, `remove`, `sort`, or slot assignment. Trying `t[0] = 99` produces a `TypeError`. A tuple's immutability applies to **its own slots only**, if a slot stores the address of a mutable object such as a list, that list can still be mutated.

**"Modifying" a tuple** means building a new tuple from pieces and reassigning the variable:

```python
t = (1, 2, 3)
t = t[:1] + (99,) + t[2:]      # new tuple (1, 99, 3); t now stores its address
```

**Where this matters later.** Array shapes in NumPy and PyTorch are tuples (e.g. `(3, 4)`), which stops code from accidentally changing a shape in place.

### Tuples vs lists

Lists and tuples both store ordered sequences of addresses. They differ in exactly one property: a list's slots can be changed after creation, a tuple's cannot. That decides which is appropriate, a tuple for a fixed group of related values, a value several places share, a dictionary key, or several return values; a list for anything that grows, shrinks, or is reordered.

**Safety from aliasing.** A list passed to a function can be mutated by that function, and the caller sees it. A tuple cannot be mutated, so the caller's data is guaranteed unchanged unless the function returns a new tuple.

**Immutability is shallow.** A tuple guarantees its **own slots** don't change, it does not guarantee the objects inside it are immutable:

```python
t = ([1, 2], [3])
t[0].append(99)        # t is now ([1, 2, 99], [3]); t's slots never changed
```

**Testing a type.** `isinstance(obj, tuple)` / `isinstance(obj, list)` are the direct way to write code that treats the two differently.

**Converting.** `tuple(seq)` and `list(seq)` build a new object of the other type. Conversions are **shallow**: the elements are shared, not copied, to convert a nested list to a nested tuple, each inner list must be converted too.

**Where this matters later.** Choosing an immutable value for something that should never change removes a category of bugs, and is what makes those values usable as dictionary keys.

## Explanation

`tuple_replace` is built the same way the theory's own "modifying a tuple" example is: `t[:index] + (value,) + t[index+1:]`, three pieces around the target position, never a list conversion, the exercise's own constraint rules that out anyway. `count_and_first_index` checks `x in t` before calling `.index()`, avoiding a `ValueError` for an absent value rather than catching it after the fact.

`updated` converts `seq` to a plain `list` unconditionally, mutates that working copy (skipping the assignment via a caught `IndexError` when `index` is out of range), then converts back to `tuple` only if the original was a tuple, one code path handles both input types instead of duplicating the "replace, but skip if out of range" logic per type. `has_mutable_element` checks only the tuple's _direct_ elements against `(list, dict, set)`, not elements nested inside an inner tuple, matching the spec's own "check only the direct elements" scope.
