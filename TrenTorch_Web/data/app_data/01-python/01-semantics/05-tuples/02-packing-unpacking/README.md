---
name: python-tuples-packing-unpacking
title: 'Packing and Unpacking, Including *'
tags: [python-tuples, unpacking]
difficulty: Intermediate
---

## Statement

Implement functions that build tuples from separate values and assign a tuple's elements to separate variables, including extended unpacking with `*`.

## Theory

**Packing** creates a tuple from separate values. **Unpacking** assigns the elements of a sequence to separate variables in one statement:

```python
point = 3, 4              # packing: builds the tuple (3, 4)
x, y = point               # unpacking
```

Unpacking works on **any iterable**, not only tuples — lists and strings unpack too. The number of variables must match the number of elements, or a `ValueError` is produced.

**Swapping.** In `a, b = b, a`, the right-hand side is evaluated **first**, packing the current values of `b` and `a` into a tuple before either variable is reassigned — no temporary variable needed.

**Extended unpacking with `*`.** One variable may be marked with `*`; it receives **all the elements not assigned to the other variables**, as a **list**:

```python
first, *rest = (1, 2, 3, 4)        # first = 1,  rest = [2, 3, 4]
first, *mid, last = (1, 2, 3, 4)   # mid = [2, 3]
first, *mid, last = (1, 2)         # mid = []
```

Only one starred variable is allowed per left-hand side.

**Unpacking in loops.** A `for` variable can be a pattern: `for index, (x, y) in enumerate(pairs): ...`.

**Where this matters later.** Extended unpacking splits a batch or a shape into leading and trailing parts (`batch, *dims = shape`). Unpacking is also how functions returning several values are used.

## Explanation

`rotate_three` performs the rotation as one multiple-assignment statement, `a, b, c = b, c, a`, matching the theory's swap example exactly — the right-hand tuple is packed from the _current_ values before any reassignment happens, so there's no risk of an intermediate assignment clobbering a value the next one still needs. `head_and_tail` and `ends_and_middle` both special-case an empty/too-short input before attempting the unpack, since `head, *tail = seq` raises `ValueError` on an empty sequence rather than producing an empty result.
