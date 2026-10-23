---
name: sheet-rotate-matrix
title: 'Rotate a Matrix'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
---

## Statement

Return the matrix **rotated 90 degrees clockwise**. A matrix with `m` rows and `n` columns becomes a matrix with `n` rows and `m` columns. The first row of the input becomes the last column of the output.

### Examples

**Example 1**

Input:

```python
rotate_matrix([[1, 2, 3], [4, 5, 6]])
```

Output:

```text
[[4, 1], [5, 2], [6, 3]]
```

**Example 2**

Input:

```python
rotate_matrix([[1]])
```

Output:

```text
[[1]]
```

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 250000`
- All rows have the same length.

## Theory

Think about where each cell goes. The cell at row `i`, column `j` of an `m x n` matrix moves to row `j`, column `m - 1 - i` of the result.

There is a very short way to say this in Python. Reversing the order of the rows (`matrix[::-1]`) and then **transposing** (swapping rows and columns with `zip(*...)`) rotates the matrix clockwise. A transpose alone mirrors it along the diagonal; flipping the rows first turns the mirror into a rotation.

Rotating in place without a second matrix works for square matrices, by rotating cells in groups of four layer by layer.

## Explanation

`matrix[::-1]` lists the rows from bottom to top. `zip(*...)` then reads columns of that reversed matrix: the first output row is the first column read from the bottom up, which is the first column of the original rotated into a row. Each tuple is turned into a list. An empty matrix, or one with empty rows, rotates to `[]`.
