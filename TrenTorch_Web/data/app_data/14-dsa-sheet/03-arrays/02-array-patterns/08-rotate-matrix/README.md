---
name: sheet-rotate-matrix
title: 'Rotate a Matrix'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
theory: rotating-by-combining-moves
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

## Explanation

`matrix[::-1]` lists the rows from bottom to top. `zip(*...)` then reads columns of that reversed matrix: the first output row is the first column read from the bottom up, which is the first column of the original rotated into a row. Each tuple is turned into a list. An empty matrix, or one with empty rows, rotates to `[]`.

### Complexity

- Time: O(r * c). Every cell is copied once.
- Space: O(r * c). The rotated matrix is a new list of lists.
