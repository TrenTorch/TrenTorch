---
name: sheet-set-matrix-zeroes
title: 'Set Matrix Zeroes'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
theory: row-and-column-flags
---

## Statement

Whenever a cell of the matrix is `0`, set **every cell in its row and its column** to `0`. Return the new matrix. Decide which rows and columns to clear from the **original** matrix, not from cells you have already cleared. Do not change the input.

### Examples

**Example 1**

Input:

```python
set_matrix_zeroes([[1, 2, 3], [4, 0, 6], [7, 8, 9]])
```

Output:

```text
[[1, 0, 3], [0, 0, 0], [7, 0, 9]]
```

**Example 2**

Input:

```python
set_matrix_zeroes([[0, 1], [2, 3]])
```

Output:

```text
[[0, 0], [0, 3]]
```

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 250000`
- All rows have the same length.
- `-10**9 <= matrix[i][j] <= 10**9`

## Explanation

`rows` is the set of row indexes that contain a `0`; `cols` is the set of column indexes that contain one. The result is built from the original matrix: `0` where `i in rows or j in cols`, the original value elsewhere.

### Complexity

- Time: O(r * c). One scan to find the zero rows and columns and one to build the result.
- Space: O(r * c). The result matrix; besides it only the sets of zero rows and columns (`O(r + c)`) are kept.
