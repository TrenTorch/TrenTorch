---
name: python-names-mutation
title: Reassignment vs Mutation
tags: [python-core, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that separate "pointing a variable at a new object" from "changing the object a variable already points to", show why the distinction changes what other variables observe and decide whether a value's type is mutable or immutable along with the practical consequence of that classification.

## Theory

### Reassignment vs mutation

There are two fundamentally different operations that can look similar in code, and confusing them is the single most common source of unexpected behavior for people new to Python.

**Reassignment** changes what address a variable stores. It does not touch any existing object.

```python
x = [1, 2, 3]
x = [4, 5, 6]
```

The object `[1, 2, 3]` is untouched, it still exists exactly as it was (until nothing refers to it and it's cleaned up). `x` was simply repointed to a different, newly created object.

**Mutation** changes the data inside an object that already exists, at its existing address, without creating a new object.

```python
x = [1, 2, 3]
x.append(4)
```

`x` still stores the same address, nothing about `x` changed. The object _at_ that address changed.

**Why this distinction matters:** if a second variable `y` also stores the same address (because `y = x` happened earlier), mutation is visible through `y`, reading `y` shows the updated list, because `y` points at the same address where the change happened. Reassignment of `x` is never visible through `y`, because reassignment only updates `x`'s stored value; `y` still stores the old address, unaffected.

```python
x = [1, 2, 3]
y = x
x.append(4)        # mutation, y sees this too: y is now [1, 2, 3, 4]
x = [9, 9, 9]       # reassignment, y is unaffected: y is still [1, 2, 3, 4]
```

### Mutable vs immutable types

Every built-in type falls into one of two categories:

**Immutable types**, the object at a given address can never be changed after creation. Any operation that looks like a modification actually creates a new object at a new address.

- `int`, `float`, `bool`, `str`, `tuple`, `frozenset`

**Mutable types**, the object at a given address can be changed directly; its data is edited in place, and its address stays the same.

- `list`, `dict`, `set` and instances of most custom classes by default

**Immutable example:**

```python
s = "hello"
s = s + " world"
```

`s + " world"` cannot modify the string object at `s`'s address, strings are immutable, so that address's contents are fixed forever. Instead, a brand-new string object `"hello world"` is created at a new address, and `s` is reassigned to store that new address.

**Mutable example:**

```python
lst = [1, 2, 3]
lst.append(4)
```

`.append()` is a method defined on the mutable `list` type. It directly modifies the object at `lst`'s address, no new object is created and `id(lst)` is identical before and after.

**Why this distinction determines behavior everywhere:** whether a second variable referring to the same object "sees" a change depends entirely on whether the type is mutable, this is _why_ the previous topic's reassignment-vs-mutation distinction has any real consequence.

**Tuples deserve a specific note:** a tuple itself is immutable, you cannot add, remove, or replace elements, but if a tuple contains a mutable object (e.g. a list), that inner object can still be mutated. The tuple's immutability only guarantees its own slots can't be reassigned to different objects; it says nothing about the mutability of what those slots point to.

```python
t = ([1, 2], "fixed")
t[0].append(3)     # allowed, mutating the list inside the tuple
t[0] = [9, 9]        # not allowed, reassigning a tuple slot raises an error
```

## Explanation

`observe_through_alias` runs the exact sequence the theory's last example walks through, alias, mutate, then reassign, and reports `alias`'s contents at each checkpoint rather than only at the end, so the hidden tests can confirm the mutation propagated through the alias while the later reassignment did not, instead of only checking a final state that could pass for the wrong reason.

`is_mutable_type` checks against the fixed set of immutable built-ins (`int`, `float`, `bool`, `str`, `tuple`, `frozenset`) and treats everything else, including a custom class instance the function has never seen before, as mutable by default, matching Python's own actual rule (a class only becomes immutable by explicitly defining `__slots__` with no setters, `__setattr__` blocking, or similar, the default for a plain class is mutable). `tuple_inner_mutation_check` mutates `t[0]` directly via `.append()` rather than by reassigning `t[0] = ...`, which is exactly the operation the theory's tuple note distinguishes as allowed.
