---
name: problem-5-matrix-transpose
title: 'Matrix Transpose'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'swap the two axes'
tools: [NumPy]
---

## Statement

Return the transpose of a rectangular matrix, swapping its rows and columns.

Implement `solve(A)`.

**Returns.** Return a NumPy array of shape $(n, m)$ for an $m\times n$ input.

### Examples

**Example 1**

Input:

```python
solve([[1, 2, 3], [4, 5, 6]])
```

Output:

```text
[[1, 4], [2, 5], [3, 6]]
```

**Example 2**

Input:

```python
solve([[7]])
```

Output:

```text
[[7]]
```

## Theory

### The simple version

The transpose flips a matrix over its main diagonal, so the entry in row $i$, column $j$ moves to row $j$, column $i$.

### The formula

$$(A^\top)_{ij}=A_{ji}$$

### Why it matters

- Transposing swaps what rows and columns mean, which is needed to line shapes up for matrix products ($X^\top X$, $W^\top$).
- It is a pure re-indexing, so it should never change a value.

### How it works

1. For an $m\times n$ matrix create an $n\times m$ result.
2. Put the entry from row $i$, column $j$ into row $j$, column $i$.

### Worked example

The $2\times3$ matrix with rows $(1,2,3)$ and $(4,5,6)$ becomes a $3\times2$ matrix. Its first column $(1,4)$ becomes the first row, giving [[1, 4], [2, 5], [3, 6]].

## Explanation

NumPy's `.T` swaps the two axes. It returns a view on the same data, so no values are copied.
