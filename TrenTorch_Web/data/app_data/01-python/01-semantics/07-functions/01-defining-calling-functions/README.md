---
name: python-functions-defining-calling
title: Defining and Calling Functions, and Return Values
tags: [python-functions]
difficulty: Beginner
---

## Statement

Implement functions that accept arguments, perform calculations, and return values, including how multiple values are returned.

## Theory

A **function** is defined with `def`, which creates the function object and stores it in a variable:

```python
def add(a, b):
    return a + b
```

**`return`** ends the current function call and hands a value back to the caller. If execution reaches the end of a function without a `return`, the function returns `None` — printing and returning are different operations.

```python
def show_value(x):
    print(x)

result = show_value(10)   # result is None, even though 10 was printed
```

**`return` immediately ends the function** — statements after it in that execution path never run.

**Multiple return values.** `return 10, 20` actually returns one tuple, `(10, 20)`, connecting directly to tuple packing:

```python
def coordinates():
    return 10, 20

x, y = coordinates()      # x == 10, y == 20
```

**Parameters are variables** belonging to a single function call — a later call creates fresh parameter storage, not a reuse of the earlier call's.

**Where this matters later.** Functions are the main unit for structuring reusable logic, especially in data-processing pipelines and ML utilities.

## Explanation

`min_max` tracks running minimum and maximum with a plain loop and comparisons, per the exercise's own "do not use `min()`/`max()`" constraint, then returns them packed as `(minimum, maximum)` — one tuple, matching the module's own multiple-return-value convention. `absolute_value` branches on `x < 0` rather than calling `abs()`, per that function's own constraint, returning `-x` for negatives and `x` otherwise.
