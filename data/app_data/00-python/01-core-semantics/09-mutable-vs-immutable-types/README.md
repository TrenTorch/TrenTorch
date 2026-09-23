---
name: python-mutable-vs-immutable-types
title: Mutable vs Immutable Types
tags: [python-core, mutation]
difficulty: Intermediate
---

## Statement

Implement a function that, for a given value, determines whether its type is mutable or immutable, and a second function that demonstrates the practical consequence of that classification.

## Theory

Every built-in type falls into one of two categories:

**Immutable types** — the object at a given address can never be changed after creation. Any operation that looks like a modification actually creates a new object at a new address.

- `int`, `float`, `bool`, `str`, `tuple`, `frozenset`

**Mutable types** — the object at a given address can be changed directly; its data is edited in place, and its address stays the same.

- `list`, `dict`, `set`, and instances of most custom classes by default

**Immutable example:**

```python
s = "hello"
s = s + " world"
```

`s + " world"` cannot modify the string object at `s`'s address — strings are immutable, so that address's contents are fixed forever. Instead, a brand-new string object `"hello world"` is created at a new address, and `s` is reassigned to store that new address.

**Mutable example:**

```python
lst = [1, 2, 3]
lst.append(4)
```

`.append()` is a method defined on the mutable `list` type. It directly modifies the object at `lst`'s address — no new object is created, and `id(lst)` is identical before and after.

**Why this distinction determines behavior everywhere:** whether a second variable referring to the same object "sees" a change depends entirely on whether the type is mutable — this is *why* the previous topic's reassignment-vs-mutation distinction has any real consequence.

**Tuples deserve a specific note:** a tuple itself is immutable — you cannot add, remove, or replace elements — but if a tuple contains a mutable object (e.g. a list), that inner object can still be mutated. The tuple's immutability only guarantees its own slots can't be reassigned to different objects; it says nothing about the mutability of what those slots point to.

```python
t = ([1, 2], "fixed")
t[0].append(3)     # allowed — mutating the list inside the tuple
t[0] = [9, 9]        # not allowed — reassigning a tuple slot raises an error
```

## Explanation

`is_mutable_type` checks against the fixed set of immutable built-ins (`int`, `float`, `bool`, `str`, `tuple`, `frozenset`) and treats everything else — including a custom class instance the function has never seen before — as mutable by default, matching Python's own actual rule (a class only becomes immutable by explicitly defining `__slots__` with no setters, `__setattr__` blocking, or similar — the default for a plain class is mutable). `tuple_inner_mutation_check` mutates `t[0]` directly via `.append()` rather than by reassigning `t[0] = ...`, which is exactly the operation the theory's tuple note distinguishes as allowed.
