---
name: numpy-incompatible-shapes-and-errors
title: Incompatible Shapes and Reading the Error
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement a function that attempts a broadcasting operation between incompatible shapes, catches NumPy's resulting error, and a function that locates exactly where two shapes fail to be compatible.

## Theory

When two shapes fail the compatibility rule at some aligned dimension, NumPy raises a `ValueError` describing the two shapes it attempted to align.

```python
a = np.ones((2, 3))
b = np.ones((2, 4))
a + b
# ValueError: operands could not be broadcast together with shapes (2,3) (2,4)
```

Reading it means applying the rule in reverse: compare from the right, find where neither dimension is equal nor `1`.

A common mistake: assuming any array with a matching _total size_ will broadcast — it will not. Broadcasting only ever looks at the shape, dimension by dimension, never the total element count:

```python
a = np.ones((6,))
b = np.ones((2, 3))
a + b     # fails — (6,) padded to (1, 6), vs (2, 3): 6 != 3, neither is 1
```

## Explanation

`try_broadcast_add` wraps `a + b` in a `try`/`except ValueError`, reporting `success`/`result` accordingly alongside `a.shape`/`b.shape`. `find_first_incompatible_axis` pads both shapes to equal length with leading `1`s (as in the previous topic), walks the aligned pairs from the right, and returns the negative index of the first pair that's neither equal nor has a `1` — or `None` if every pair passes.
