---
name: python-names-arguments-defaults
title: 'Arguments & Mutable Defaults'
tags: [python-core, functions, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that show exactly what gets passed into a function's parameters and how the mutability of the argument's type decides whether changes are visible to the caller, plus a function that avoids the mutable default argument trap and a diagnostic that detects whether a function definition is vulnerable to it.

## Theory

### Function arguments

The "What a Function Is" topic covered calling a function and passing arguments, without explaining what actually happens to those arguments internally. That's covered here, now that objects, variables and mutability have all been introduced.

When you call `f(x)`, Python copies the **value stored inside `x`** into `f`'s parameter variable. If `x` refers to an object, that value is the object's address, so the parameter ends up storing the same address `x` stores. No object is copied; only the address is copied, into a new variable slot (the parameter).

**Consequence for mutable arguments:** if `f` mutates the object `param` refers to (e.g. `param.append(4)`), that mutation happens at the same address `x` refers to. So the caller's `x`, read after `f` returns, reflects the change.

**Consequence for reassigning a parameter:** if `f` reassigns `param` to something new (e.g. `param = ["new", "list"]`), this only ever changes what `param` itself stores, a local variable slot, never what `x` stores. `x` outside `f` still stores the original address; it never sees this reassignment. This holds for _any_ reassignment of a parameter inside a function, not just literally-immutable types, even reassigning a parameter that started out pointing at a mutable object only changes that parameter's own stored value, not the caller's variable.

```python
def try_to_replace(param):
    param = ["new", "list"]     # only repoints the local `param` variable

x = [1, 2, 3]
try_to_replace(x)
print(x)     # still [1, 2, 3], x was never touched
```

```python
def actually_mutate(param):
    param.append("added")       # mutates the object param points to

x = [1, 2, 3]
actually_mutate(x)
print(x)     # [1, 2, 3, "added"], visible, because the shared object was mutated
```

### The mutable default argument

Default argument values in a function definition are evaluated **exactly once**, at the moment the `def` statement itself runs, not each time the function is called. For immutable default values (numbers, strings, `None`), this timing makes no observable difference. For mutable default values, it creates a subtle and common bug.

```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket
```

When Python executes this `def` statement, it creates one list object to serve as the default value for `bucket`. That object is created once and stored as part of the function itself, not recreated per call.

```python
add_item("a")     # bucket defaults to the same shared list; becomes ["a"]
add_item("b")     # bucket AGAIN defaults to that SAME list, which
                   # already contains ["a"]; becomes ["a", "b"]
```

Every call that omits `bucket` reuses a reference to that same shared object. `.append()` mutates it in place, so items accumulate across calls that appear, from the calling code, to be entirely independent.

**The fix** is to default to an immutable placeholder, typically `None`, and create a fresh mutable object inside the function body on each call when needed:

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

Now, each call that omits `bucket` triggers the `if` branch, creating a brand-new list object at a new address every time, no state is shared across calls.

This same reasoning applies to any mutable default: `bucket={}` and `bucket=set()` have the identical problem and the identical fix.

## Explanation

`append_in_place` and `attempt_reassign` are deliberately paired opposites operating on the same kind of argument (a list), so the hidden tests can isolate exactly one variable, mutate vs. reassign, while holding the argument's mutability constant. `add_one` repeats the same "does the caller see this?" question for an `int`, where the answer is a foregone "no" (ints have no mutating methods at all), included so the behavior is confirmed for an immutable type too rather than only ever demonstrated on lists.

`is_vulnerable_to_mutable_default` inspects `func.__defaults__`, a real tuple Python attaches to every function object holding its positional defaults in order, checking each element's type against `(list, dict, set)` is a direct, general way to detect the trap without needing to parse source code or run the function.
