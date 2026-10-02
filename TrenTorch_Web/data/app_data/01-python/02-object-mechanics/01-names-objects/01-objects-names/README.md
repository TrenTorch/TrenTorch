---
name: python-names-objects-names
title: 'Objects, Names & Assignment'
tags: [python-core, objects, variables]
difficulty: Beginner
---

## Statement

Implement functions that report basic facts about a piece of data (its type and memory address), show that a variable and the object it refers to are separate things and perform chains of assignments while reporting the address each variable ends up holding, making explicit what assignment does and does not copy.

## Theory

### What an object is

Every piece of data Python works with, a number, a string, a list, anything, including the values used in the previous two topics, is stored as an **object**. An object is a chunk of memory holding two things: the actual data, and information about what type that data is.

When you write `100`, Python creates an object somewhere in memory. That object has:

- An **address**, where it physically sits in memory.
- A **type**, `int` in this case, which determines what operations are valid on it.
- A **value**, the data itself, `100`.

```
   1002
 ┌────────────┐
 │  type: int │
 │  value: 100│
 └────────────┘
```

Every value you have used so far, the `25` from the variable topic, the `"Sam"` from the function topic, was already an object with an address, a type, and a value, even though that wasn't mentioned at the time. This is true with no exceptions in Python: there is no separate category of "simple" values that behave differently from more complex ones. An integer is an object exactly as much as a list is.

You can check an object's type with the built-in `type()` function, which returns the object's type as a value you can compare or print.

This idea, that all data is an object living at an address, is the foundation for what a variable and a function argument actually _are_ underneath the syntax already covered. The next topic revisits variables with this in mind.

### Variables as pointers

The Basics sub-section covered writing `x = 100` and treated it as "storing a value in `x`." Now that "object" has been introduced, this can be described precisely: a **variable** is a named storage slot, separate from the object itself, that stores a **value**, and for objects, that stored value is the **address of the object**.

Concretely, when you write:

```python
x = 100
```

Two things exist in memory:

1. The object `100`, the `int` object, sitting at its own address (say `1002`).
2. The variable `x`, sitting at its own, different address (say `3002`), storing the value `1002` (the address of the object it refers to).

```
   3002                          1002
 ┌──────┐                      ┌────────────┐
 │ 1002 │ ────────────────▶   │ type: int   │
 └──────┘                      │ value: 100  │
    x                          └────────────┘
```

`x` itself has an address (`3002`), the location of the variable slot, but that is different from the address `x` _stores_ (`1002`), which is the location of the actual object. When people talk about "the address of `x`," they almost always mean the second one, the address `x` points to, because that's what `id(x)` returns (covered fully in the next topic). `id()` never reports where the variable slot itself lives; it reports the address stored inside it.

This two-layer structure, a variable slot, storing the address of a separately-stored object, is what every remaining topic in this module builds on: assignment, reassignment, mutation, identity, and function arguments are all about how these two layers interact.

### Assignment

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

This copies the **value stored inside `x`**, the address `1002`, into `y`. It does not create a new list. `y` gets its own address as a variable (say `4002`), but the value it stores is identical to what `x` stores: `1002`.

After this, `x` and `y` are two separate variables at two separate addresses, but both store the same value (`1002`), so both refer to the same single list object. This holds no matter how many variables you assign this way, `z = y` would give `z` the value `1002` too, and now three variables all refer to one object.

Assignment is always this same operation, regardless of what's on the right-hand side: a literal, another variable, or the result of a function call. The right-hand side is evaluated down to a single object's address, and that address is what gets stored in the variable on the left.

## Explanation

`describe_object` returns `type(value).__name__` for the type name (the plain string form, e.g. `"int"`, not the `<class 'int'>` repr `type(value)` alone would give) and `id(value)` for the address, exactly as the two named tools the theory introduces. Nothing else needs to happen here, the point of this question is only to establish that these two built-ins exist and what they report, before the next topic builds on them.

`same_object` deliberately does not compare `var1_value == var2_value`, the whole point of this question is that "same object" and "equal value" are different questions, and comparing with `==` would silently pass the "equal value, different object" test case for the wrong reason. Using `id(var1_value) == id(var2_value)` (equivalently, `var1_value is var2_value`) checks the address each stored value points to, which is exactly what "same object" means under the pointer model this topic introduces.

`chain_assign` performs `a = original`, `b = a`, `c = b` and reads `id()` back off each of the four names, rather than off any intermediate captured value, this is what confirms the chain of plain assignments never manufactures a new object at any link, since every one of `id(a)`, `id(b)`, `id(c)` and `id(original)` has to come out identical.
