---
name: sheet-pacific-atlantic-water-flow
title: 'Pacific Atlantic Water Flow'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
---

## Statement

`heights[r][c]` is the height of a cell. Water flows from a cell to a neighbour (up, down, left, right) that is **at the same height or lower**. The **Pacific** ocean touches the top and left edges, the **Atlantic** touches the bottom and right edges. Return, as `[row, col]` pairs sorted by row and then column, **all cells from which water can reach both oceans**.

For `[[1, 2], [2, 1]]` the answer is `[[0, 1], [1, 0]]`.

### Examples

**Example 1**

Input:

```python
pacific_atlantic([[1, 2], [2, 1]])
```

Output:

```text
[[0, 1], [1, 0]]
```

**Explanation:** Cell (0,1) height 2 flows left to (0,0) height 1 (Pacific) and down to (1,1) height 1 (Atlantic). Cell (1,0) similarly flows up and right. Others cannot reach both oceans.

**Example 2**

Input:

```python
pacific_atlantic([[1]])
```

Output:

```text
[[0, 0]]
```

**Explanation:** The single cell touches top/left (Pacific) and bottom/right (Atlantic) edges, so water reaches both oceans.

### Constraints

- `0 <= rows, cols <= 200`
- `0 <= heights[r][c] <= 10**5`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

Asking, for every cell, "can water from here reach the ocean?" means a search from each cell: far too slow. **Reverse the flow**: start at the cells next to an ocean and move **uphill** (to neighbours that are at least as high). The cells reached from the Pacific edges are those that can flow to the Pacific; likewise for the Atlantic.

Run one flood from all Pacific border cells and one from all Atlantic border cells, then take the **intersection** of the two reached sets. Each flood visits every cell at most once: `O(rows * cols)`.

## Explanation

`flood(starts)` returns the set of cells reachable moving to equal or higher neighbours. The answer is the sorted intersection of the two sets.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                                  | Variables                                                              |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `rows = len(heights)`                                                            | `rows = 2`                                                             |
| `cols = len(heights[0]) if rows else 0`                                          | `cols = 2`                                                             |
| `def flood(starts):`                                                             | `flood = <function pacific_atlantic.<locals>.flood at 0x000001F483...` |
| `pacific = flood([(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)])` | `pacific = {(1, 0), (0, 1), (0, 0)}`                                   |
| `atlantic = flood(`                                                              | `atlantic = {(0, 1), (1, 0), (1, 1)}`                                  |
| `return`                                                                         | `returned = [[0, 1], [1, 0]]`                                          |

### Complexity

- Time: O(m * n). The flood function traverses all m * n cells once, and the intersection set operation is linear in the number of reachable cells. Since the stack grows linearly with the number of reachable cells (bounded by m*n), the total time complexity is O(m * n).
- Extra space: O(m * n). The seen set stores up to m * n cells. The stack also grows linearly with the number of reachable cells, so the total extra memory is O(m * n).
- The brute force takes O((m * n)^2). The outer loop iterates over m * n cells. For each cell, the inner loop performs a DFS-like search that can traverse all m * n cells again if they are connected, leading to a quadratic time complexity.
