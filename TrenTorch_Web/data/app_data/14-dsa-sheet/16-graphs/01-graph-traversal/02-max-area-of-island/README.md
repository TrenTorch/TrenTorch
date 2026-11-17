---
name: sheet-max-area-of-island
title: 'Largest Island'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
theory: flood-fill-and-counting-islands
---

## Statement

`grid` holds `1` (land) and `0` (water). Return the **number of cells in the largest island** (land cells connected up, down, left or right), or `0` if there is no land.

For `[[1, 1, 0], [0, 1, 0], [0, 0, 1]]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
max_island_area([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_island_area([[0]])
```

Output:

```text
0
```

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0` or `1`.

## Explanation

`size` counts the cells taken from the stack during one flood; `best` keeps the largest.

### Complexity

- Time: O(r * c). Every cell is pushed and popped at most once and each has 4 neighbours.
- Space: O(r * c). The visited grid and the stack.
