---
name: python-oop-classes-and-instances
title: Classes and Instances
tags: [python-oop]
difficulty: Beginner
---

## Statement

Implement functions that create instances of a class, attach attributes to them, and compare their classes, establishing what a class is and how instances relate to it.

## Theory

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

## Explanation

`build_instances` calls `cls()` once per iteration of a `range(count)` loop rather than once and copying the result — copying an instance would just share one object under different names, defeating "every instance must be a separate object," while calling the class fresh each time is what actually constructs distinct instances. `attribute_snapshot` returns `dict(obj.__dict__)` — a real, separate copy of the attribute dictionary — rather than `obj.__dict__` itself, since the spec requires that mutating the returned dictionary must not affect the object's real attributes.
