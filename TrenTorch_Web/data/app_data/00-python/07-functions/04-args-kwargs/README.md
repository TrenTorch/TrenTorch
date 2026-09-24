---
name: python-functions-args-kwargs
title: "*args and **kwargs"
tags: [python-args-kwargs]
difficulty: Intermediate
---

## Statement

Implement functions that accept a variable number of positional and keyword arguments, using `*args` and `**kwargs`.

## Theory

`*args` collects extra positional arguments into a **tuple**:

```python
def total(*values):
    ...

total(1, 2, 3)     # values == (1, 2, 3)
total()            # values == ()
```

`**kwargs` collects extra keyword arguments into a **dictionary**:

```python
def configure(**kwargs):
    ...

configure(batch_size=32, device="cpu")   # kwargs == {"batch_size": 32, "device": "cpu"}
```

Both can combine with ordinary parameters and each other: `def process(required, *args, **kwargs)` sends the first positional argument to `required`, the rest to `args`, and every keyword argument to `kwargs`.

**Unpacking when calling.** The same syntax unpacks a sequence into positional arguments (`total(*values)`) or a dictionary into keyword arguments (`configure(**options)`).

Since `*args` is a real tuple and `**kwargs` a real dictionary, tuple and dictionary operations (unpacking, `.items()`, etc.) work on them directly inside the function.

**Where this matters later.** Variable argument handling is common in reusable utilities and is the foundation for decorators and higher-order functions, where one function needs to accept and forward another function's arguments.

## Explanation

`summarize` builds its result dict as `{"required": required, "values": values, "options": options}` directly — `values` is already the tuple `*values` collected, and `options` is already the dict `**options` collected, so no repacking is needed; the spec's "do not modify any input objects" is automatically satisfied since neither is touched, only read. `call_with_options` forwards with `function(*args, **options)` — the same `*`/`**` unpacking syntax used when *calling*, which is exactly how a generic wrapper forwards an arbitrary call it received, the pattern the theory calls out as the foundation for decorators.
