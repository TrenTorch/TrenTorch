---
name: sheet-dijkstra-shortest-paths
title: 'Dijkstra: Shortest Distances'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
---

## Statement

A **directed** graph has `n` nodes and weighted `edges` `[a, b, w]` (an arrow from `a` to `b` of length `w >= 0`). Return a list with the **shortest distance from `source` to every node**, using `-1` for nodes that cannot be reached.

For `n = 3`, `edges = [[0, 1, 4], [0, 2, 1], [2, 1, 2]]` and `source = 0` the answer is `[0, 3, 1]`.

The starter code finds the closest unfinished node by scanning all nodes every time. It is correct but too slow for a large graph.

### Examples

**Example 1**

Input:

```python
shortest_distances(3, [[0, 1, 4], [0, 2, 1], [2, 1, 2]], 0)
```

Output:

```text
[0, 3, 1]
```

**Example 2**

Input:

```python
shortest_distances(3, [[1, 2, 5]], 0)
```

Output:

```text
[0, -1, -1]
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- `0 <= w <= 10**4`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

BFS finds shortest paths only when all edges cost the same. With **non-negative weights**, use **Dijkstra's algorithm**: keep a tentative distance for every node. Repeatedly take the unfinished node with the **smallest** tentative distance. Its distance is now final (any other route would have to go through a node at least as far), so relax its outgoing edges: if `dist[u] + w < dist[v]`, update `dist[v]`.

A **min-heap** of `(distance, node)` finds the smallest quickly; when you pop an entry that is out of date (its distance is larger than the best known), skip it. Cost `O((n + m) log n)`. Dijkstra is **wrong with negative weights**; use Bellman–Ford for those.

## Explanation

Pushing a new `(distance, node)` pair on every improvement leaves old pairs in the heap; `if d > dist[u]: continue` skips them.
