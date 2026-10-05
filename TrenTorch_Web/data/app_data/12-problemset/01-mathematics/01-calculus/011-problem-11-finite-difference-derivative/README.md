---
name: problem-11-finite-difference-derivative
title: 'Finite Difference Derivative'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'evaluate f at x+h and x-h'
tools: [NumPy]
---

## Statement

Implement `solve(f, x, h=1e-5)`. Approximate the derivative of a scalar-valued function at scalar x using step size h (default 1e-5).

### Examples

**Example 1**

Input:

```python
solve(lambda z: z*z, 3.0)
```

Output:

```text
6.000000000039306
```

**Example 2**

Input:

```python
solve(np.sin, 0.0)
```

Output:

```text
0.9999999999833332
```

## Theory

The centered finite-difference quotient [f(x+h)-f(x-h)]/(2h) has second-order truncation error.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
