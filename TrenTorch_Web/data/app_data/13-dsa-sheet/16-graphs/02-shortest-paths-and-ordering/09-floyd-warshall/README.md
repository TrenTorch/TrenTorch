---
name: sheet-floyd-warshall
title: 'Floyd-Warshall: All Pairs'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
---

## Statement

A directed graph has `n` nodes and weighted `edges` `[a, b, w]` with `w >= 0`. Return an `n x n` matrix where entry `[i][j]` is the **shortest distance from `i` to `j`**, with `-1` if `j` cannot be reached from `i`. The distance from a node to itself is `0`.

For `n = 3` and `edges = [[0, 1, 4], [1, 2, 1], [0, 2, 7]]` the answer is `[[0, 4, 5], [-1, 0, 1], [-1, -1, 0]]`.

### Examples

**Example 1**

Input:

```python
all_pairs_shortest(3, [[0, 1, 4], [1, 2, 1], [0, 2, 7]])
```

Output:

```text
[[0, 4, 5], [-1, 0, 1], [-1, -1, 0]]
```

**Example 2**

Input:

```python
all_pairs_shortest(2, [])
```

Output:

```text
[[0, -1], [-1, 0]]
```

### Constraints

- `1 <= n <= 120`
- `0 <= len(edges) <= 3000`
- `0 <= w <= 10**4`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

When you need the distances between **all pairs**, running Dijkstra from every node costs `n` runs. **Floyd–Warshall** does it with three nested loops and a beautiful idea of **dynamic programming**: let `dist[i][j]` be the best distance using only the nodes `0..k-1` as intermediate stops. Allowing one more intermediate node `k` gives

`dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.

The loop over `k` must be the **outermost** one. After all `n` values of `k`, every path is allowed. `O(n³)`, which is fine for `n` up to a few hundred and very short to write.

## Explanation

The matrix starts with the edge weights (and 0 on the diagonal); `inf` marks missing edges. After the triple loop, `inf` entries become `-1`.
