---
name: python-functions-as-objects
title: Functions as Objects
tags: [python-functions-as-values, python-lambda]
difficulty: Intermediate
---

## Statement

Implement functions that treat functions like ordinary values: assign them to variables, store them in collections, pass them to other functions that call them and write small `lambda` expressions where a function is needed directly as a value.

## Theory

### Functions are objects

A function's name is a variable, like any other, it stores the address of an object. Writing the bare name refers to the **function object**; writing the name with `()` **calls** it.

```python
def square(x):
    return x * x

f = square       # stores the function object; does NOT call it
f = square(5)    # calls square; f now refers to 25, an int
```

`f = square` creates another variable pointing at the _same_ function object, it doesn't create a second function.

**Functions in collections.** Since functions are objects, they can be stored in lists and dictionaries: `operations = [add_one, double]`, and `operations[0](10)` retrieves the function then calls it.

**Function identity.** Two variables can refer to the exact same function object, `a is b` is `True` when both point at one function, the same identity concept from Module 1.

**Where this matters later.** Functions as objects are the foundation for passing transformations, callbacks, and sorting keys around as data.

### Passing functions as arguments

Since functions are objects, a function can be passed to another function like any other value:

```python
def apply_once(function, value):
    return function(value)

apply_once(square, 5)
```

`square` without parentheses is the function object; `square(5)` would call it immediately and pass its _result_ instead. The distinction is exactly `function` (the object) vs `function(...)` (a call).

A function that receives another function as an argument is a **higher-order function**. It doesn't need to know what the passed-in function does internally, only that it can be called with the right number of values.

**Applying repeatedly.** A higher-order function can call the same operation several times in sequence, each time feeding the previous result back in:

```text
3 -> add_two -> 5 -> add_two -> 7 -> add_two -> 9
```

**Where this matters later.** Passing functions as values is directly useful for preprocessing, scoring, and configurable data pipelines, where the same pipeline structure applies different operations to different inputs.

### lambda expressions

A `lambda` expression creates a function object in a single line: `lambda parameters: expression`. The expression after the colon _is_ the return value, there's no explicit `return` statement, and a lambda is restricted to exactly one expression (unlike a `def` function, which can hold multiple statements).

```python
square = lambda x: x * x
square(5)      # 25
```

**Lambdas are ordinary function objects**, they can be assigned to a variable, passed as an argument, stored in a list, or returned from another function, exactly like a `def`-defined function.

```python
operations = [lambda x: x + 1, lambda x: x * 2]
operations[1](5)      # 10
```

**Lambda as an argument** is especially useful when a function is needed only at one call site, with no need to give it a separate name first: `transform_all(values, lambda x: x * 10)`.

**Lambda and closures combine directly**, a lambda can retain access to an enclosing variable exactly like a nested `def` function can:

```python
def make_multiplier(factor):
    return lambda x: x * factor
```

**Where this matters later.** Small inline functions are common for transformations, sort keys, and filters, and this reads naturally into the iteration tools covered later.

## Explanation

`alias_and_call` assigns `function` to a local name _before_ calling it through that name, the spec's own "do not call function before assigning it" constraint exists specifically to prove the assignment step itself never calls anything, only the explicit `()` afterward does. `same_function` compares with `is`, never `==` or by calling both and comparing results, since two functions that happen to produce equal outputs are not the same object, only identity answers "is this literally the same function."

`apply_n_times` loops exactly `count` times, feeding each call's result into the next, and returns the original `value` unchanged for `count <= 0`, no calls happen at all in that case, matching the spec rather than "applying zero times" being mistaken for one no-op call. `transform_all` builds a fresh list via a comprehension (`[function(v) for v in values]`) rather than mutating `values` in place, since the input must stay untouched and the result must be a genuinely new list.

`make_square_function` and `make_offset_function` both return a `lambda` rather than a nested `def`, the whole point of this topic is that a lambda is exactly as valid a return value as a named function, and `make_offset_function`'s lambda retains `offset` as a closure the same way a `def`-based closure would. `apply_lambda` accepts "the function may be a lambda or any other one-argument function" literally, it just calls `function(v)` for each element, with no code path that assumes or requires lambda syntax specifically.
