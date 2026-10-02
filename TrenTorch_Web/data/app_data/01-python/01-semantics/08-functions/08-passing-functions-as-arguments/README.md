---
name: python-functions-as-values-passing-as-arguments
title: Passing a Function as an Argument
tags: [python-functions-as-values]
difficulty: Intermediate
---

## Statement

Implement functions that receive another function as an argument and call it at the appropriate point.

## Theory

Since functions are objects, a function can be passed to another function like any other value:

```python
def apply_once(function, value):
    return function(value)

apply_once(square, 5)
```

`square` without parentheses is the function object; `square(5)` would call it immediately and pass its _result_ instead. The distinction is exactly `function` (the object) vs `function(...)` (a call).

A function that receives another function as an argument is a **higher-order function**. It doesn't need to know what the passed-in function does internally — only that it can be called with the right number of values.

**Applying repeatedly.** A higher-order function can call the same operation several times in sequence, each time feeding the previous result back in:

```text
3 -> add_two -> 5 -> add_two -> 7 -> add_two -> 9
```

**Where this matters later.** Passing functions as values is directly useful for preprocessing, scoring, and configurable data pipelines, where the same pipeline structure applies different operations to different inputs.

## Explanation

`apply_n_times` loops exactly `count` times, feeding each call's result into the next, and returns the original `value` unchanged for `count <= 0` — no calls happen at all in that case, matching the spec rather than "applying zero times" being mistaken for one no-op call. `transform_all` builds a fresh list via a comprehension (`[function(v) for v in values]`) rather than mutating `values` in place, since the input must stay untouched and the result must be a genuinely new list.
