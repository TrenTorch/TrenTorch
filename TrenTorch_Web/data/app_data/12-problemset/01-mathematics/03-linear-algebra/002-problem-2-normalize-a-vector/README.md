---
name: problem-2-normalize-a-vector
title: 'Normalize a Vector'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'divide by the norm, and reject a zero norm'
tools: [NumPy]
---

## Statement

Return the unit vector that points in the same direction as a non-zero vector.

Implement `solve(x)`.

**Returns.** Return a NumPy array of the same shape with length 1. A zero vector has no direction, so it raises `ValueError`.

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
solve([0.0, 0.0])
```

Output: Raises `ValueError`.

## Theory

### The simple version

Dividing a vector by its own length rescales it to length 1 without changing where it points. Unit vectors are convenient because the dot product of two of them is exactly the cosine of the angle between them.

### The formula

$$\hat x=\frac{x}{\|x\|_2}$$

## Explanation

The norm is computed once and every entry is divided by it. A zero vector would divide $0$ by $0$, and quietly returning NaNs would hide the bug upstream, so the function raises `ValueError` instead.
