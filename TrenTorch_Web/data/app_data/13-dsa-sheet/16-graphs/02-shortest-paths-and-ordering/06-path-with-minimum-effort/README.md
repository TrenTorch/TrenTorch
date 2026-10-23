---
name: sheet-path-with-minimum-effort
title: 'Path With Minimum Effort'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
---

## Statement

`heights[r][c]` is the height of a cell. You walk from the top-left to the bottom-right cell, moving up, down, left or right. The **effort** of a path is the **largest absolute difference in height between two neighbouring cells on the path**. Return the **smallest effort** over all paths.

For `[[1, 2, 2], [3, 8, 2], [5, 3, 5]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
minimum_effort_path([[1, 2, 2], [3, 8, 2], [5, 3, 5]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
minimum_effort_path([[1, 2, 3], [3, 8, 4], [5, 3, 5]])
```

Output:

```text
1
```

### Constraints

- `1 <= rows, cols <= 100`
- `1 <= heights[r][c] <= 10**6`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

The cost of a path is a **maximum** of edge costs, not a sum, but Dijkstra's idea still works: always expand the cell with the smallest effort so far. The effort of reaching a neighbour through a cell is `max(effort of the cell, |height difference|)`. The first time the bottom-right cell is popped from the heap, its effort is the minimum.

A heap gives `O(rows·cols·log(rows·cols))`. Another approach: **binary search** the answer `e` and check with a BFS whether the target is reachable using only steps of difference at most `e`.

## Explanation

`effort[r][c]` is the best known maximum difference to reach the cell. The heap pops cells in order of effort, and `max(...)` combines the path so far with the new step.
