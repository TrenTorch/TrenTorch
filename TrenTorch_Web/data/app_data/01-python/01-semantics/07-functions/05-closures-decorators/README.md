---
name: python-functions-closures-decorators
title: 'Closures & Decorators'
tags: [python-closures, python-decorators]
difficulty: Intermediate
---

## Statement

Implement functions that create and return other functions while retaining access to values from the enclosing function, and simple decorators that wrap another function to add behavior before or after it runs.

## Theory

### Closures

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

**Where this matters later.** Closures carry configuration and state without exposing it as a global variable, used in configurable preprocessing, metric functions and caching helpers.

### Decorators

A **decorator** is a function that receives another function and returns a function that wraps it, combining several ideas from this module: functions are objects, they can be passed as arguments, a function can be returned from another function, and a nested function can retain access to an enclosing variable.

```python
def announce(function):
    def wrapper():
        print("starting")
        result = function()
        print("finished")
        return result
    return wrapper
```

`wrapper` is a closure over `function`. Applying it manually is `greet = announce(greet)`; the `@announce` syntax above a `def` does exactly that, rebinding the name to the returned wrapper.

**Preserving the original result** matters, if the wrapper calls `function()` but doesn't `return` its result, the decorated function silently starts returning `None`, a common decorator bug.

**Wrapping functions with arguments.** A general-purpose wrapper accepts anything with `*args, **kwargs` and forwards them: `return function(*args, **kwargs)`.

**Where this matters later.** Decorators are widely used for logging, timing, validation and instrumentation without rewriting the underlying function.

## Explanation

`make_multiplier` and `make_prefixer` both define a small nested function that simply _reads_ the enclosing parameter (`factor`, `prefix`), reading needs no `nonlocal` at all, only assignment does. `make_counter` is the one function here that reassigns its enclosing variable (`count += 1` inside the nested function), which is exactly why it needs `nonlocal count`, omitting it would silently create a function-local `count` that resets to a fresh value every call instead of accumulating.

`add_call_count` stores its counter as an attribute on the wrapper function itself (`wrapper.calls`), initialized once right after `wrapper` is defined, this keeps the count trivially inspectable from outside (`wrapped.calls`) while still being private to that one wrapper, since each call to `add_call_count` creates a brand-new `wrapper` function object with its own attribute, never shared across different decorated functions. `run_with_message` and `decorate_result` both forward with `function(*args, **kwargs)` / `function(x)` and return the result directly, `message`/`prefix` are handled entirely separately from the forwarded call, never smuggled into the wrapped function's own arguments.
