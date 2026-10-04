---
name: problem-4-matrix-vector-product
title: "Matrix-Vector Product"
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: "part-math|Linear Algebra"
topic: "linear algebra"
hint: "accumulate one dot product per output row"
tools: [NumPy]
---

# Matrix-Vector Product

## Statement

Implement `solve(A, x)`. Multiply an m-by-n matrix by a length-n vector and return the length-m result.

## Theory

Each output coordinate is the dot product of one matrix row with the input vector.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.

## Examples

**Example 1**

Input:
```python
solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 2.0])
```

Output:
```text
[5.0, 11.0]
```

**Example 2**

Input:
```python
solve([[2.0, -1.0]], [3.0, 4.0])
```

Output:
```text
[2.0]
```
