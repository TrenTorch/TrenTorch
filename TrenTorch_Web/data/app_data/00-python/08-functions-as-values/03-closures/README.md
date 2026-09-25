---
name: python-functions-as-values-closures
title: Closures and Retained Enclosing Scope
tags: [python-closures]
difficulty: Intermediate
---

## Statement

Implement functions that create and return other functions while retaining access to values from the enclosing function.

## Theory

A **closure** is a function that retains access to variables from an enclosing scope, even after that enclosing function has finished running:

```python
def make_adder(amount):
    def add(value):
        return value + amount
    return add

add_five = make_adder(5)
add_five(3)   # 8 -- `add` still has access to `amount`
```

Different calls to the outer function create independent retained values: `make_multiplier(2)` and `make_multiplier(3)` produce two separate closures, each with its own `factor`.

**Changing an enclosing variable** requires `nonlocal`:

```python
def make_counter():
    count = 0
    def next_count():
        nonlocal count
        count += 1
        return count
    return next_count
```

Without `nonlocal`, `count += 1` inside `next_count` would create a _local_ `count`, shadowing the enclosing one, rather than updating it. Calling `make_counter()` twice creates two completely independent retained `count`s.

**Where this matters later.** Closures carry configuration and state without exposing it as a global variable — used in configurable preprocessing, metric functions, and caching helpers.

## Explanation

`make_multiplier` and `make_prefixer` both define a small nested function that simply _reads_ the enclosing parameter (`factor`, `prefix`) — reading needs no `nonlocal` at all, only assignment does. `make_counter` is the one function here that reassigns its enclosing variable (`count += 1` inside the nested function), which is exactly why it needs `nonlocal count` — omitting it would silently create a function-local `count` that resets to a fresh value every call instead of accumulating.
