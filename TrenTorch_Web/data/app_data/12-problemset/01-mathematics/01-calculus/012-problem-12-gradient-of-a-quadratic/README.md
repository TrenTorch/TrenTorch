---
name: problem-12-gradient-of-a-quadratic
title: 'Gradient of a Quadratic'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'symmetrize A before multiplying by x'
tools: [NumPy]
---

## Statement

Return the gradient of the quadratic function $f(x)=\tfrac12 x^\top A x+b^\top x$. The matrix $A$ does not have to be symmetric.

Implement `solve(A, x, b)`.

**Returns.** Return a NumPy array of length $n$.

### Examples

**Example 1**

Input:

```python
solve([[2.0, 0.0], [0.0, 2.0]], [1.0, 1.0], [0.0, 0.0])
```

Output:

```text
[2.0, 2.0]
```

**Example 2**

Input:

```python
solve([[0.0, 1.0], [0.0, 0.0]], [1.0, 2.0], [0.0, 0.0])
```

Output:

```text
[1.0, 0.5]
```

## Theory

### The simple version

For a quadratic function the gradient is linear in $x$. Only the symmetric part of $A$ matters, because $x^\top A x$ is unchanged if $A$ is replaced by its symmetrized version.

### The formula

$$\nabla f(x)=\tfrac12\,(A+A^\top)\,x+b$$

When $A$ is symmetric this reduces to the familiar $Ax+b$.

### Why it matters

- Quadratics are the standard test bed for optimisers, and their gradient is the simplest non-trivial one to derive.
- Only the symmetric part of $A$ affects $x^\top Ax$, so the gradient must symmetrise a non-symmetric $A$.

### How it works

1. Symmetrise: $S=\tfrac12(A+A^\top)$.
2. Multiply by the point: $Sx$.
3. Add the linear term $b$.

### Worked example

For $A=2I$, $x=(1,1)$ and $b=(0,0)$: $A$ is already symmetric, $Ax=(2,2)$, and adding $b$ leaves [2.0, 2.0].

## Explanation

The reference symmetrizes $A$ first, so non-symmetric inputs still give the correct gradient. The second example uses an asymmetric $A$, where $\tfrac12(A+A^\top)x$ differs from $Ax$.
