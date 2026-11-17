---
name: sheet-count-square-submatrices
title: 'Count Square Submatrices of Ones'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
theory: squares-inside-a-grid
---

## Statement

`matrix` holds `0`s and `1`s. Return the **number of square submatrices** (of any size) that contain only `1`s.

For `[[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]]` the answer is `15`.

### Examples

**Example 1**

Input:

```python
count_squares([[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]])
```

Output:

```text
15
```

**Example 2**

Input:

```python
count_squares([[1, 0, 1], [1, 1, 0], [1, 1, 0]])
```

Output:

```text
7
```

### Constraints

- `0 <= rows, cols <= 500`
- Every cell is `0` or `1`.

## Explanation

The same DP as maximal square, but each cell adds its `side` to the total instead of updating a maximum.

### Complexity

- Time: O(r * c). Every cell is computed once from three neighbours.
- Space: O(c). Two rows of the table.
