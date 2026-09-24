---
name: python-numpy-bridge-assemble-vector-views
title: "Assemble: A Vector With Shared-Memory Views"
tags: [python-numpy-bridge]
difficulty: Advanced
---

## Statement

Implement a `Vector` class that combines views and copies, special methods, duck-typed arithmetic with broadcasting, and an in-place normalization, behaving in miniature like an array library.

## Theory

This problem introduces no new concepts. It combines this module's topics, and earlier modules leading to it, into one class:

- Keep values in a shared **buffer** and describe which positions a `Vector` exposes with a `range`, so slicing produces a **view** and `copy()` produces an independent object.
- Implement `__len__`, `__getitem__`, `__setitem__`, `__add__`, `__radd__`, and `__repr__`.
- Accept either a number or any sequence as the operand of `+` by testing capability, not type.
- Build results with comprehensions, using `zip` and broadcasting.
- Write an **in-place** operation that changes the buffer through the view, and a returning-new-object operation that does not.

Following the convention used by tensor libraries, a method whose label ends in an underscore, such as `normalize_`, modifies the object in place, while a method without the underscore returns a new object.

## Explanation

`__getitem__`/`__setitem__` mirror the earlier `View` class exactly: slicing indexes into `self.indices` (a range, so slicing it is cheap and produces another range) and wraps the *same* `self.buffer` in a new `Vector`, while an int key writes or reads straight through to the buffer at the resolved position. Slice assignment with a sequence value takes `list(value)` — a real snapshot — *before* writing a single position, which is exactly what makes `v[1:] = v[:-1]` safe even though the source view and the destination positions overlap in the same buffer; writing eagerly instead could smear an already-written value forward into a position still waiting to be read. `copy()` and `map()` both build a **new** list first (`self.to_list()`, or a comprehension over it) and hand that fresh list to `Vector(...)` as its own buffer — never `self.buffer` itself — which is what makes them independent rather than views. `__add__` decides scalar vs. sequence with `hasattr(other, "__len__")`, then uses `list(other)` to read it — since a `Vector` supports the old-style `__getitem__`-based iteration protocol, `list(other)` already works whether `other` is a plain list, a tuple, or another `Vector`, with no `isinstance` needed. `__radd__` just returns `self + other`, which is what makes `sum([v1, v2, v3])` work: `sum` starts from `0`, and `0 + v1` fails on the `int`'s own `__add__`, so Python falls back to `v1.__radd__(0)`.
