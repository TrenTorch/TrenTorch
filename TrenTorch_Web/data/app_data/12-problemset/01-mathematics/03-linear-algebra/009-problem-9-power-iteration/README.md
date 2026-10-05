---
name: problem-9-power-iteration
title: 'Power Iteration'
tags: [problemset, maths-stats-for-ml, eigenvalues]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'eigenvalues'
hint: 'normalize after every matrix-vector multiplication'
tools: [NumPy]
---

## Statement

Implement `solve(A, steps=100)`. Estimate a dominant eigenvector of a symmetric square matrix using power iteration, with a default of 100 iterations.

### Examples

**Example 1**

Input:

```python
solve([[2.0, 0.0], [0.0, 1.0]], steps=20)
```

Output:

```text
[0.9999999999995453, 9.536743164058163e-07]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [0.0, 3.0]], steps=20)
```

Output:

```text
[2.8679719907924424e-10, 1.0]
```

## Theory

Repeated multiplication by A amplifies the component along the dominant eigenvector; normalize after every step to control scale.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
