---
name: problem-1-compute-a-stable-l2-norm
title: 'Compute a Stable L2 Norm'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'scale the vector by its largest absolute value before squaring'
tools: [NumPy]
---

## Statement

Implement `solve(x)`. Compute the Euclidean (L2) norm of a non-empty real vector. Scaling by the largest magnitude avoids squaring unnecessarily large or small values.

### Examples

**Example 1**

Input:

```python
solve([3.0, 4.0])
```

Output:

```text
5.0
```

**Example 2**

Input:

```python
solve([0.0, 0.0])
```

Output:

```text
0.0
```

## Theory

The norm is sqrt(sum(x_i^2)). Factoring out max(abs(x)) preserves the result while improving numerical stability.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
