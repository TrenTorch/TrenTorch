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

**Explanation:** The cells (0,0),(0,1),(1,1) form the largest island of size 3.

**Example 2**

Input:

```python
max_island_area([[0]])
```

Output:

```text
0
```

**Explanation:** No land cells exist, so the largest island size is 0.

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0` or `1`.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

It is the previous question with one change: instead of only counting the floods, **count the cells each flood visits** and keep the maximum. A DFS or BFS returns the number of cells it marked. `O(rows * cols)`.

## Explanation

`size` counts the cells taken from the stack during one flood; `best` keeps the largest.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                   | Variables                                                                                                                 |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `rows = len(grid)`                                                | `rows = 3`                                                                                                                |
| `stack = [(r, c)]`                                                | `cols = 3, seen = [[True, False, False], [False, False, False], [False, Fal..., best = 0, r = 0, c = 0, stack = [(0, 0)]` |
| `seen[nx][ny] = True`                                             | `seen = [[True, True, False], [False, False, False], [False, Fals..., stack = [], size = 1, x = 0, y = 0, nx = 0, ny = 1` |
| `stack.append((nx, ny))`                                          | `seen = [[True, True, False], [False, True, False], [False, False..., stack = [(1, 1)], size = 2, y = 1, nx = 1`          |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `stack = [], size = 3, x = 1, ny = 2`                                                                                     |
| `for c in range(cols):`                                           | `best = 3, r = 1, c = 1, ny = 0`                                                                                          |
| `size = 0`                                                        | `r = 2, c = 2, stack = [(2, 2)], size = 0`                                                                                |
| `return`                                                          | `returned = 3`                                                                                                            |

### Complexity

- Time: O(n), n = rows*cols.
- Extra space: O(n), n = rows*cols.
- The brute force takes O(n^2), n is number of cells.
