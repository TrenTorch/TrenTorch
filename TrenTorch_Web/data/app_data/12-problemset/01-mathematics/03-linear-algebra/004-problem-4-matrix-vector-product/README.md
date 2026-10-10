---
name: problem-4-matrix-vector-product
title: 'Matrix-Vector Product'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'each output entry is one row dotted with the vector'
tools: [NumPy]
---

## Statement

Multiply an $m\times n$ matrix by a length-$n$ vector by computing each output entry as the dot product of one matrix row with the vector.

Implement `solve(A, x)`.

**Returns.** Return a NumPy array of length $m$.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 1.0])
```

Output:

```text
[3.0, 7.0]
```

**Example 2**

Input:

```python
solve([[0.0, 1.0, 0.0]], [5.0, 6.0, 7.0])
```

Output:

```text
[6.0]
```

## Theory

### The simple version

Entry $i$ of the result is row $i$ of the matrix dotted with the vector. A matrix-vector product is just many dot products stacked together.

### The formula

$$y_i=\sum_{j=1}^{n}A_{ij}\,x_j$$

### Why it matters

- Matrix-vector products are the basic step of every linear layer and every linear system.
- Seeing each output as one dot product makes the cost ($m\times n$ multiplications) and the shapes obvious.

### How it works

1. Check that the vector length equals the number of columns of the matrix.
2. For each row of the matrix, compute its dot product with the vector.
3. Collect those $m$ numbers into the result.

### Worked example

For the matrix with rows $(1,2)$ and $(3,4)$ and the vector $(1,1)$: row one gives $1\cdot1+2\cdot1=3$ and row two gives $3\cdot1+4\cdot1=7$, so the result is [3.0, 7.0].

## Explanation

The reference loops over the rows and takes one dot product per row, which mirrors the definition directly. Library routines compute the same numbers with optimized kernels.
