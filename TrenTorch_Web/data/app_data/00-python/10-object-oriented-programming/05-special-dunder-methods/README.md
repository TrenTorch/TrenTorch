---
name: python-oop-special-dunder-methods
title: Special (Dunder) Methods
tags: [python-oop]
difficulty: Intermediate
---

## Statement

Implement a `Vec` class whose instances work with `print`, `==`, `len`, indexing, slicing, and iteration by defining the special methods Python calls for those operations.

## Theory

Special ("dunder") methods let a class participate in built-in syntax — Python calls them, they're never called directly.

| Written code | Python calls |
|---|---|
| `repr(x)` | `x.__repr__()` |
| `str(x)`, `print(x)`, `f"{x}"` | `x.__str__()` (falls back to `__repr__` if undefined) |
| `x == y` | `x.__eq__(y)` |
| `len(x)` | `x.__len__()` |
| `x[i]`, `x[a:b]` | `x.__getitem__(i)` or `x.__getitem__(slice)` |

Both `__repr__` and `__str__` must **return** a string, never print one.

**`__eq__`.** Without it, `==` falls back to identity. When `other` is a type the method doesn't understand, it should return the special value `NotImplemented` (not `False`) — Python then tries the other operand and finally gives `False`, letting different types cooperate. Defining `__eq__` also makes instances unhashable by default, since equal objects need equal hashes and Python can't guarantee that without a matching `__hash__`.

**`__len__` and `__getitem__`.** With `__len__`, `len(x)` works and `x` becomes falsy at length `0`. With `__getitem__`, indexing works for both an `int` and a `slice` object — and because a `for` loop can fall back to `__getitem__` with indices `0, 1, 2, ...` until `IndexError`, defining it also makes instances iterable.

**Where this matters later.** PyTorch and NumPy define these same methods on tensors/arrays: `len(t)`, `t[0]`, `t[:, 1]`, `t == u`.

## Explanation

`__getitem__` delegates directly to `self.data[index]` for both `int` and `slice` — a plain Python list already handles both index types and already raises `IndexError` for an out-of-range int, so the only extra step needed is wrapping a slice's *list* result back into a new `Vec` (a slice of a list returns a list, not a `Vec`, so `Vec(*self.data[index])` re-wraps it). `__eq__` returns `NotImplemented` for a non-`Vec` `other` rather than `False` directly — the exact distinction the theory calls out, verified by the hidden tests calling `.__eq__(...)` directly rather than only checking `==`, since checking only `==` wouldn't be able to tell `False` and `NotImplemented` apart (Python converts the latter to `False` automatically when both sides fail).
