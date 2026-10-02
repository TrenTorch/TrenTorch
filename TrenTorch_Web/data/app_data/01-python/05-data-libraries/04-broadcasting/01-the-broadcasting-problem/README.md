---
name: numpy-the-broadcasting-problem
title: The Problem Broadcasting Solves
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement a function that applies an operation between arrays of different shapes, first by writing it as an explicit loop, then by letting NumPy handle it automatically.

## Theory

Applying a single row to every row of a larger array, without broadcasting, requires an explicit loop:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])     # shape (2, 3)
addend = np.array([10, 20, 30])                 # shape (3,)

result = np.empty_like(matrix)
for i in range(matrix.shape[0]):
    result[i] = matrix[i] + addend
```

This reintroduces a Python-level loop with per-iteration overhead, exactly the problem Module 6 covers in full.

**Broadcasting is NumPy automatically figuring out how to apply an operation between two differently-shaped arrays**, without an explicit loop, by virtually "stretching" the smaller array across the larger one:

```python
result = matrix + addend     # broadcasting happens automatically
```

`addend`'s shape `(3,)` is compatible with `matrix`'s `(2, 3)` — it's treated as if repeated once per row, without NumPy actually materializing a repeated copy in memory. This is both faster and more memory-efficient than manually building a repeated-row array.

## Explanation

`add_row_with_loop` iterates `for i in range(matrix.shape[0])`, writing `matrix[i] + row` into `result[i]`. `add_row_with_broadcasting` is a single expression, `matrix + row` — NumPy handles the per-row application internally, with no explicit iteration.
