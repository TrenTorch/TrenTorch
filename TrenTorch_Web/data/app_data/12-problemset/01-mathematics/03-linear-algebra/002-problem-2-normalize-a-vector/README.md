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

### Why it matters

- After normalisation only the direction of a vector matters, not its size, which is what similarity measures and many layers need.
- Returning `nan` for a zero vector would hide a bug upstream, so the function refuses to guess a direction.

### How it works

1. Compute the length $\|x\|_2$.
2. If it is $0$, raise `ValueError`.
3. Divide every entry by the length.

### Worked example

For $x=(3,4)$ the length is $\sqrt{9+16}=5$, so the result is $(3/5,4/5)=$ [0.6, 0.8]. Its length is $\sqrt{0.36+0.64}=1$.

## Explanation

The norm is computed once and every entry is divided by it. A zero vector would divide $0$ by $0$, and quietly returning NaNs would hide the bug upstream, so the function raises `ValueError` instead.
