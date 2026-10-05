---
name: python-oop-inheritance-duck-typing
title: 'Inheritance & Duck Typing'
tags: [python-oop, inheritance, python-numpy-bridge]
difficulty: Intermediate
---

## Statement

Implement a small hierarchy of shape classes in which a base class relies on methods that its subclasses override, using `super()` to reuse the parent's initialization and functions that work with any object supporting the required operations instead of checking types.

## Theory

### Inheritance & overriding

A class can specialize another by naming it as a **parent**: `class Square(Shape):`. The child **inherits** every attribute and method of the parent, searched in **method resolution order**, instance, class, then parent classes, then `object`.

```python
class Shape:
    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"

class Square(Shape):
    def area(self):
        return self.side * self.side
```

`Square(3).describe()` works even though `Square` never defines `describe`, lookup finds it on `Shape`.

**Overriding.** A child method with the same name as the parent's is found first, replacing the parent's behavior for instances of the child, the parent itself is unchanged.

**Polymorphism.** `self.area()` inside `describe` is looked up on the _actual instance_, the same `describe` code runs for every subclass and calls whichever `area` that instance's own class provides.

**`super()`** lets a child extend rather than replace a parent's method, most importantly `__init__`:

```python
class Square2(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)      # runs Rectangle.__init__ on this same instance
```

If a child defines `__init__` and never calls the parent's, the parent's attributes are simply never created.

**Testing relationships.** `isinstance(obj, Shape)` is `True` for `Shape` or any subclass; `issubclass(Square2, Rectangle)` tests a class-to-class relationship.

**Where this matters later.** Every PyTorch model subclasses `nn.Module`, calls `super().__init__()` first, and overrides `forward`, this exact pattern.

### Duck typing

Python code rarely asks "what type is this?", it uses the object and relies on it supporting the operations applied to it. This is **duck typing**.

```python
def total_length(containers):
    return sum(len(c) for c in containers)
```

This works for lists, strings, tuples, dicts, sets, ranges, and any class defining `__len__`, it never names a type. `isinstance(c, list)` would reject everything else, including types written later.

**Protocols**, each operation corresponds to special methods: `len(x)` needs `__len__`; `x[i]` needs `__getitem__`; `for v in x` needs `__iter__` (or `__getitem__` with integer indices as a fallback); `x(...)` needs `__call__`.

**Testing for capability.** `hasattr(obj, "__len__")` is the direct way to ask whether an operation is supported.

**Two styles of handling absence:** look-before-you-leap (`if hasattr(...)`) vs. easier-to-ask-forgiveness (`try`/`except`). The second avoids listing every type that might work and is the usual Python approach when many types could be supplied.

**Where this matters later.** NumPy functions accept lists, tuples, arrays, anything readable by position. A custom dataset class only needs `__len__` and `__getitem__` to be usable by a data loader.

## Explanation

`Shape.describe` calls `self.area()`, never a specific subclass's `area` by name, this is what makes it work correctly for `Circle`, `Rectangle`, and `Square` alike without `Shape` needing to know any of them exist, the polymorphism the theory describes. `Square.__init__` calls `super().__init__(side, side)` rather than duplicating `Rectangle.__init__`'s two assignment lines, reusing the parent's logic through `super()` is exactly why `Square` never needs its own `area()` either: it inherits `Rectangle.area()` unchanged, and that method just reads `self.width`/`self.height`, which `super().__init__` already set correctly.

`total_length` and `add_all` never inspect a type at all, `len(c)` and `+` are simply called and trusted to work, exactly the duck-typing style the theory names, which is also what lets both functions work unmodified on a custom class supplying only the needed special method. `Countdown.__getitem__` raises `IndexError` for any `index` outside `0 <= index < start`, which is precisely what lets `list(Countdown(3))` work with **no** `__iter__` defined, Python's fallback iteration protocol calls `__getitem__` with `0, 1, 2, ...` until it sees that exact exception. `first_or_none` catches `(IndexError, KeyError, TypeError)` rather than checking `obj`'s type first, since the "ask forgiveness" style is what lets one function handle lists, dicts and unsubscriptable objects alike without naming any of them.
