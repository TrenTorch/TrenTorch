---
name: problem-2-normalize-a-vector
title: 'Normalize a Vector'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'compute the norm once and divide every component by it'
tools: [NumPy]
---

## Statement

Implement `solve(x)`. Return a unit vector in the direction of a non-zero input vector.

### Examples

**Example 1**

Input:

```python
solve([3.0, 4.0])
```

Output:

```text
[0.6, 0.8]
```

**Example 2**

Input:

```python
solve([-5.0, 0.0])
```

Output:

```text
[-1.0, 0.0]
```

## Theory

A vector is normalized by dividing each coordinate by its Euclidean length, making the output length one.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
