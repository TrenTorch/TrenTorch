---
name: python-oop-class-vs-instance-attributes
title: Class Attributes vs Instance Attributes
tags: [python-oop]
difficulty: Intermediate
---

## Statement

Implement a class that tracks how many instances exist using a class attribute, and a function that reports where an attribute is found, exposing how attribute lookup works.

## Theory

An **instance attribute** lives in one instance's own attribute dictionary (usually set via `self.attr = ...` in `__init__`). A **class attribute** lives on the class object itself, created by assigning in the class body outside any method:

```python
class Tracker:
    count = 0                    # class attribute: one slot, on the class object

    def __init__(self, label):
        self.label = label       # instance attribute: one slot per instance
        Tracker.count = Tracker.count + 1
```

**Lookup order** for `obj.attr`: the instance's own attributes first, then the class's (and its parents'). The first match wins; `AttributeError` if neither has it. Class attributes act as shared defaults every instance can read.

**Assignment always targets the instance.** `obj.attr = value` *always* creates/updates an instance attribute, even if the class already has one of that name — it **shadows** the class attribute for that instance only. `Tracker.count` itself is unaffected; to change the shared value, assign through the class: `Tracker.count = ...`.

**Mutable class attributes are shared and dangerous.** `class Bag: items = []` — every instance's `self.items.append(x)` mutates the *one* shared list, since no assignment happens, just an in-place method call. Per-instance mutable data belongs in `__init__`.

**Where this matters later.** Shared mutable class attributes are a common source of bugs when several model instances unexpectedly influence each other.

## Explanation

`Tracker.__init__` increments through the class name (`Tracker.count = Tracker.count + 1`), never `self.count = ...` — the latter would create a brand-new *instance* attribute shadowing the shared counter instead of advancing it, which is exactly the mistake this topic warns against. `where_is_attribute` checks `attr in obj.__dict__` first (instance-only, per its own definition) before falling back to `hasattr(obj, attr)` (which also finds class-level attributes) — the order matters, since checking `hasattr` alone can't distinguish "found on the instance" from "found on the class."
