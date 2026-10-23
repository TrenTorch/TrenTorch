---
name: sheet-rotting-oranges
title: 'Rotting Oranges'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
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

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

The rot spreads from **many sources at the same time**, one step per minute: exactly a **multi-source BFS**. Put _all_ rotten oranges in the queue at the start (distance 0). Each BFS level is one minute: process the queue level by level, rot the fresh neighbours and push them. The number of levels that rotted something is the time.

At the end, if any fresh orange remains it was unreachable: return `-1`. Counting fresh oranges at the start and decrementing as they rot avoids a final scan. `O(rows * cols)`.

## Explanation

The `while` loop runs while the queue is non-empty and fresh oranges remain; each pass of the loop is one minute.
