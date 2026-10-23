---
name: sheet-max-area-of-island
title: 'Largest Island'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
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

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

It is the previous question with one change: instead of only counting the floods, **count the cells each flood visits** and keep the maximum. A DFS or BFS returns the number of cells it marked. `O(rows * cols)`.

## Explanation

`size` counts the cells taken from the stack during one flood; `best` keeps the largest.
