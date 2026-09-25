---
name: python-numpy-bridge-duck-typing
title: Duck Typing
tags: [python-numpy-bridge]
difficulty: Intermediate
---

## Statement

Implement functions that work with any object supporting the required operations instead of checking types, and a class that becomes usable with `len`, indexing, and iteration by defining the right special methods.

## Theory

Python code rarely asks "what type is this?" — it uses the object and relies on it supporting the operations applied to it. This is **duck typing**.

```python
def total_length(containers):
    return sum(len(c) for c in containers)
```

This works for lists, strings, tuples, dicts, sets, ranges, and any class defining `__len__` — it never names a type. `isinstance(c, list)` would reject everything else, including types written later.

**Protocols** — each operation corresponds to special methods: `len(x)` needs `__len__`; `x[i]` needs `__getitem__`; `for v in x` needs `__iter__` (or `__getitem__` with integer indices as a fallback); `x(...)` needs `__call__`.

**Testing for capability.** `hasattr(obj, "__len__")` is the direct way to ask whether an operation is supported.

**Two styles of handling absence:** look-before-you-leap (`if hasattr(...)`) vs. easier-to-ask-forgiveness (`try`/`except`). The second avoids listing every type that might work and is the usual Python approach when many types could be supplied.

**Where this matters later.** NumPy functions accept lists, tuples, arrays — anything readable by position. A custom dataset class only needs `__len__` and `__getitem__` to be usable by a data loader.

## Explanation

`total_length` and `add_all` never inspect a type at all — `len(c)` and `+` are simply called and trusted to work, exactly the duck-typing style the theory names, which is also what lets both functions work unmodified on a custom class supplying only the needed special method. `Countdown.__getitem__` raises `IndexError` for any `index` outside `0 <= index < start`, which is precisely what lets `list(Countdown(3))` work with **no** `__iter__` defined — Python's fallback iteration protocol calls `__getitem__` with `0, 1, 2, ...` until it sees that exact exception. `first_or_none` catches `(IndexError, KeyError, TypeError)` rather than checking `obj`'s type first, since the "ask forgiveness" style is what lets one function handle lists, dicts, and unsubscriptable objects alike without naming any of them.
