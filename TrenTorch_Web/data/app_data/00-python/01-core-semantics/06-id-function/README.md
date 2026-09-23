---
name: python-id-function
title: The id() Function
tags: [python-core, objects]
difficulty: Beginner
---

## Statement

Implement functions that use `id()` to answer concrete questions about whether operations created a new object or reused an existing one.

## Theory

`id(x)` returns the address currently stored inside variable `x` — the address of the object `x` refers to. Two variables that refer to the same object will always return the same value from `id()`.

```python
x = [1, 2, 3]
print(id(x))     # e.g. 1002

y = x
print(id(y))     # 1002 — same object, same id
```

`id()` is the direct tool for answering the question "are these actually the same object, or just equal in value?" — a question `==` cannot answer, because `==` only compares values, not addresses.

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)     # True — same values
print(id(a) == id(b))   # False — two separate objects
```

`id()` is also the precise way to detect whether an operation mutated an existing object or created a new one. If you record `id(x)` before an operation and again after, an unchanged `id()` means the same object was modified in place; a changed `id()` means a new object was created and `x` was repointed at it.

```python
x = [1, 2, 3]
before = id(x)
x.append(4)
after = id(x)
print(before == after)   # True — same object, mutated in place

x = x + [5]
after2 = id(x)
print(before == after2)  # False — a new list was created
```

This is the exact tool used throughout the rest of this module — and in every later module — to verify whether an operation mutates in place or creates a new object.

## Explanation

`did_mutate_in_place` records `id(lst)` before calling `operation(lst)` and compares it to `id(lst)` after — since `operation` receives `lst` by reference (covered fully in the Function Arguments topic), any in-place mutation the operation performs is visible through this same `lst` name, and comparing the two ids is the direct test for whether that happened. `are_same_object` intentionally uses `is` (equivalent to comparing `id()` directly) rather than `==`, to keep the identity-vs-equality distinction the theory introduces sharp: the hidden tests specifically check this function diverges from `==` on equal-but-separately-built objects.
