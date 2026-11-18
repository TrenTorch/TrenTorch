---
name: sheet-spiral-order
title: 'Spiral Order'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
theory: walking-around-the-edge
---

## Statement

Return all the values of the matrix in **clockwise spiral order**: along the top row left to right, down the right column, along the bottom row right to left, up the left column, then repeat on the inner part until every value is used.

### Examples

**Example 1**

Input:

```python
spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
```

Output:

```text
[1, 2, 3, 6, 9, 8, 7, 4, 5]
```

**Example 2**

Input:

```python
spiral_order([[1, 2, 3, 4]])
```

Output:

```text
[1, 2, 3, 4]
```

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 250000`
- All rows have the same length.

## Explanation

The loop `while top <= bottom and left <= right` handles one layer. After walking the top row and the right column, the bottom row is walked only if `top <= bottom` still holds, and the left column only if `left <= right` still holds. These checks stop a single row or column from being walked twice.

### Complexity

- Time: O(r * c). Every cell is appended exactly once while the four borders shrink.
- Space: O(r * c). The result list holds all cells; nothing else is allocated.
