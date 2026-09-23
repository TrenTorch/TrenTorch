---
name: python-what-a-function-is
title: What a Function Is
tags: [python-core, functions]
difficulty: Beginner
---

## Statement

Implement several small functions, establishing the basic syntax for defining, calling, and returning values from a function before anything about how arguments are passed internally is introduced.

## Theory

A function is a named, reusable block of code that can be run whenever you call its name, optionally with input values, and can optionally give back a result.

You define a function with `def`, a name, parentheses containing its **parameters** (the inputs it accepts), and a colon. The indented lines beneath belong to the function's body.

```python
def greet(name):
    print("Hello, " + name)
```

This defines the function but does not run it. To run it, you **call** it by writing its name followed by parentheses containing the actual value(s) to use — called **arguments**.

```python
greet("Sam")     # runs the function body with name set to "Sam"
```

**Parameters vs arguments:** `name` in the definition is a parameter — a placeholder for whatever value will be provided. `"Sam"` in the call is the argument — the actual value supplied for that call. A function can be called many times with different arguments, and each call runs the body fresh with those specific values.

```python
greet("Sam")
greet("Alex")
```

**`return`** gives a value back to whatever called the function, and immediately ends the function's execution — any code after a `return` statement in the same function does not run for that call.

```python
def add(a, b):
    return a + b

result = add(3, 4)     # result now holds 7
```

A function that never has a `return` statement (like `greet` above) automatically gives back the special value `None` when called — this is why calling `greet("Sam")` and trying to store its result would give you `None`, not the printed text.

A function can take any number of parameters, including none at all:

```python
def say_hi():
    return "hi"
```

**Why functions exist:** without them, any block of logic you need more than once would have to be retyped every time, and any change to that logic would have to be made in every copy. A function lets you write the logic once, give it a name, and reuse it by calling that name — anywhere, any number of times, with different inputs each time.

What actually happens to the arguments you pass in — specifically, whether the function receives a copy of the value or something else — is covered later in this module, once the idea of a variable's underlying pointer mechanism has been introduced.

## Explanation

`apply_twice` is the one function here that isn't a one-liner arithmetic check — it exists specifically to prove a function is a first-class value that can be passed around and called through a parameter name, not just invoked by its own literal name. Calling `func(value)` and then `func(...)` again on that result, rather than hardcoding what `func` is, is what the hidden tests use to confirm the implementation actually calls the passed-in function twice in sequence rather than special-casing a known function.
