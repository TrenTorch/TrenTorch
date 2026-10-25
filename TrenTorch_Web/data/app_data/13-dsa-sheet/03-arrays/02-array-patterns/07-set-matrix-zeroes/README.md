---
name: sheet-set-matrix-zeroes
title: 'Set Matrix Zeroes'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
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

**Explanation:** The input matrix has a zero at row index 1 and column index 1, so row 1 and column 1 are completely filled with zeros while other cells remain unchanged.

**Example 2**

Input:

```python
set_matrix_zeroes([[0, 1], [2, 3]])
```

Output:

```text
[[0, 0], [0, 3]]
```

**Explanation:** The zero at row index 0 and column index 0 clears both the first row and the first column, leaving only the bottom-right cell as 3.

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 250000`
- All rows have the same length.
- `-10**9 <= matrix[i][j] <= 10**9`

## Theory

A trap: if you clear a row as soon as you find a zero, the new zeros you write would trigger more clearing and wipe the whole matrix. So work in **two phases**: first _record_ which rows and columns contain a zero, then _write_ the result.

Recording takes one pass over the cells and stores two small sets, so memory is `O(rows + cols)`. Writing is another pass: a cell becomes `0` if its row or its column is in the recorded sets, and keeps its value otherwise. Total time is `O(rows * cols)`, which is the size of the input.

Interviewers often ask for `O(1)` extra space, by using the first row and first column of the matrix as the marker storage. The two-phase version is the clearest to learn first.

## Explanation

`rows` is the set of row indexes that contain a `0`; `cols` is the set of column indexes that contain one. The result is built from the original matrix: `0` where `i in rows or j in cols`, the original value elsewhere.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                     | Variables                                      |
| ------------------------------------------------------------------- | ---------------------------------------------- |
| `rows = {i for i, row in enumerate(matrix) if 0 in row}`            | `rows = {1}`                                   |
| `cols = {j for row in matrix for j, x in enumerate(row) if x == 0}` | `cols = {1}`                                   |
| `return`                                                            | `returned = [[1, 0, 3], [0, 0, 0], [7, 0, 9]]` |
