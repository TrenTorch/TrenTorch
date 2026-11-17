---
name: problem-1-compute-a-stable-l2-norm
title: 'Compute a Stable L2 Norm'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'divide by the largest absolute entry before squaring'
tools: [NumPy]
---

## Statement

Compute the Euclidean (L2) norm of a non-empty real vector. Entries may be extremely large or extremely small, so the computation must not overflow or underflow.

Implement `solve(x)`.

**Returns.** Return the norm as a Python float. The all-zero vector has norm `0.0`.

### Examples

**Example 1**

Input:

```python
solve([3.0, 4.0])
```

Output:

```text
5.0
```

**Example 2**

Input:

```python
solve([3e200, 4e200])
```

Output:

```text
5e+200
```

## Theory

### The simple version

The L2 norm is the straight-line length of a vector: square every entry, add the squares, take the square root. The catch is numerical. Squaring a very large number overflows to infinity, and squaring a very small one underflows to zero, even when the true length is a perfectly ordinary number.

### The formula

$$\|x\|_2=\sqrt{\sum_i x_i^2}=s\sqrt{\sum_i \left(\frac{x_i}{s}\right)^2},\qquad s=\max_i |x_i|$$

Both sides are equal, but the right-hand form never squares anything larger than 1.

### Why it matters

- Squaring a very large number overflows to infinity and squaring a very small one underflows to zero, even when the true length is an ordinary number.
- Norms appear everywhere (gradient clipping, normalisation, distances), so a silent overflow here corrupts everything built on top.

### How it works

1. Find the largest magnitude $s=\max_i|x_i|$. If $s=0$ the answer is $0$.
2. Divide every entry by $s$, so every entry now lies in $[-1,1]$.
3. Square, add up and take the square root of the scaled entries.
4. Multiply by $s$ to restore the original scale.

### Worked example

For $x=(3,4)$ the largest magnitude is $s=4$. The scaled vector is $(0.75,1)$, its squares add to $0.5625+1=1.5625$, the square root is $1.25$, and $1.25\times4=5.0$.

## Explanation

Dividing by the largest magnitude $s$ first keeps every squared term at most 1, so nothing overflows, and multiplying by $s$ at the end restores the scale. The all-zero vector would make $s=0$ and divide by zero, so it is returned directly as `0.0`.
