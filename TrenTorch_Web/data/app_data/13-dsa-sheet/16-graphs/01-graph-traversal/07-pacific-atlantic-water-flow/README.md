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

**Example 2**

Input:

```python
pacific_atlantic([[1]])
```

Output:

```text
[[0, 0]]
```

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
