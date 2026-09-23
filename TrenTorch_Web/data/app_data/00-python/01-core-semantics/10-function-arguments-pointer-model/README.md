---
name: python-function-arguments-pointer-model
title: Function Arguments (Pointer Model)
tags: [python-core, functions, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that revisit the basic function-calling syntax from earlier in this module, now demonstrating exactly what gets passed into a function's parameters, and how the mutability of the argument's type determines whether changes are visible to the caller.

## Theory

The "What a Function Is" topic covered calling a function and passing arguments, without explaining what actually happens to those arguments internally. That's covered here, now that objects, variables, and mutability have all been introduced.

When you call `f(x)`, Python copies the **value stored inside `x`** into `f`'s parameter variable. If `x` refers to an object, that value is the object's address — so the parameter ends up storing the same address `x` stores. No object is copied; only the address is copied, into a new variable slot (the parameter).

**Consequence for mutable arguments:** if `f` mutates the object `param` refers to (e.g. `param.append(4)`), that mutation happens at the same address `x` refers to. So the caller's `x`, read after `f` returns, reflects the change.

**Consequence for reassigning a parameter:** if `f` reassigns `param` to something new (e.g. `param = ["new", "list"]`), this only ever changes what `param` itself stores — a local variable slot — never what `x` stores. `x` outside `f` still stores the original address; it never sees this reassignment. This holds for *any* reassignment of a parameter inside a function, not just literally-immutable types — even reassigning a parameter that started out pointing at a mutable object only changes that parameter's own stored value, not the caller's variable.

```python
def try_to_replace(param):
    param = ["new", "list"]     # only repoints the local `param` variable

x = [1, 2, 3]
try_to_replace(x)
print(x)     # still [1, 2, 3] — x was never touched
```

```python
def actually_mutate(param):
    param.append("added")       # mutates the object param points to

x = [1, 2, 3]
actually_mutate(x)
print(x)     # [1, 2, 3, "added"] — visible, because the shared object was mutated
```

## Explanation

`append_in_place` and `attempt_reassign` are deliberately paired opposites operating on the same kind of argument (a list), so the hidden tests can isolate exactly one variable — mutate vs. reassign — while holding the argument's mutability constant. `add_one` repeats the same "does the caller see this?" question for an `int`, where the answer is a foregone "no" (ints have no mutating methods at all), included so the behavior is confirmed for an immutable type too rather than only ever demonstrated on lists.
