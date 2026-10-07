---
name: problem-3-cosine-similarity
title: 'Cosine Similarity'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'dot product over the product of the two norms'
tools: [NumPy]
---

## Statement

Compute the cosine of the angle between two equal-length vectors.

Implement `solve(a, b)`.

**Returns.** Return a float in $[-1, 1]$. If either vector is all zeros the angle is undefined and the function returns `0.0`.

### Examples

**Example 1**

Input:

```python
solve([1.0, 0.0], [1.0, 1.0])
```

Output:

```text
0.707107
```

**Example 2**

Input:

```python
solve([1.0, 2.0], [-1.0, -2.0])
```

Output:

```text
-1.0
```

## Theory

### The simple version

Cosine similarity compares direction and ignores length. A value of 1 means the vectors point the same way, 0 means they are perpendicular, and -1 means they point in opposite directions.

### The formula

$$\cos\theta=\frac{a\cdot b}{\|a\|_2\,\|b\|_2}$$

## Explanation

The dot product is divided by the product of the two norms. The zero-vector guard returns `0.0` instead of dividing by zero, which is the usual convention for "no similarity".
