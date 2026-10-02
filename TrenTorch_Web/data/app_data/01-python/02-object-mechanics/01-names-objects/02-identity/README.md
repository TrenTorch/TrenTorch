---
name: python-names-identity
title: 'Identity & Equality'
tags: [python-core, objects]
difficulty: Beginner
---

## Statement

Implement functions that use `id()` to tell whether operations created a new object or reused an existing one, and that classify pairs of values by whether they are equal, identical, both, or neither.

## Theory

### The id() function

`id(x)` returns the address currently stored inside variable `x`, the address of the object `x` refers to. Two variables that refer to the same object will always return the same value from `id()`.

```python
x = [1, 2, 3]
print(id(x))     # e.g. 1002

y = x
print(id(y))     # 1002, same object, same id
```

`id()` is the direct tool for answering the question "are these actually the same object, or just equal in value?", a question `==` cannot answer, because `==` only compares values, not addresses.

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)     # True, same values
print(id(a) == id(b))   # False, two separate objects
```

`id()` is also the precise way to detect whether an operation mutated an existing object or created a new one. If you record `id(x)` before an operation and again after, an unchanged `id()` means the same object was modified in place; a changed `id()` means a new object was created and `x` was repointed at it.

```python
x = [1, 2, 3]
before = id(x)
x.append(4)
after = id(x)
print(before == after)   # True, same object, mutated in place

x = x + [5]
after2 = id(x)
print(before == after2)  # False, a new list was created
```

This is the exact tool used throughout the rest of this module, and in every later module, to verify whether an operation mutates in place or creates a new object.

### Identity (is) vs equality (==)

Python has two different comparison operators that are easy to confuse:

- `==` checks **equality**, whether two objects have the same value, according to that type's definition of equal.
- `is` checks **identity**, whether two variables store the exact same address, i.e. whether they refer to the literal same object.

```python
a = [1, 2, 3]
b = [1, 2, 3]

a == b     # True, same values
a is b     # False, two different objects, different addresses
```

```python
c = a
c == a     # True
c is a     # True, c stores the same address as a
```

Two objects that are identical (`is` is `True`) are always also equal (`==` is `True`), because they're literally the same object being compared to itself. The reverse is not guaranteed, two equal objects are not necessarily identical.

**A specific behavior to be aware of:** small integers and short strings are sometimes automatically reused by Python for efficiency, which can make `is` return `True` even for separately written literals in some cases (e.g. small integers like `5`). This is an internal optimization detail, not a guarantee, `is` should be used to check identity intentionally (e.g. checking something `is None`), not relied upon as a shortcut for equality on arbitrary values. `==` is the correct tool for comparing values; `is` is the correct tool for confirming two variables refer to one object.

## Explanation

`did_mutate_in_place` records `id(lst)` before calling `operation(lst)` and compares it to `id(lst)` after, since `operation` receives `lst` by reference (covered fully in the Function Arguments topic), any in-place mutation the operation performs is visible through this same `lst` name, and comparing the two ids is the direct test for whether that happened. `are_same_object` intentionally uses `is` (equivalent to comparing `id()` directly) rather than `==`, to keep the identity-vs-equality distinction the theory introduces sharp: the hidden tests specifically check this function diverges from `==` on equal-but-separately-built objects.

`classify_pair` checks `is` before `==` rather than the other way around, because identity implies equality but not the reverse, checking `is` first means the `"identical"` branch never needs to also verify `==` separately (it's guaranteed), and the remaining two branches only need to distinguish equal-but-not-identical from genuinely unequal.
