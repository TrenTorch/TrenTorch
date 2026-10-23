---
name: sheet-shortest-path-in-binary-matrix
title: 'Shortest Path in a Binary Matrix'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
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

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

In a graph where every move costs the same (here, one step), the **shortest path** is found by **BFS**: it explores the nodes in order of distance from the start, so the first time it reaches the target is by a shortest path. Store the distance in the queue (or in a table) and mark cells as visited **when you add them to the queue**, not when you take them out (otherwise a cell could be queued many times).

Check the corner cases: the start or the end is blocked, or the grid has a single open cell (answer `1`). `O(rows * cols)`.

## Explanation

Each queue entry is `(row, col, steps)`. The first time the bottom-right cell is dequeued, `steps` is the answer.
