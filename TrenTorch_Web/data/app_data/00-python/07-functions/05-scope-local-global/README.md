---
name: python-functions-scope-local-global
title: "Scope: Local vs Global"
tags: [python-scope]
difficulty: Intermediate
---

## Statement

Implement functions that use local variables and controlled access to global variables.

## Theory

A variable created inside a function belongs to that function's **local scope** and is not accessible outside it. Each call gets its own separate local variables.

A variable created at module level is in **global scope**. A function can **read** a global variable freely:

```python
limit = 100

def is_valid(value):
    return value < limit
```

But **assigning** to a variable of that name inside a function creates a new *local* variable by default — it does not change the global:

```python
limit = 100

def change():
    limit = 200      # creates a local `limit`; the global is untouched
```

The **`global`** statement tells Python that assignment to a name inside the function should target the module-level variable instead:

```python
limit = 100

def change():
    global limit
    limit = 200      # now changes the global
```

`global` is only needed for **assignment** (and other binding operations), never for reading.

**Scope and mutation are different questions.** Mutating an object a global variable refers to (`items.append(1)`) doesn't require `global`, since the variable itself is never reassigned — only reassigning the variable (`items = [1]`) does.

**Where this matters later.** Understanding scope is necessary for predictable functions and later for closures and decorators.

## Explanation

`local_double` and `read_limit` need no `global` statement at all — they only create/read local variables and parameters, never rebind anything at module level. `increment_global` uses `global COUNTER` specifically because it *reassigns* `COUNTER` (`COUNTER = COUNTER + 1`), which without the `global` declaration would instead create a local variable shadowing it and leave the module-level `COUNTER` untouched. `mutate_shared` needs no `global` either, even though it changes shared state — `items.append(value)` mutates the object the parameter refers to, it never reassigns the parameter itself.
