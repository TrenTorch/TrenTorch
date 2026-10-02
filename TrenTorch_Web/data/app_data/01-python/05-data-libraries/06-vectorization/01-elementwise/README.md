---
name: numpy-elementwise-operations
title: 'Element-Wise Operations'
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions performing basic arithmetic between arrays, establishing exactly what "element-wise" means, and applying common mathematical functions across whole arrays at once.

## Theory

### Element-wise arithmetic

Standard arithmetic operators (`+`, `-`, `*`, `/`, `**`) applied to arrays of the same shape operate **element-wise**: each result position comes from the corresponding positions in the inputs, independently of every other position.

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
a + b     # [11, 22, 33]
a * b     # [10, 40, 90]
```

`*` always means element-wise multiplication for ndarrays, never matrix multiplication (covered in Module 7).

Every result of an element-wise operation is a genuinely new array, this is the "copy" side of Module 3's view/copy rule, since new data needs a new buffer.

**In-place variants** (`+=`, `-=`, `*=`, `/=`) mutate the existing buffer directly, matching the reassignment-vs-mutation distinction from Python Foundations:

```python
arr += 1     # mutates arr's existing buffer in place
arr = arr + 1     # creates a new array, reassigns arr
```

### Universal functions

A **universal function**, or **ufunc**, operates element-wise across an entire array in a single call, the arithmetic operators themselves are implemented as ufuncs internally.

```python
np.sqrt(np.array([1.0, 4.0, 9.0]))     # [1.0, 2.0, 3.0]
np.exp(np.array([0.0, 1.0, 2.0]))       # [1.0, 2.718..., 7.389...]
np.log(np.array([1.0, 2.718..., 7.389...]))   # inverse of exp
```

Common ufuncs: `np.sqrt`, `np.exp`, `np.log`, `np.sin`/`np.cos`/`np.tan`, `np.abs`, and more, all applying their single-input operation to every element independently, returning a new array of the same shape.

Some ufuncs take two arrays, `np.add`, `np.multiply`, `np.power` are the actual ufuncs underlying `+`, `*`, `**`.

## Explanation

`elementwise_multiply` returns `a * b`. `increment_in_place` mutates with `arr += amount`, never reassigning `arr`. `square_each` returns `arr ** 2`, a new array, `arr` itself is never touched.

Each function is a direct call to the matching ufunc: `np.sqrt(arr)`, `np.exp(arr)`, `np.log(arr)`, `np.abs(arr)`. Every one preserves the input's shape, since a ufunc always produces one output value per input element.
