---
name: python-functions-default-arguments
title: Default Arguments and When Values Are Bound
tags: [python-function-defaults]
difficulty: Intermediate
---

## Statement

Implement functions with optional parameters using default arguments, relying on the fact that default values are evaluated when the function is defined, not each call.

## Theory

A parameter can have a **default value**, used only when the caller omits it:

```python
def add(a, b=10):
    return a + b

add(5)       # a=5, b=10 (default used)
add(5, 20)   # a=5, b=20 (default not used)
```

**Default values are bound at definition time.** Changing a variable used as a default afterward does not change the already-created default — it's part of the function object from the moment `def` runs.

**Mutable defaults are reused across calls that omit the argument** — the exact issue from the very first module. The safe pattern is defaulting to `None` and creating a fresh object inside the function body:

```python
def collect(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items
```

**Immutable defaults** (numbers, strings, tuples) don't have this problem, since there's nothing to mutate.

**Ordering.** A required parameter cannot follow a parameter with a default in the plain parameter list — `def f(a=1, b)` is invalid; `def f(a, b=1, c=2)` is fine.

**Where this matters later.** The binding rule matters in long-running programs and ML code where a mutable default could silently preserve state between calls.

## Explanation

`append_value` uses the `items=None` safe pattern rather than `items=[]`, so a call that omits `items` gets a genuinely fresh list every time, while a call that *does* supply a list mutates that exact object (matching "return the same list object" in the spec) — one function correctly handling both the "give me a new list" and "mutate my list" cases. `power`, `make_label`, and `describe_config` all use plain immutable defaults (`2`, `"item"`, `True`/`3`), which need no such care since there's no shared mutable state to leak between calls.
