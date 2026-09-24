---
name: python-oop-init-instance-attributes
title: __init__ and Instance Attributes
tags: [python-oop]
difficulty: Beginner
---

## Statement

Implement classes whose instances receive their attributes at creation time through `__init__`, including a class that avoids the mutable default argument bug.

## Theory

`__init__` is a special method Python calls **automatically, immediately after a new instance is created**, with the arguments given when calling the class:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

r = Rectangle(3, 4)
```

`Rectangle(3, 4)` creates a new empty instance, then calls `Rectangle.__init__(new_instance, 3, 4)`. `self` receives the address of that new instance — `self.width = width` stores the parameter's value as an attribute on it.

**`__init__` is an ordinary function** — it can have default values, and the mutable-default-argument issue applies exactly as it does to any function:

```python
class Log:
    def __init__(self, entries=None):
        if entries is None:
            entries = []
        self.entries = entries
```

If a caller passes a list, `self.entries` refers to *that same list* unless it's explicitly copied (`self.entries = list(entries)`) — otherwise the instance and caller share it.

**Where this matters later.** In PyTorch, layers are created in `__init__`, so the constructor is where a model's structure is defined.

## Explanation

`Account.__init__` uses the `history=None` safe-default pattern, then wraps a supplied list in `list(history)` rather than storing it directly — this is what makes "mutate the caller's list afterward" not affect the account, since the account's own `self.history` is a genuinely separate list object holding a copy of the same elements. `Rectangle.__init__` needs no such care, since its `width`/`height` arguments are plain numbers with no shared-mutable-state risk to begin with.
