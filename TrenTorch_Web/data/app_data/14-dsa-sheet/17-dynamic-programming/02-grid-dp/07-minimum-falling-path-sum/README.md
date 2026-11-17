---
name: sheet-minimum-falling-path-sum
title: 'Minimum Falling Path Sum'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
theory: triangles-and-falling-paths
---

## Statement

`matrix` is a grid of numbers. A **falling path** starts at any cell of the first row and moves down one row at a time, to the cell directly below or diagonally below left or right. Return the **smallest sum** of a falling path. An empty matrix gives `0`.

For `[[2, 1, 3], [6, 5, 4], [7, 8, 9]]` the answer is `13` (`1 + 5 + 7`).

### Examples

**Example 1**

Input:

```python
min_falling_path_sum([[2, 1, 3], [6, 5, 4], [7, 8, 9]])
```

Output:

```text
13
```

**Example 2**

Input:

```python
min_falling_path_sum([[-19, 57], [-40, -5]])
```

Output:

```text
-59
```

### Constraints

- `0 <= rows, cols <= 500`
- `-100 <= value <= 100`

## Explanation

`prev` is the previous row of totals. The slice `prev[max(0, c - 1) : c + 2]` takes only the neighbours that exist.

### Complexity

- Time: O(r * c). Every cell is computed once from at most three cells above it.
- Space: O(c). One row of the table.
