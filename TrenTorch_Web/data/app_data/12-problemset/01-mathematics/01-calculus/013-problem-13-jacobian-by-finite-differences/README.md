---
name: problem-13-jacobian-by-finite-differences
title: 'Jacobian by Finite Differences'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'perturb one input at a time and difference the outputs'
tools: [NumPy]
---

## Statement

Estimate the Jacobian of a vector-valued function $f:\mathbb R^n\to\mathbb R^m$ at a point, one column at a time, with centered finite differences.

Implement `solve(f, x, h=1e-5)`.

**Returns.** Return an $m\times n$ NumPy array whose entry $(i, j)$ approximates $\partial f_i/\partial x_j$.

### Examples

**Example 1**

Input:

```python
solve(lambda z: np.array([z[0]**2, z[0]*z[1]]), [1.0, 2.0])
```

Output:

```text
[[2.0, 0.0], [2.0, 1.0]]
```

**Example 2**

Input:

```python
solve(lambda z: np.array([np.sin(z[0])]), [0.0])
```

Output:

```text
[[1.0]]
```

## Theory

### The simple version

The Jacobian collects every first derivative of a vector function into a matrix: row $i$ is the gradient of output $i$. To estimate column $j$, nudge only input $j$ up and down and see how all the outputs respond.

### The formula

$$J_{:,j}\approx\frac{f(x+h\,e_j)-f(x-h\,e_j)}{2h}$$

where $e_j$ is the $j$-th unit vector.

### Why it matters

- The Jacobian says how each output changes with each input; it is what backpropagation multiplies together.
- Comparing it with a numerical Jacobian is the standard way to find bugs in a hand-written backward pass.

### How it works

1. For each input coordinate $j$, nudge $x_j$ up and down by $h$.
2. Evaluate the vector function both times and subtract.
3. Divide by $2h$; the result is column $j$ of the Jacobian.

### Worked example

For $f(z)=(z_0^2,\,z_0z_1)$ at $(1,2)$: nudging $z_0$ changes the outputs by $(2z_0,\,z_1)=(2,2)$; nudging $z_1$ changes them by $(0,\,z_0)=(0,1)$. Those are the two columns, so the Jacobian is [[2.0, 0.0], [2.0, 1.0]].

## Explanation

The reference evaluates the function once to learn the number of outputs $m$, then perturbs each input coordinate in turn. The result is an approximation, so compare it with a tolerance. For a scalar-valued function there is no meaningful vector output, so the function must return an array of length $m$.
