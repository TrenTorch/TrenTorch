---
name: python-oop-assemble-matrix-hierarchy
title: 'Assemble: A Small Matrix Class Hierarchy'
tags: [python-oop, inheritance]
difficulty: Advanced
---

## Statement

Implement a `Matrix` class and an `IdentityMatrix` subclass that combine instance attributes, class attributes, methods, special methods, and `super()`, while protecting internal data from aliasing.

## Theory

This problem introduces no new concepts. It combines this module's topics into one realistic class:

- Build instances in `__init__` and store per-instance data as attributes.
- Write methods that read `self` and return new instances.
- Keep a class-level counter that every construction increments, including constructions through a subclass.
- Implement `__repr__`, `__eq__`, `__len__`, and `__getitem__`.
- Reuse the parent constructor from the subclass with `super()` and rely on inherited methods.
- Prevent the caller's lists from being shared with the instance.

Two matrices are equal when their rows are equal. The transpose of an $r \times c$ matrix is the $c \times r$ matrix whose entry at row $j$, column $i$ is the original entry at row $i$, column $j$.

## Explanation

`Matrix.__init__` stores `copy.deepcopy(rows)`, not `rows` or `list(rows)` — a shallow copy would still share the _inner_ row lists with the caller, so only a deep copy actually satisfies "later changes to the caller's lists never affect this matrix." The counter increments through the class name (`Matrix.instances_created += 1`) inside `Matrix.__init__` itself, which is what makes every construction path count exactly once: a direct `Matrix(...)` call runs this code directly, and `IdentityMatrix.__init__` reaches the same line via `super().__init__(rows)` rather than duplicating the counting logic, so subclass instances are counted without any extra code. `transpose` and `scale` both build their result rows as a fresh nested list comprehension and pass that to `Matrix(...)` — going through the real constructor (not bypassing it to poke at `.rows` directly) is what keeps the counter accurate for matrices produced by these methods too.
