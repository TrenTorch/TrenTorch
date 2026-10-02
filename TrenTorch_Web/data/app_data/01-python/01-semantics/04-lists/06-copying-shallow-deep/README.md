---
name: python-lists-copying-shallow-deep
title: 'Copying: Shallow vs Deep'
tags: [python-lists, copying]
difficulty: Intermediate
---

## Statement

Implement functions that copy lists at different depths and verify which objects the copies share, connecting list behavior to the pointer model.

## Theory

**Assignment is not copying.** `b = a` copies the address stored in `a`, so both variables refer to one list. To get a separate list object, a copy must be made explicitly.

**Shallow copy.** Three equivalent forms build a **new list object** whose slots store the **same element addresses** as the original: `b = a.copy()`, `b = list(a)`, `b = a[:]`. The two list objects are separate — appending to `b` does not change `a`. The elements are shared, which is harmless for immutable elements but not for mutable ones:

```python
a = [[1, 2], [3]]
b = a.copy()
b[0].append(99)      # mutates the inner list, which both a and b refer to
print(a)             # [[1, 2, 99], [3]]
```

**Deep copy.** `copy.deepcopy(x)` builds a new object for `x` and, recursively, new objects for everything inside it — nothing is shared with the original. It requires `import copy`.

**Choosing.** Use a shallow copy when elements are immutable or sharing is intended. Use a deep copy when elements are mutable and the copy must be modified independently.

**Where this matters later.** The shallow-versus-deep distinction decides whether modifying a copy of a model configuration, a batch, or a parameter list changes the original.

## Explanation

`shares_inner_objects` pairs up `original` and `duplicate` element-by-element with `zip` and checks `is` on each pair, rather than comparing the lists' overall equality — `is` is what distinguishes "the exact same object" from "an equal-looking copy," which is the whole question a shallow-vs-deep check needs answered. `add_row_safely` deep-copies every existing row plus the new row into a brand-new outer list, rather than shallow-copying `matrix` and appending — a shallow copy would still share every row object with the caller's `matrix`, violating "no row inside matrix may be modified or shared with the returned matrix."
