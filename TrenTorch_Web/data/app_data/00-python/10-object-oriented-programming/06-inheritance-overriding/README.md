---
name: python-oop-inheritance-overriding
title: Inheritance and Method Overriding
tags: [python-oop, inheritance]
difficulty: Intermediate
---

## Statement

Implement a small hierarchy of shape classes in which a base class relies on methods that its subclasses override, using `super()` to reuse the parent's initialization.

## Theory

A class can specialize another by naming it as a **parent**: `class Square(Shape):`. The child **inherits** every attribute and method of the parent, searched in **method resolution order** — instance, class, then parent classes, then `object`.

```python
class Shape:
    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"

class Square(Shape):
    def area(self):
        return self.side * self.side
```

`Square(3).describe()` works even though `Square` never defines `describe` — lookup finds it on `Shape`.

**Overriding.** A child method with the same name as the parent's is found first, replacing the parent's behavior for instances of the child — the parent itself is unchanged.

**Polymorphism.** `self.area()` inside `describe` is looked up on the *actual instance* — the same `describe` code runs for every subclass and calls whichever `area` that instance's own class provides.

**`super()`** lets a child extend rather than replace a parent's method, most importantly `__init__`:

```python
class Square2(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)      # runs Rectangle.__init__ on this same instance
```

If a child defines `__init__` and never calls the parent's, the parent's attributes are simply never created.

**Testing relationships.** `isinstance(obj, Shape)` is `True` for `Shape` or any subclass; `issubclass(Square2, Rectangle)` tests a class-to-class relationship.

**Where this matters later.** Every PyTorch model subclasses `nn.Module`, calls `super().__init__()` first, and overrides `forward` — this exact pattern.

## Explanation

`Shape.describe` calls `self.area()`, never a specific subclass's `area` by name — this is what makes it work correctly for `Circle`, `Rectangle`, and `Square` alike without `Shape` needing to know any of them exist, the polymorphism the theory describes. `Square.__init__` calls `super().__init__(side, side)` rather than duplicating `Rectangle.__init__`'s two assignment lines — reusing the parent's logic through `super()` is exactly why `Square` never needs its own `area()` either: it inherits `Rectangle.area()` unchanged, and that method just reads `self.width`/`self.height`, which `super().__init__` already set correctly.
