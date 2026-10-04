---
name: problem-12-gradient-of-a-quadratic
title: "Gradient of a Quadratic"
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Advanced
kind: problemset
relatedModule: "part-math|Calculus"
topic: "calculus"
hint: "use (A+Aᵀ)x/2 + b"
tools: [NumPy]
---

# Gradient of a Quadratic

## Statement

Implement `solve(A, x, b)`. Return the gradient with respect to x of 0.5*xᵀAx + bᵀx.

## Theory

The gradient is (A+Aᵀ)x/2 + b; only the symmetric part of A contributes to the quadratic form.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.

## Examples

**Example 1**

Input:
```python
solve([[2.0, 0.0], [0.0, 4.0]], [1.0, 2.0], [1.0, -1.0])
```

Output:
```text
[3.0, 7.0]
```

**Example 2**

Input:
```python
solve([[0.0, 0.0], [0.0, 0.0]], [3.0, 4.0], [2.0, -2.0])
```

Output:
```text
[2.0, -2.0]
```
