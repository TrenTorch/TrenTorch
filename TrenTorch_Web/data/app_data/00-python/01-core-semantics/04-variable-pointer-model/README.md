---
name: python-variable-pointer-model
title: What a Variable Really Is (Pointer Model)
tags: [python-core, variables, objects]
difficulty: Beginner
---

## Statement

Implement a function that demonstrates the distinction between a variable and the object it refers to — two separate things, each with its own address — revisiting the basic variable syntax from the first topic with the object model now in place.

## Theory

The first topic in this module covered writing `x = 100` and treated it as "storing a value in `x`." Now that "object" has been introduced, this can be described precisely: a **variable** is a named storage slot, separate from the object itself, that stores a **value** — and for objects, that stored value is the **address of the object**.

Concretely, when you write:

```python
x = 100
```

Two things exist in memory:

1. The object `100` — the `int` object, sitting at its own address (say `1002`).
2. The variable `x` — sitting at its own, different address (say `3002`), storing the value `1002` (the address of the object it refers to).

```
   3002                          1002
 ┌──────┐                      ┌────────────┐
 │ 1002 │ ────────────────▶   │ type: int   │
 └──────┘                      │ value: 100  │
    x                          └────────────┘
```

`x` itself has an address (`3002`) — the location of the variable slot — but that is different from the address `x` *stores* (`1002`), which is the location of the actual object. When people talk about "the address of `x`," they almost always mean the second one — the address `x` points to — because that's what `id(x)` returns (covered fully in the next topic). `id()` never reports where the variable slot itself lives; it reports the address stored inside it.

This two-layer structure — a variable slot, storing the address of a separately-stored object — is what every remaining topic in this module builds on: assignment, reassignment, mutation, identity, and function arguments are all about how these two layers interact.

## Explanation

`same_object` deliberately does not compare `var1_value == var2_value` — the whole point of this question is that "same object" and "equal value" are different questions, and comparing with `==` would silently pass the "equal value, different object" test case for the wrong reason. Using `id(var1_value) == id(var2_value)` (equivalently, `var1_value is var2_value`) checks the address each stored value points to, which is exactly what "same object" means under the pointer model this topic introduces.
