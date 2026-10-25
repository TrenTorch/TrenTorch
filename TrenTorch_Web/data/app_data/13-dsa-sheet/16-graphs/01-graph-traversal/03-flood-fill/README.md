---
name: sheet-flood-fill
title: 'Flood Fill'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
---

## Statement

`image` is a grid of colours. Starting at the cell `(sr, sc)`, **recolour** it and every cell connected to it (up, down, left or right) that has the **same original colour** to `color`. Return the new image.

For `image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]`, `(sr, sc) = (1, 1)` and `color = 2` the answer is `[[2, 2, 2], [2, 2, 0], [2, 0, 1]]`.

### Examples

**Example 1**

Input:

```python
flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2)
```

Output:

```text
[[2, 2, 2], [2, 2, 0], [2, 0, 1]]
```

**Explanation:** The starting pixel is color 1; all connected pixels with color 1 are set to 2, producing the displayed matrix.

**Example 2**

Input:

```python
flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0)
```

Output:

```text
[[0, 0, 0], [0, 0, 0]]
```

**Explanation:** Starting pixel is already color 0 and desired color is also 0, so no changes are made.

### Constraints

- `1 <= rows, cols <= 300`
- `0 <= image[i][j], color < 65536`
- `(sr, sc)` is a cell of the image.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

This is the paint bucket tool. Remember the **original colour** of the start cell, then flood: visit neighbours that still have that colour and recolour them. Recolouring is also the visited mark. One trap: if the new colour **equals** the old colour, nothing would ever change and a naive flood would loop forever (every cell stays "unvisited"). Return the image at once in that case. `O(rows * cols)`.

## Explanation

The early return handles `color == old`. Otherwise each recoloured cell no longer has the old colour, so it is never pushed again.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                   | Variables                                                                                                 |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `old = image[sr][sc]`                                             | `old = 1`                                                                                                 |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `image = [[1, 1, 1], [1, 2, 0], [1, 0, 1]], rows = 3, cols = 3, stack = [], x = 1, y = 1, nx = 0, ny = 1` |
| `x, y = stack.pop()`                                              | `image = [[1, 2, 1], [2, 2, 0], [1, 0, 1]], stack = [(0, 1)], y = 0, nx = 1, ny = 0`                      |
| `stack.append((nx, ny))`                                          | `image = [[2, 2, 1], [2, 2, 0], [2, 0, 1]], stack = [(0, 1), (2, 0), (0, 0)], nx = 0`                     |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `stack = [(0, 1), (2, 0)], x = 0, ny = 1`                                                                 |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `stack = [(0, 1)], x = 2, nx = 2, ny = -1`                                                                |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `image = [[2, 2, 2], [2, 2, 0], [2, 0, 1]], stack = [(0, 2)], x = 0, y = 1, nx = 0, ny = 0`               |
| `return`                                                          | `returned = [[2, 2, 2], [2, 2, 0], [2, 0, 1]]`                                                            |
