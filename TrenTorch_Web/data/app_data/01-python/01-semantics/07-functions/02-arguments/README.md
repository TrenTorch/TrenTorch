---
name: python-functions-arguments
title: Arguments
tags: [python-function-arguments, python-function-defaults, python-args-kwargs]
difficulty: Intermediate
---

## Statement

Implement functions called with positional arguments, keyword arguments and combinations of both, with optional parameters whose defaults are evaluated when the function is defined and that accept a variable number of arguments using `*args` and `**kwargs`.

## Theory

### Positional vs keyword arguments

**Positional arguments** are matched by position: `describe("A", 18, "Delhi")` sends `"A"` to the first parameter, `18` to the second and so on.

**Keyword arguments** identify their parameter by name, and their order doesn't need to match the parameter order: `describe(city="Delhi", name="A", age=18)`.

**Mixing** is allowed as long as positional arguments come first: `describe("A", age=18, city="Delhi")` is valid; a positional argument after a keyword argument is a syntax error.

**Repeating a parameter**, supplying the same parameter both positionally and by keyword in one call, raises `TypeError`, since Python can't decide which value that parameter should get.

**Positional-only and keyword-only parameters.** `def f(a, b, /, c)` forces `a` and `b` to be positional; `def f(a, *, b, c)` forces `b` and `c` to be keyword-only. Neither of these forms is required for an ordinary function to already accept both calling styles.

**Where this matters later.** Keyword arguments are common in ML APIs, where functions often have many configuration parameters.

### Default arguments

A parameter can have a **default value**, used only when the caller omits it:

```python
def add(a, b=10):
    return a + b

add(5)       # a=5, b=10 (default used)
add(5, 20)   # a=5, b=20 (default not used)
```

**Default values are bound at definition time.** Changing a variable used as a default afterward does not change the already-created default, it's part of the function object from the moment `def` runs.

**Mutable defaults are reused across calls that omit the argument**, the exact issue from the very first module. The safe pattern is defaulting to `None` and creating a fresh object inside the function body:

```python
def collect(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items
```

**Immutable defaults** (numbers, strings, tuples) don't have this problem, since there's nothing to mutate.

**Ordering.** A required parameter cannot follow a parameter with a default in the plain parameter list, `def f(a=1, b)` is invalid; `def f(a, b=1, c=2)` is fine.

**Where this matters later.** The binding rule matters in long-running programs and ML code where a mutable default could silently preserve state between calls.

### *args & **kwargs

`*args` collects extra positional arguments into a **tuple**:

```python
def total(*values):
    ...

total(1, 2, 3)     # values == (1, 2, 3)
total()            # values == ()
```

`**kwargs` collects extra keyword arguments into a **dictionary**:

```python
def configure(**kwargs):
    ...

configure(batch_size=32, device="cpu")   # kwargs == {"batch_size": 32, "device": "cpu"}
```

Both can combine with ordinary parameters and each other: `def process(required, *args, **kwargs)` sends the first positional argument to `required`, the rest to `args` and every keyword argument to `kwargs`.

**Unpacking when calling.** The same syntax unpacks a sequence into positional arguments (`total(*values)`) or a dictionary into keyword arguments (`configure(**options)`).

Since `*args` is a real tuple and `**kwargs` a real dictionary, tuple and dictionary operations (unpacking, `.items()`, etc.) work on them directly inside the function.

**Where this matters later.** Variable argument handling is common in reusable utilities and is the foundation for decorators and higher-order functions, where one function needs to accept and forward another function's arguments.

## Explanation

None of these three functions restricts its parameters with `/` or `*`, an ordinary `def` already accepts positional calls, all-keyword calls, and any valid mix of the two, since Python's default parameter-matching rules (position first, then name) apply automatically. The functions exist to prove that fact with real calling-convention tests, not to add code that enables it.

`append_value` uses the `items=None` safe pattern rather than `items=[]`, so a call that omits `items` gets a genuinely fresh list every time, while a call that _does_ supply a list mutates that exact object (matching "return the same list object" in the spec), one function correctly handling both the "give me a new list" and "mutate my list" cases. `power`, `make_label`, and `describe_config` all use plain immutable defaults (`2`, `"item"`, `True`/`3`), which need no such care since there's no shared mutable state to leak between calls.

`summarize` builds its result dict as `{"required": required, "values": values, "options": options}` directly, `values` is already the tuple `*values` collected, and `options` is already the dict `**options` collected, so no repacking is needed; the spec's "do not modify any input objects" is automatically satisfied since neither is touched, only read. `call_with_options` forwards with `function(*args, **options)`, the same `*`/`**` unpacking syntax used when _calling_, which is exactly how a generic wrapper forwards an arbitrary call it received, the pattern the theory calls out as the foundation for decorators.
