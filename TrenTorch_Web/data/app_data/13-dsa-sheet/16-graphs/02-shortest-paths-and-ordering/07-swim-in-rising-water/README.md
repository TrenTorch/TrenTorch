---
name: sheet-swim-in-rising-water
title: 'Swim in Rising Water'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
---

## Statement

`grid[r][c]` is the height of a platform. At time `t` the water level is `t`, and you can swim from a cell to a neighbour (up, down, left, right) if **both** have height at most `t`. You start at the top-left at time 0. Return the **least time** at which you can reach the bottom-right cell.

For `[[0, 2], [1, 3]]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
swim_in_water([[0, 2], [1, 3]])
```

Output:

```text
3
```

**Explanation:** The goal cell has height 3, so the water has to be at least 3 before you can stand on it. At time 3 both routes are open, so 3 is the answer.

**Example 2**

Input:

```python
swim_in_water([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]])
```

Output:

```text
16
```

**Explanation:** The only way down from the top row is through the 5 on the right edge, which leads to the 16 below it. From there the path runs left along the middle row and then along the bottom row to the goal. The highest cell on that path is 16, so the water must reach 16.

### Constraints

- `1 <= rows, cols <= 100`
- All heights are different integers from `0` to `rows * cols - 1`.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

The time needed for a path is the **highest platform on it** (you must wait for the water to reach the highest one). So you want the path whose maximum cell height is smallest: a **minimax path**, solved like the previous question with Dijkstra: expand the cell with the smallest "time so far" first, where the time to enter a neighbour is `max(time so far, neighbour's height)`.

Another view is a **union-find**: add the cells in order of height and stop when the top-left and the bottom-right become connected.

## Explanation

The heap starts with the top-left cell at time `grid[0][0]`. The first pop of the bottom-right cell gives the answer.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                   | Variables                                                                             |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `n, m = len(grid), len(grid[0])`                                  | `n = 2, m = 2`                                                                        |
| `t, x, y = heapq.heappop(heap)`                                   | `seen = [[True, False], [False, False]], heap = [], t = 0, x = 0, y = 0`              |
| `heapq.heappush(heap, (max(t, grid[nx][ny]), nx, ny))`            | `seen = [[True, False], [True, False]], heap = [(1, 1, 0)], nx = 1, ny = 0`           |
| `heapq.heappush(heap, (max(t, grid[nx][ny]), nx, ny))`            | `seen = [[True, True], [True, False]], heap = [(1, 1, 0), (2, 0, 1)], nx = 0, ny = 1` |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `heap = [(2, 0, 1)], t = 1, x = 1, ny = 0`                                            |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `seen = [[True, True], [True, True]], heap = [(2, 0, 1), (3, 1, 1)], nx = 1, ny = -1` |
| `for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):` | `heap = [(3, 1, 1)], t = 2, x = 0, y = 1, nx = -1, ny = 1`                            |
| `return`                                                          | `returned = 3`                                                                        |

### Complexity

- Time: O(n * m log(n * m)) n is rows, m is columns.
- Extra space: O(n * m) seen array and heap.
- The brute force takes O((n * m) squared) testing all time steps.
