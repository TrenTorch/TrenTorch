---
name: sheet-transpose-matrix
title: 'Transpose a Matrix'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
---

## Statement

A matrix is a list of rows, each row a list of the same length. Return its **transpose**: the matrix whose rows are the columns of the original. The element at row `i`, column `j` moves to row `j`, column `i`.

A matrix with no rows, or with rows that have no columns, transposes to `[]`.

### Examples

**Example 1**

Input:

```python
transpose_matrix([[1, 2, 3], [4, 5, 6]])
```

Output:

```text
[[1, 4], [2, 5], [3, 6]]
```

**Example 2**

Input:

```python
transpose_matrix([[7]])
```

Output:

```text
[[7]]
```

### Constraints

- `0 <= rows * cols <= 250000`
- All rows have the same length.
- Return new lists; do not change the input.

## Theory

`zip(a, b, c)` walks several iterables in step and yields tuples: the first elements together, then the second elements, and so on. If you give `zip` the **rows** of a matrix, it yields the **columns**: that is a transpose.

`zip(*matrix)` unpacks the list of rows into separate arguments, so it works for any number of rows. Each result is a tuple, so wrap it with `list(...)` when lists are needed. List comprehensions like `[[row[j] for row in matrix] for j in range(cols)]` do the same job but are longer and slower.

## Explanation

`[list(col) for col in zip(*matrix)]` builds each new row from one column. For `[]`, `zip()` yields nothing, and for `[[], []]` every row is empty, so `zip` stops immediately. Both give `[]`.
