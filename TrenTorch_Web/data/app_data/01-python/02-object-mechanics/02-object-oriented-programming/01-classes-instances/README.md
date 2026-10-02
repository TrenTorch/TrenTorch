---
name: python-oop-classes-instances
title: 'Classes, Instances & __init__'
tags: [python-oop]
difficulty: Beginner
---

## Statement

Implement functions that create instances of a class, attach attributes to them and compare their classes and classes whose instances receive their attributes at creation time through `__init__`, including a class that avoids the mutable default argument bug.

## Theory

### Classes & instances

A **class** defines a new type. `class Point: pass` creates a class object and stores its address in `Point`. **Calling** a class creates a new **instance** of that type:

```python
p = Point()
q = Point()
```

`p is q` is `False` (separate instances); `type(p) is type(q)` is `True` (same class).

**Attributes.** An attribute is a variable belonging to an object, read/written with dot syntax. Each instance keeps its own attributes in a dictionary, available as `obj.__dict__`. Assigning to an attribute creates it if absent:

```python
p.x = 3
q.x = 10           # q has its own x; p.x is still 3
p.__dict__         # {"x": 3}
```

Reading a missing attribute raises `AttributeError`.

**Testing class membership.** `isinstance(obj, Point)` is `True` for `Point` or any subclass; `type(obj) is Point` matches only exactly.

**Where this matters later.** Every PyTorch model is a class instance, with layers and settings as attributes.

### __init__ & instance attributes

`__init__` is a special method Python calls **automatically, immediately after a new instance is created**, with the arguments given when calling the class:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

r = Rectangle(3, 4)
```

`Rectangle(3, 4)` creates a new empty instance, then calls `Rectangle.__init__(new_instance, 3, 4)`. `self` receives the address of that new instance, `self.width = width` stores the parameter's value as an attribute on it.

**`__init__` is an ordinary function**, it can have default values, and the mutable-default-argument issue applies exactly as it does to any function:

```python
class Log:
    def __init__(self, entries=None):
        if entries is None:
            entries = []
        self.entries = entries
```

If a caller passes a list, `self.entries` refers to _that same list_ unless it's explicitly copied (`self.entries = list(entries)`), otherwise the instance and caller share it.

**Where this matters later.** In PyTorch, layers are created in `__init__`, so the constructor is where a model's structure is defined.

## Explanation

`build_instances` calls `cls()` once per iteration of a `range(count)` loop rather than once and copying the result, copying an instance would just share one object under different names, defeating "every instance must be a separate object," while calling the class fresh each time is what actually constructs distinct instances. `attribute_snapshot` returns `dict(obj.__dict__)`, a real, separate copy of the attribute dictionary, rather than `obj.__dict__` itself, since the spec requires that mutating the returned dictionary must not affect the object's real attributes.

`Account.__init__` uses the `history=None` safe-default pattern, then wraps a supplied list in `list(history)` rather than storing it directly, this is what makes "mutate the caller's list afterward" not affect the account, since the account's own `self.history` is a genuinely separate list object holding a copy of the same elements. `Rectangle.__init__` needs no such care, since its `width`/`height` arguments are plain numbers with no shared-mutable-state risk to begin with.
