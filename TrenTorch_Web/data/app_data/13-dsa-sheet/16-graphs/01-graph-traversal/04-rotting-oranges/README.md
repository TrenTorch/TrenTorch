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

**Explanation:** This grid contains multiple fresh oranges that become rotten from nearby rotten. After 4 rounds all oranges are rotten.

**Example 2**

Input:

```python
oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]])
```

Output:

```text
-1
```

**Explanation:** In this grid one fresh orange is surrounded by empty cells so it never contacts a rotten orange. When no fresh orange can spread the rot, the answer is -1.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                   | Variables                                                                                                                       |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `rows = len(grid)`                                                | `rows = 3`                                                                                                                      |
| `for r in range(rows):`                                           | `cols = 3, g = [[2, 1, 1], [1, 1, 0], [0, 1, 1]], queue = deque([(0, 0)]), fresh = 2, r = 1, c = 2`                             |
| `fresh += 1`                                                      | `fresh = 6, r = 2`                                                                                                              |
| `fresh -= 1`                                                      | `g = [[2, 2, 1], [2, 1, 0], [0, 1, 1]], queue = deque([(1, 0)]), fresh = 4, minutes = 1, _ = 0, x = 0, y = 0, nx = 0, ny = 1`   |
| `for _ in range(len(queue)):`                                     | `g = [[2, 2, 1], [2, 2, 0], [0, 1, 1]], queue = deque([(0, 1), (1, 1)]), fresh = 3, minutes = 2, _ = 1, x = 1, nx = 1, ny = -1` |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `g = [[2, 2, 2], [2, 2, 0], [0, 1, 1]], queue = deque([(0, 2)]), fresh = 2, minutes = 3, _ = 0, y = 1, nx = 2, ny = 1`          |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `g = [[2, 2, 2], [2, 2, 0], [0, 2, 1]], queue = deque([(2, 1)]), fresh = 1, _ = 1, x = 0, y = 2, nx = 0, ny = 3`                |
| `return`                                                          | `returned = 4`                                                                                                                  |
