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

**Explanation:** Starting at (0,0) and moving only through adjacent cells where each step differs by at most 2 leads to the destination. Any path must cross a height difference of at least 2, so the minimal effort is 2.

**Example 2**

Input:

```python
minimum_effort_path([[1, 2, 3], [3, 8, 4], [5, 3, 5]])
```

Output:

```text
1
```

**Explanation:** A route from (0,0) to (2,2) uses only steps with differences 1 or less, so its effort is 1. No path can avoid a difference of at least 1, making 1 the minimum.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                   | Variables                                                                                                                               |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `rows, cols = len(heights), len(heights[0])`                      | `rows = 3, cols = 3`                                                                                                                    |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `inf = inf, effort = [[0, inf, inf], [2, inf, inf], [inf, inf, inf]], heap = [(2, 1, 0)], e = 0, x = 0, y = 0, nx = -1, ny = 0, ne = 2` |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `effort = [[0, 1, inf], [2, 6, inf], [inf, inf, inf]], heap = [(2, 1, 0), (6, 1, 1)], e = 1, y = 1, ny = 1, ne = 6`                     |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `effort = [[0, 1, 1], [2, 6, 1], [inf, inf, inf]], heap = [(1, 1, 2), (6, 1, 1), (2, 1, 0)], y = 2, ny = 2, ne = 1`                     |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `effort = [[0, 1, 1], [2, 6, 1], [inf, inf, 3]], heap = [(2, 1, 0), (6, 1, 1), (3, 2, 2)], x = 1, nx = 1, ny = 1`                       |
| `effort[nx][ny] = ne`                                             | `effort = [[0, 1, 1], [2, 5, 1], [2, inf, 3]], heap = [(2, 2, 0), (6, 1, 1), (3, 2, 2)], e = 2, y = 0, ne = 5`                          |
| `e, x, y = heapq.heappop(heap)`                                   | `effort = [[0, 1, 1], [2, 5, 1], [2, 2, 3]], heap = [(3, 2, 2), (5, 1, 1), (6, 1, 1)], x = 2, y = 1, nx = 2, ny = -1, ne = 2`           |
| `return`                                                          | `returned = 2`                                                                                                                          |
