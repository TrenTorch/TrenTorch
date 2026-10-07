---
name: problem-9-power-iteration
title: 'Power Iteration'
tags: [problemset, maths-stats-for-ml, eigenvalues]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'eigenvalues'
hint: 'multiply by A, then divide by the norm, repeat'
tools: [NumPy]
---

## Statement

Estimate the dominant eigenvector of a symmetric matrix with power iteration: repeatedly multiply a vector by the matrix and renormalize it.

Implement `solve(A, steps=100)`.

**Returns.** Return a unit-length NumPy vector after `steps` iterations (default 100), starting from the all-ones vector. If an iterate becomes the zero vector (for example for the zero matrix) it is returned as is. The overall sign depends on the starting vector.

### Examples

**Example 1**

Input:

```python
solve([[2.0, 0.0], [0.0, 1.0]])
```

Output:

```text
[1.0, 0.0]
```

**Example 2**

Input:

```python
solve([[2.0, 1.0], [1.0, 2.0]])
```

Output:

```text
[0.707107, 0.707107]
```

## Theory

### The simple version

Multiplying a vector by a matrix stretches it most along the eigenvector with the largest eigenvalue (in absolute value). Do that many times and the vector lines up with that eigenvector.

### The formula

$$v_{t+1}=\frac{A v_t}{\|A v_t\|_2}$$

The error shrinks roughly like $|\lambda_2/\lambda_1|^t$, so a larger gap between the top two eigenvalues means faster convergence.

## Explanation

Renormalizing after every multiplication stops the numbers from growing without bound. The method only converges when the start vector has some component along the dominant eigenvector; the all-ones start works for the usual test matrices. A zero iterate is returned immediately because it cannot be normalized.
