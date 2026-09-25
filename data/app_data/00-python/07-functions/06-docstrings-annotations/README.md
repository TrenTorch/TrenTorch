---
name: python-functions-docstrings-annotations
title: Docstrings and Function Annotations
tags: [python-function-metadata]
difficulty: Beginner
---

## Statement

Implement functions with clear docstrings and annotations that describe their parameters and return values.

## Theory

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

**Annotations do not automatically enforce types.** Python never inserts a runtime type check merely because an annotation exists — whether a call actually succeeds still depends on what the function body does with the value it receives.

Annotations can describe collections too (`values: list[int]`), and are especially useful for communicating a function's interface without reading its body.

**Where this matters later.** Clear function contracts are valuable in ML and inference code, where many functions pass arrays, configuration values, and metadata between components.

## Explanation

`percentage`, `repeat_text`, and `make_pair` all carry real parameter and return annotations plus a docstring describing behavior and edge cases — the two are complementary, not redundant: the annotation states the intended types, the docstring states what the function actually computes. `function_metadata` reads `function_metadata.__doc__` and `function_metadata.__annotations__` directly off the function object by name, rather than hard-coding copies of that text — a function can reference its own module-level name inside its body, since that name is only looked up when the function actually runs, by which point `def` has already finished binding it.
