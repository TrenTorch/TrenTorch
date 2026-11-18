---
name: sheet-unique-paths-with-obstacles
title: 'Unique Paths With Obstacles'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
theory: blocked-cells-and-cheapest-paths
---

## Statement

`grid` has `0` (free) and `1` (blocked). A robot moves **right or down** from the top-left to the bottom-right cell, only through free cells. Return the **number of paths**. Return the answer modulo `10**9 + 7`.

For `[[0, 0, 0], [0, 1, 0], [0, 0, 0]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
unique_paths_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
unique_paths_obstacles([[0, 1], [0, 0]])
```

Output:

```text
1
```

### Constraints

- `0 <= rows, cols <= 500`
- Every cell is `0` or `1`.

## Explanation

A blocked cell resets its entry to zero, which also stops paths from flowing through it to later cells.

### Complexity

- Time: O(r * c). Every cell is computed once from its left and upper neighbours.
- Space: O(c). One row of the table.
