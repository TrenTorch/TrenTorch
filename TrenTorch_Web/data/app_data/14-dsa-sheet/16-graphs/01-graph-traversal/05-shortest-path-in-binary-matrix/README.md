---
name: sheet-shortest-path-in-binary-matrix
title: 'Shortest Path in a Binary Matrix'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
theory: bfs-on-a-grid-shortest-path-in-a-binary-matrix
---

## Statement

`grid` has `0` (open) and `1` (blocked). Find the **shortest path from the top-left cell to the bottom-right cell** that only uses open cells and moves in **8 directions** (also diagonally). Return the **number of cells on the path** (both ends included), or `-1` if there is no path.

For `[[0, 0, 0], [1, 1, 0], [1, 1, 0]]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
shortest_path_binary_matrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]])
```

Output:

```text
4
```

**Example 2**

Input:

```python
shortest_path_binary_matrix([[1, 0], [0, 0]])
```

Output:

```text
-1
```

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0` or `1`.
- The empty grid has no path.

## Explanation

Each queue entry is `(row, col, steps)`. The first time the bottom-right cell is dequeued, `steps` is the answer.

### Complexity

- Time: O(r * c). A breadth-first search; each cell enters the queue at most once and has 8 neighbours.
- Space: O(r * c). The visited grid and the queue.
