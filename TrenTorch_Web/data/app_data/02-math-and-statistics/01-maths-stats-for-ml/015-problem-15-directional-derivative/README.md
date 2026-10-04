---
name: problem-15-directional-derivative
title: "Directional Derivative"
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Beginner
kind: problemset
relatedModule: "part-math|Calculus"
topic: "calculus"
hint: "normalize the direction before taking the dot product with the gradient"
tools: [NumPy]
---

# Directional Derivative

## Statement

Implement `solve(grad, direction)`. Compute the directional derivative from gradient vector grad along the unit direction of direction.

## Theory

The directional derivative is the dot product of the gradient with a normalized direction vector.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.

## Examples

**Example 1**

Input:
```python
solve([2.0, 3.0], [1.0, -1.0])
```

Output:
```text
-0.7071067811865475
```

**Example 2**

Input:
```python
solve([2.0, 3.0], [1.0, 0.0])
```

Output:
```text
2.0
```
