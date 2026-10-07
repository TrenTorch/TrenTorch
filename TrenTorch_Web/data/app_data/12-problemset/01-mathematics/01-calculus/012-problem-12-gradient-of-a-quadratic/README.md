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

## Explanation

The reference symmetrizes $A$ first, so non-symmetric inputs still give the correct gradient. The second example uses an asymmetric $A$, where $\tfrac12(A+A^\top)x$ differs from $Ax$.
