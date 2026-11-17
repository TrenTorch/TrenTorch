---
name: sheet-transpose-matrix
title: 'Transpose a Matrix'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: slicing-and-zip
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

## Explanation

`[list(col) for col in zip(*matrix)]` builds each new row from one column. For `[]`, `zip()` yields nothing, and for `[[], []]` every row is empty, so `zip` stops immediately. Both give `[]`.

### Complexity

- Time: O(r * c). Every one of the `r * c` cells is copied once.
- Space: O(r * c). The transposed matrix is a new list of lists.
