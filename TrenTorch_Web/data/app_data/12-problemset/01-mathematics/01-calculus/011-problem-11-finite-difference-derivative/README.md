---
name: problem-11-finite-difference-derivative
title: 'Finite Difference Derivative'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'average the slope on both sides of the point'
tools: [NumPy]
---

## Statement

Estimate the derivative $f'(x)$ of a scalar function at a point with a centered finite difference and step `h`.

Implement `solve(f, x, h=1e-5)`.

**Returns.** Return a float.

### Examples

**Example 1**

Input:

```python
solve(lambda t: t**2, 3.0)
```

Output:

```text
6.0
```

**Example 2**

Input:

```python
solve(lambda t: t**3, 2.0)
```

Output:

```text
12.0
```

## Theory

### The simple version

The derivative is the slope of the function. Evaluate the function a tiny step to the right and to the left of the point, and the slope between those two values estimates the slope at the point.

### The formula

$$f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}$$

The error is of order $h^2$, which is much better than the one-sided version.

## Explanation

The centered form cancels the first-order error term that a one-sided difference leaves behind. The default $h=10^{-5}$ balances truncation error (too large an $h$) against floating-point rounding error (too small an $h$). The result is an estimate, so compare it with a tolerance, not exactly.
