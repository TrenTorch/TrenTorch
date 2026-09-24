---
name: python-functions-as-values-lambda
title: lambda Expressions
tags: [python-lambda]
difficulty: Beginner
---

## Statement

Implement functions using `lambda` expressions where a small function is needed directly as a value.

## Theory

A `lambda` expression creates a function object in a single line: `lambda parameters: expression`. The expression after the colon *is* the return value — there's no explicit `return` statement, and a lambda is restricted to exactly one expression (unlike a `def` function, which can hold multiple statements).

```python
square = lambda x: x * x
square(5)      # 25
```

**Lambdas are ordinary function objects** — they can be assigned to a variable, passed as an argument, stored in a list, or returned from another function, exactly like a `def`-defined function.

```python
operations = [lambda x: x + 1, lambda x: x * 2]
operations[1](5)      # 10
```

**Lambda as an argument** is especially useful when a function is needed only at one call site, with no need to give it a separate name first: `transform_all(values, lambda x: x * 10)`.

**Lambda and closures combine directly** — a lambda can retain access to an enclosing variable exactly like a nested `def` function can:

```python
def make_multiplier(factor):
    return lambda x: x * factor
```

**Where this matters later.** Small inline functions are common for transformations, sort keys, and filters, and this reads naturally into Module 9's iteration tools.

## Explanation

`make_square_function` and `make_offset_function` both return a `lambda` rather than a nested `def` — the whole point of this topic is that a lambda is exactly as valid a return value as a named function, and `make_offset_function`'s lambda retains `offset` as a closure the same way a `def`-based closure would. `apply_lambda` accepts "the function may be a lambda or any other one-argument function" literally — it just calls `function(v)` for each element, with no code path that assumes or requires lambda syntax specifically.
