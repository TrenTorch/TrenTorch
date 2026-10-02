---
name: python-oop-methods-attributes
title: 'Methods, self & Class Attributes'
tags: [python-oop]
difficulty: Intermediate
---

## Statement

Implement a class with methods that act on the instance they are called on, functions that call methods explicitly through the class to expose what `self` really is and a class that tracks how many instances exist using a class attribute, exposing how attribute lookup works.

## Theory

### Why methods take self

A **method** is a function defined inside a class body. Calling it on an instance, `obj.method(args)`, passes `obj` automatically as the **first argument**. `self` is just the conventional name for that first parameter, nothing about the word itself is special.

```python
c.increment(5)
Counter.increment(c, 5)     # exactly equivalent
```

Because the function was found _through an instance_, Python builds a **bound method**: an object storing the function and the instance together. Inside the method, `self` is a parameter that stores the same address as the caller's instance, mutating `self.count` mutates the one object both variables refer to.

**Common consequences:**

- Forgetting `self` in the definition raises `TypeError` (the call passes one more argument than the function accepts).
- Inside a method, a bare `count` (without `self.`) refers to a different variable entirely, not the attribute.
- Reassigning `self` inside a method only changes the local parameter, it never changes the caller's instance.
- A method that **returns `self`** enables chaining: `c.increment(1).increment(2)` works because each call returns the same instance the next call runs on.

**Where this matters later.** PyTorch's `forward` and `nn.Module` methods rely on `self` to reach parameters stored on the instance.

### Class attributes vs instance attributes

An **instance attribute** lives in one instance's own attribute dictionary (usually set via `self.attr = ...` in `__init__`). A **class attribute** lives on the class object itself, created by assigning in the class body outside any method:

```python
class Tracker:
    count = 0                    # class attribute: one slot, on the class object

    def __init__(self, label):
        self.label = label       # instance attribute: one slot per instance
        Tracker.count = Tracker.count + 1
```

**Lookup order** for `obj.attr`: the instance's own attributes first, then the class's (and its parents'). The first match wins; `AttributeError` if neither has it. Class attributes act as shared defaults every instance can read.

**Assignment always targets the instance.** `obj.attr = value` _always_ creates/updates an instance attribute, even if the class already has one of that name, it **shadows** the class attribute for that instance only. `Tracker.count` itself is unaffected; to change the shared value, assign through the class: `Tracker.count = ...`.

**Mutable class attributes are shared and dangerous.** `class Bag: items = []`, every instance's `self.items.append(x)` mutates the _one_ shared list, since no assignment happens, just an in-place method call. Per-instance mutable data belongs in `__init__`.

**Where this matters later.** Shared mutable class attributes are a common source of bugs when several model instances unexpectedly influence each other.

## Explanation

`Accumulator.add` returns `self` at the end, which is exactly what makes `chain_adds` able to write one unbroken expression (`acc.add(n1).add(n2)...`) instead of reassigning a variable after each call, each `.add()` call's return value is the same instance the next `.add()` runs on. `add_via_class` calls `Accumulator.add(acc, x)`, the unbound function looked up on the class itself, with `acc` supplied explicitly as the first argument, which is the literal mechanism `acc.add(x)` already performs automatically; the two must produce identical results because they're the same call. `bound_method_target` reads `method.__self__`, the actual attribute a bound method object carries specifically to remember which instance it's bound to.

`Tracker.__init__` increments through the class name (`Tracker.count = Tracker.count + 1`), never `self.count = ...`, the latter would create a brand-new _instance_ attribute shadowing the shared counter instead of advancing it, which is exactly the mistake this topic warns against. `where_is_attribute` checks `attr in obj.__dict__` first (instance-only, per its own definition) before falling back to `hasattr(obj, attr)` (which also finds class-level attributes), the order matters, since checking `hasattr` alone can't distinguish "found on the instance" from "found on the class."
