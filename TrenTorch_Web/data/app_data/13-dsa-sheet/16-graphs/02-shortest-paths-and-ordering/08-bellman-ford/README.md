---
name: sheet-bellman-ford
title: 'Bellman-Ford With Negative Edges'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
---

## Statement

A directed graph has `n` nodes and weighted `edges` `[a, b, w]`, where **`w` can be negative**. Return the list of **shortest distances from `source`**, using `None` for unreachable nodes. If a **negative cycle** (a cycle whose total weight is negative) can be reached from `source`, shortest distances do not exist: return an **empty list**.

For `n = 3`, `edges = [[0, 1, 4], [1, 2, -2], [0, 2, 3]]` and `source = 0` the answer is `[0, 4, 2]`.

### Examples

**Example 1**

Input:

```python
bellman_ford(3, [[0, 1, 4], [1, 2, -2], [0, 2, 3]], 0)
```

Output:

```text
[0, 4, 2]
```

**Example 2**

Input:

```python
bellman_ford(3, [[0, 1, 1], [1, 2, -3], [2, 1, 1]], 0)
```

Output:

```text
[]
```

### Constraints

- `1 <= n <= 1000`
- `0 <= len(edges) <= 5000`
- `-100 <= w <= 100`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Dijkstra fails with negative weights (a node's distance can still drop after it is "finished"). **Bellman–Ford** is simpler: **relax every edge** (`if dist[a] + w < dist[b]: dist[b] = dist[a] + w`) and repeat this `n - 1` times. A shortest path has at most `n - 1` edges, and round `i` makes sure all paths with at most `i` edges are right.

**Detecting a negative cycle:** do one more round. If any edge still improves a distance, a negative cycle is reachable (distances would keep decreasing forever). Only edges whose start is reachable (`dist[a]` is finite) count. `O(n · m)`.

## Explanation

The first `n - 1` rounds compute the distances; the last round is the cycle test. Edges out of unreachable nodes are skipped.
