---
name: numpy-elementwise-arithmetic
title: Element-Wise Arithmetic
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions performing basic arithmetic between arrays, establishing exactly what "element-wise" means.

## Theory

Standard arithmetic operators (`+`, `-`, `*`, `/`, `**`) applied to arrays of the same shape operate **element-wise**: each result position comes from the corresponding positions in the inputs, independently of every other position.

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
a + b     # [11, 22, 33]
a * b     # [10, 40, 90]
```

`*` always means element-wise multiplication for ndarrays — never matrix multiplication (covered in Module 7).

Every result of an element-wise operation is a genuinely new array — this is the "copy" side of Module 3's view/copy rule, since new data needs a new buffer.

**In-place variants** (`+=`, `-=`, `*=`, `/=`) mutate the existing buffer directly, matching the reassignment-vs-mutation distinction from Python Foundations:

```python
arr += 1     # mutates arr's existing buffer in place
arr = arr + 1     # creates a new array, reassigns arr
```

## Explanation

`elementwise_multiply` returns `a * b`. `increment_in_place` mutates with `arr += amount`, never reassigning `arr`. `square_each` returns `arr ** 2`, a new array — `arr` itself is never touched.
