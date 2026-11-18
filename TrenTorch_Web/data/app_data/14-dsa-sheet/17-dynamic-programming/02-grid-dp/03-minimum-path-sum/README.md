---
name: sheet-minimum-path-sum
title: 'Minimum Path Sum'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Beginner
theory: blocked-cells-and-cheapest-paths
---

## Statement

`grid` holds non-negative numbers. Move **right or down** from the top-left to the bottom-right cell. Return the **smallest possible sum** of the numbers on the path (both ends included). An empty grid gives `0`.

For `[[1, 3, 1], [1, 5, 1], [4, 2, 1]]` the answer is `7` (`1 + 3 + 1 + 1 + 1`).

The starter code is a plain recursion. It is correct but too slow for big grids.

### Examples

**Example 1**

Input:

```python
min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
```

Output:

```text
7
```

**Example 2**

Input:

```python
min_path_sum([[1, 2, 3], [4, 5, 6]])
```

Output:

```text
12
```

### Constraints

- `0 <= rows, cols <= 500`
- `0 <= grid[r][c] <= 100`

## Explanation

`row[c]` holds `best(r - 1, c)` before the update and the new `best(r, c)` after; `row[c - 1]` is the left neighbour.

### Complexity

- Time: O(r * c). Every cell is computed once from its left and upper neighbours.
- Space: O(c). One row of the table.
