---
name: python-what-an-object-is
title: What an Object Is
tags: [python-core, objects]
difficulty: Beginner
---

## Statement

Implement a function that reports basic facts about a piece of data — its type and its memory address — to build a concrete picture of what an "object" is, ahead of revisiting variables and functions with this deeper model.

## Theory

Every piece of data Python works with — a number, a string, a list, anything, including the values used in the previous two topics — is stored as an **object**. An object is a chunk of memory holding two things: the actual data, and information about what type that data is.

When you write `100`, Python creates an object somewhere in memory. That object has:

- An **address** — where it physically sits in memory.
- A **type** — `int` in this case, which determines what operations are valid on it.
- A **value** — the data itself, `100`.

```
   1002
 ┌────────────┐
 │  type: int │
 │  value: 100│
 └────────────┘
```

Every value you have used so far — the `25` from the variable topic, the `"Sam"` from the function topic — was already an object with an address, a type, and a value, even though that wasn't mentioned at the time. This is true with no exceptions in Python: there is no separate category of "simple" values that behave differently from more complex ones. An integer is an object exactly as much as a list is.

You can check an object's type with the built-in `type()` function, which returns the object's type as a value you can compare or print.

This idea — that all data is an object living at an address — is the foundation for what a variable and a function argument actually *are* underneath the syntax already covered. The next topic revisits variables with this in mind.

## Explanation

`describe_object` returns `type(value).__name__` for the type name (the plain string form, e.g. `"int"`, not the `<class 'int'>` repr `type(value)` alone would give) and `id(value)` for the address, exactly as the two named tools the theory introduces. Nothing else needs to happen here — the point of this question is only to establish that these two built-ins exist and what they report, before the next topic builds on them.
