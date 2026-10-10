---
name: problem-14-hessian-diagonal
title: 'Hessian Diagonal'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'second difference along each axis, divided by h squared'
tools: [NumPy]
---

## Statement

Estimate the diagonal of the Hessian of a scalar function: the second derivative along each coordinate axis.

Implement `solve(f, x, h=1e-5)`.

**Returns.** Return a NumPy array of length $n$. The values are finite-difference estimates, accurate to roughly three decimals.

### Examples

**Example 1**

Input:

```python
solve(lambda z: float(np.sum(z**2)), [1.0, 2.0])
```

Output:

```text
[2.0, 2.0]
```

**Example 2**

Input:

```python
solve(lambda z: float(np.sum(z**3)), [1.0, 2.0])
```

Output:

```text
[6.0, 12.0]
```

## Theory

### The simple version

The second derivative measures curvature. Compare the function value at the point with the values a small step to either side: if the middle value is lower than the average of the sides, the function curves upward.

### The formula

$$\frac{\partial^2 f}{\partial x_j^2}\approx\frac{f(x+h\,e_j)-2f(x)+f(x-h\,e_j)}{h^2}$$

### Why it matters

- The Hessian diagonal is the curvature along each coordinate axis, used by second-order and diagonal-preconditioned optimisers.
- Computing only the diagonal is much cheaper than the full Hessian.

### How it works

1. For each coordinate $j$, evaluate $f$ at $x+he_j$, $x$ and $x-he_j$.
2. Combine them: $(f(x+he_j)-2f(x)+f(x-he_j))/h^2$.

### Worked example

For $f(z)=z_0^2+z_1^2$ every coordinate has second derivative $2$, so at any point the diagonal is [2.0, 2.0]. The second difference of $z^2$ is exactly $2h^2$, divided by $h^2$.

## Explanation

Each coordinate is perturbed separately and the function value at the point is computed once and reused. Dividing by $h^2$ amplifies rounding error, so the answers are only accurate to a few decimals and tests use a loose tolerance.
