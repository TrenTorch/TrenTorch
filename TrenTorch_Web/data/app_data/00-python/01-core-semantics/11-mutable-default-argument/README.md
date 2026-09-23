---
name: python-mutable-default-argument
title: The Mutable Default Argument Issue
tags: [python-core, functions, mutation]
difficulty: Intermediate
---

## Statement

Implement a function that correctly avoids the mutable default argument trap, and a diagnostic function that detects whether a given function definition is vulnerable to it.

## Theory

Default argument values in a function definition are evaluated **exactly once** — at the moment the `def` statement itself runs, not each time the function is called. For immutable default values (numbers, strings, `None`), this timing makes no observable difference. For mutable default values, it creates a subtle and common bug.

```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket
```

When Python executes this `def` statement, it creates one list object to serve as the default value for `bucket`. That object is created once and stored as part of the function itself, not recreated per call.

```python
add_item("a")     # bucket defaults to the same shared list; becomes ["a"]
add_item("b")     # bucket AGAIN defaults to that SAME list, which
                   # already contains ["a"]; becomes ["a", "b"]
```

Every call that omits `bucket` reuses a reference to that same shared object. `.append()` mutates it in place, so items accumulate across calls that appear — from the calling code — to be entirely independent.

**The fix** is to default to an immutable placeholder, typically `None`, and create a fresh mutable object inside the function body on each call when needed:

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

Now, each call that omits `bucket` triggers the `if` branch, creating a brand-new list object at a new address every time — no state is shared across calls.

This same reasoning applies to any mutable default: `bucket={}` and `bucket=set()` have the identical problem and the identical fix.

## Explanation

`is_vulnerable_to_mutable_default` inspects `func.__defaults__`, a real tuple Python attaches to every function object holding its positional defaults in order — checking each element's type against `(list, dict, set)` is a direct, general way to detect the trap without needing to parse source code or run the function.
