---
name: sheet-rotting-oranges
title: 'Rotting Oranges'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
theory: spreading-over-time-rotting-oranges
---

## Statement

`grid` has `0` (empty), `1` (fresh orange) and `2` (rotten orange). Every minute, each fresh orange that is next to a rotten one (up, down, left or right) becomes rotten. Return the **number of minutes** until no fresh orange is left, or `-1` if some fresh orange can never rot. If there is no fresh orange at the start the answer is `0`.

For `[[2, 1, 1], [1, 1, 0], [0, 1, 1]]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]])
```

Output:

```text
4
```

**Example 2**

Input:

```python
oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]])
```

Output:

```text
-1
```

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0`, `1` or `2`.

## Explanation

The `while` loop runs while the queue is non-empty and fresh oranges remain; each pass of the loop is one minute.

### Complexity

- Time: O(r * c). A breadth-first search from all rotten oranges at once; each cell enters the queue at most once.
- Space: O(r * c). The copy of the grid and the queue.
