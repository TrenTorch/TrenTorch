---
name: problem-13-jacobian-by-finite-differences
title: "Jacobian by Finite Differences"
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Beginner
kind: problemset
relatedModule: "part-math|Calculus"
topic: "calculus"
hint: "perturb one input coordinate at a time"
tools: [NumPy]
---

# Jacobian by Finite Differences

## Statement

Implement `solve(f, x, h=1e-5)`. Approximate the Jacobian of a vector-valued function at vector x using centered differences.

## Theory

Each Jacobian column is the derivative of the output with respect to one input coordinate.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.

## Examples

**Example 1**

Input:
```python
solve(lambda z: np.array([z[0]**2, z[0]*z[1]]), [2.0, 3.0])
```

Output:
```text
[[4.000000000026205, 0.0], [3.000000000064062, 2.0000000000131024]]
```

**Example 2**

Input:
```python
solve(lambda z: np.array([z[0]+z[1], z[0]-z[1]]), [1.0, 2.0])
```

Output:
```text
[[1.0000000000065512, 1.0000000000065512], [1.0000000000065512, -1.0000000000065512]]
```
