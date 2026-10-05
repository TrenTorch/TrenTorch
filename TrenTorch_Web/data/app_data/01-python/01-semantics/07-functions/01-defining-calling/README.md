---
name: python-functions-defining-calling
title: 'Defining & Calling'
tags: [python-functions, python-function-metadata]
difficulty: Beginner
---

## Statement

Implement functions that accept arguments, perform calculations and return values (including multiple values) and that carry clear docstrings and annotations describing their parameters and return values.

## Theory

### Defining & calling functions

A **function** is defined with `def`, which creates the function object and stores it in a variable:

```python
def add(a, b):
    return a + b
```

**`return`** ends the current function call and hands a value back to the caller. If execution reaches the end of a function without a `return`, the function returns `None`, printing and returning are different operations.

```python
def show_value(x):
    print(x)

result = show_value(10)   # result is None, even though 10 was printed
```

**`return` immediately ends the function**, statements after it in that execution path never run.

**Multiple return values.** `return 10, 20` actually returns one tuple, `(10, 20)`, connecting directly to tuple packing:

```python
def coordinates():
    return 10, 20

x, y = coordinates()      # x == 10, y == 20
```

**Parameters are variables** belonging to a single function call, a later call creates fresh parameter storage, not a reuse of the earlier call's.

**Where this matters later.** Functions are the main unit for structuring reusable logic, especially in data-processing pipelines and ML utilities.

### Docstrings & annotations

A **docstring** is a string placed immediately inside a function definition, stored as the function's `__doc__` attribute:

```python
def square(x):
    """Return the square of x."""
    return x * x

square.__doc__   # "Return the square of x."
```

**Function annotations** describe intended parameter and return types:

```python
def square(x: int) -> int:
    return x * x

square.__annotations__   # {'x': int, 'return': int}
```

**Annotations do not automatically enforce types.** Python never inserts a runtime type check merely because an annotation exists, whether a call actually succeeds still depends on what the function body does with the value it receives.

Annotations can describe collections too (`values: list[int]`), and are especially useful for communicating a function's interface without reading its body.

**Where this matters later.** Clear function contracts are valuable in ML and inference code, where many functions pass arrays, configuration values and metadata between components.

## Explanation

`min_max` tracks running minimum and maximum with a plain loop and comparisons, per the exercise's own "do not use `min()`/`max()`" constraint, then returns them packed as `(minimum, maximum)`, one tuple, matching the module's own multiple-return-value convention. `absolute_value` branches on `x < 0` rather than calling `abs()`, per that function's own constraint, returning `-x` for negatives and `x` otherwise.

`percentage`, `repeat_text`, and `make_pair` all carry real parameter and return annotations plus a docstring describing behavior and edge cases, the two are complementary, not redundant: the annotation states the intended types, the docstring states what the function actually computes. `function_metadata` reads `function_metadata.__doc__` and `function_metadata.__annotations__` directly off the function object by name, rather than hard-coding copies of that text, a function can reference its own module-level name inside its body, since that name is only looked up when the function actually runs, by which point `def` has already finished binding it.
