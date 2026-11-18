---
name: sheet-number-of-islands
title: 'Number of Islands'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
theory: flood-fill-and-counting-islands
---

## Statement

`grid` is a map of `1` (land) and `0` (water). An **island** is a group of land cells connected **up, down, left or right**. Return the **number of islands**.

For `[[1, 1, 0], [0, 1, 0], [0, 0, 1]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
num_islands([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
num_islands([[0, 0], [0, 0]])
```

Output:

```text
0
```

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0` or `1`.

## Explanation

Every cell is entered once. The outer loops look for unvisited land; `stack` is the flood fill of one island.

### Complexity

- Time: O(r * c). Every cell is pushed and popped at most once and each has 4 neighbours.
- Space: O(r * c). The visited grid and the stack.
