---
name: python-oop-why-methods-take-self
title: Why Methods Take self
tags: [python-oop]
difficulty: Intermediate
---

## Statement

Implement a class with methods that act on the instance they are called on, and functions that call methods explicitly through the class to expose what `self` really is.

## Theory

A **method** is a function defined inside a class body. Calling it on an instance, `obj.method(args)`, passes `obj` automatically as the **first argument**. `self` is just the conventional name for that first parameter — nothing about the word itself is special.

```python
c.increment(5)
Counter.increment(c, 5)     # exactly equivalent
```

Because the function was found *through an instance*, Python builds a **bound method**: an object storing the function and the instance together. Inside the method, `self` is a parameter that stores the same address as the caller's instance — mutating `self.count` mutates the one object both variables refer to.

**Common consequences:**
- Forgetting `self` in the definition raises `TypeError` (the call passes one more argument than the function accepts).
- Inside a method, a bare `count` (without `self.`) refers to a different variable entirely, not the attribute.
- Reassigning `self` inside a method only changes the local parameter — it never changes the caller's instance.
- A method that **returns `self`** enables chaining: `c.increment(1).increment(2)` works because each call returns the same instance the next call runs on.

**Where this matters later.** PyTorch's `forward` and `nn.Module` methods rely on `self` to reach parameters stored on the instance.

## Explanation

`Accumulator.add` returns `self` at the end, which is exactly what makes `chain_adds` able to write one unbroken expression (`acc.add(n1).add(n2)...`) instead of reassigning a variable after each call — each `.add()` call's return value is the same instance the next `.add()` runs on. `add_via_class` calls `Accumulator.add(acc, x)` — the unbound function looked up on the class itself, with `acc` supplied explicitly as the first argument — which is the literal mechanism `acc.add(x)` already performs automatically; the two must produce identical results because they're the same call. `bound_method_target` reads `method.__self__`, the actual attribute a bound method object carries specifically to remember which instance it's bound to.
