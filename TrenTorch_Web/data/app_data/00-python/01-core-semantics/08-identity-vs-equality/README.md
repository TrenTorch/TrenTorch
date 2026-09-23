---
name: python-identity-vs-equality
title: Identity (is) vs Equality (==)
tags: [python-core, objects]
difficulty: Beginner
---

## Statement

Implement a function that classifies pairs of values by whether they are equal, identical, both, or neither — making the distinction between these two comparisons concrete.

## Theory

Python has two different comparison operators that are easy to confuse:

- `==` checks **equality** — whether two objects have the same value, according to that type's definition of equal.
- `is` checks **identity** — whether two variables store the exact same address, i.e. whether they refer to the literal same object.

```python
a = [1, 2, 3]
b = [1, 2, 3]

a == b     # True — same values
a is b     # False — two different objects, different addresses
```

```python
c = a
c == a     # True
c is a     # True — c stores the same address as a
```

Two objects that are identical (`is` is `True`) are always also equal (`==` is `True`), because they're literally the same object being compared to itself. The reverse is not guaranteed — two equal objects are not necessarily identical.

**A specific behavior to be aware of:** small integers and short strings are sometimes automatically reused by Python for efficiency, which can make `is` return `True` even for separately written literals in some cases (e.g. small integers like `5`). This is an internal optimization detail, not a guarantee — `is` should be used to check identity intentionally (e.g. checking something `is None`), not relied upon as a shortcut for equality on arbitrary values. `==` is the correct tool for comparing values; `is` is the correct tool for confirming two variables refer to one object.

## Explanation

`classify_pair` checks `is` before `==` rather than the other way around, because identity implies equality but not the reverse — checking `is` first means the `"identical"` branch never needs to also verify `==` separately (it's guaranteed), and the remaining two branches only need to distinguish equal-but-not-identical from genuinely unequal.
