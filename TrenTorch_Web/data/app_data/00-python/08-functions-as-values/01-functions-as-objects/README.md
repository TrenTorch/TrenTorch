---
name: python-functions-as-values-objects
title: Functions Are Objects and Can Be Assigned to Variables
tags: [python-functions-as-values]
difficulty: Beginner
---

## Statement

Implement functions that treat functions like ordinary values: assign them to variables, store them in collections, and use the assigned reference to call them.

## Theory

A function's name is a variable — like any other, it stores the address of an object. Writing the bare name refers to the **function object**; writing the name with `()` **calls** it.

```python
def square(x):
    return x * x

f = square       # stores the function object; does NOT call it
f = square(5)    # calls square; f now refers to 25, an int
```

`f = square` creates another variable pointing at the *same* function object — it doesn't create a second function.

**Functions in collections.** Since functions are objects, they can be stored in lists and dictionaries: `operations = [add_one, double]`, and `operations[0](10)` retrieves the function then calls it.

**Function identity.** Two variables can refer to the exact same function object — `a is b` is `True` when both point at one function, the same identity concept from Module 1.

**Where this matters later.** Functions as objects are the foundation for passing transformations, callbacks, and sorting keys around as data.

## Explanation

`alias_and_call` assigns `function` to a local name *before* calling it through that name — the spec's own "do not call function before assigning it" constraint exists specifically to prove the assignment step itself never calls anything, only the explicit `()` afterward does. `same_function` compares with `is`, never `==` or by calling both and comparing results, since two functions that happen to produce equal outputs are not the same object — only identity answers "is this literally the same function."
