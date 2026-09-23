---
name: python-reassignment-vs-mutation
title: Reassignment vs Mutation
tags: [python-core, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that clearly separate "pointing a variable at a new object" from "changing the object a variable already points to," and demonstrate why the distinction changes what other variables observe.

## Theory

There are two fundamentally different operations that can look similar in code, and confusing them is the single most common source of unexpected behavior for people new to Python.

**Reassignment** changes what address a variable stores. It does not touch any existing object.

```python
x = [1, 2, 3]
x = [4, 5, 6]
```

The object `[1, 2, 3]` is untouched — it still exists exactly as it was (until nothing refers to it and it's cleaned up). `x` was simply repointed to a different, newly created object.

**Mutation** changes the data inside an object that already exists, at its existing address, without creating a new object.

```python
x = [1, 2, 3]
x.append(4)
```

`x` still stores the same address — nothing about `x` changed. The object *at* that address changed.

**Why this distinction matters:** if a second variable `y` also stores the same address (because `y = x` happened earlier), mutation is visible through `y` — reading `y` shows the updated list, because `y` points at the same address where the change happened. Reassignment of `x` is never visible through `y`, because reassignment only updates `x`'s stored value; `y` still stores the old address, unaffected.

```python
x = [1, 2, 3]
y = x
x.append(4)        # mutation — y sees this too: y is now [1, 2, 3, 4]
x = [9, 9, 9]       # reassignment — y is unaffected: y is still [1, 2, 3, 4]
```

## Explanation

`observe_through_alias` runs the exact sequence the theory's last example walks through — alias, mutate, then reassign — and reports `alias`'s contents at each checkpoint rather than only at the end, so the hidden tests can confirm the mutation propagated through the alias while the later reassignment did not, instead of only checking a final state that could pass for the wrong reason.
