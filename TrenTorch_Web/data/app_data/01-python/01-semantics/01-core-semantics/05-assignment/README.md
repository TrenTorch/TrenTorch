---
name: python-assignment
title: Assignment
tags: [python-core, variables]
difficulty: Beginner
---

## Statement

Implement a function that performs a chain of assignments and reports the final address stored by each variable involved, to make explicit what assignment does and does not copy.

## Theory

The statement `x = value` does exactly one thing: it makes the variable `x` store the address of `value`'s object. It never copies the object's data.

```python
x = [1, 2, 3]
```

```
   3002                          1002    1003    1004
 ┌──────┐                      ┌──────┬──────┬──────┐
 │ 1002 │ ────────────────▶   │  1   │  2   │  3   │
 └──────┘                      └──────┴──────┴──────┘
    x                                  list object
```

Now consider a second assignment using `x`:

```python
y = x
```

This copies the **value stored inside `x`** — the address `1002` — into `y`. It does not create a new list. `y` gets its own address as a variable (say `4002`), but the value it stores is identical to what `x` stores: `1002`.

After this, `x` and `y` are two separate variables at two separate addresses, but both store the same value (`1002`), so both refer to the same single list object. This holds no matter how many variables you assign this way — `z = y` would give `z` the value `1002` too, and now three variables all refer to one object.

Assignment is always this same operation, regardless of what's on the right-hand side: a literal, another variable, or the result of a function call. The right-hand side is evaluated down to a single object's address, and that address is what gets stored in the variable on the left.

## Explanation

`chain_assign` performs `a = original`, `b = a`, `c = b` and reads `id()` back off each of the four names, rather than off any intermediate captured value — this is what confirms the chain of plain assignments never manufactures a new object at any link, since every one of `id(a)`, `id(b)`, `id(c)`, and `id(original)` has to come out identical.
