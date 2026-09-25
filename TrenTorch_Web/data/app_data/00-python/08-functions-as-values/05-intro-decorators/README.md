---
name: python-functions-as-values-intro-decorators
title: Intro to Decorators
tags: [python-decorators]
difficulty: Intermediate
---

## Statement

Implement simple decorators that wrap another function, allowing behavior to be added before or after the original function runs.

## Theory

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

**Preserving the original result** matters — if the wrapper calls `function()` but doesn't `return` its result, the decorated function silently starts returning `None`, a common decorator bug.

**Wrapping functions with arguments.** A general-purpose wrapper accepts anything with `*args, **kwargs` and forwards them: `return function(*args, **kwargs)`.

**Where this matters later.** Decorators are widely used for logging, timing, validation, and instrumentation without rewriting the underlying function.

## Explanation

`add_call_count` stores its counter as an attribute on the wrapper function itself (`wrapper.calls`), initialized once right after `wrapper` is defined — this keeps the count trivially inspectable from outside (`wrapped.calls`) while still being private to that one wrapper, since each call to `add_call_count` creates a brand-new `wrapper` function object with its own attribute, never shared across different decorated functions. `run_with_message` and `decorate_result` both forward with `function(*args, **kwargs)` / `function(x)` and return the result directly — `message`/`prefix` are handled entirely separately from the forwarded call, never smuggled into the wrapped function's own arguments.
