---
name: sheet-number-of-shortest-paths
title: 'Number of Shortest Paths'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Mastery
---

## Statement

There are `n` intersections `0` to `n - 1` and two-way `roads` `[a, b, time]` with `time >= 1`. Return the **number of different shortest paths** (by total time) from `0` to `n - 1`, modulo `10**9 + 7`. If there is no path the answer is `0`; for `n = 1` the answer is `1`.

For `n = 4` and `roads = [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
count_shortest_paths(4, [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
count_shortest_paths(2, [])
```

Output:

```text
0
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(roads) <= 200000`
- `1 <= time <= 10**4`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Run Dijkstra and keep, next to each distance, the **number of shortest ways** to reach the node, `ways[v]`. When you relax an edge `u -> v` with new distance `d = dist[u] + w`:

- if `d < dist[v]`, a strictly better route: `dist[v] = d`, `ways[v] = ways[u]`;
- if `d == dist[v]`, another shortest route: `ways[v] += ways[u]`.

Because all times are positive, when a node is popped from the heap its `ways` is final. Take everything modulo `10**9 + 7`. `O((n + m) log n)`.

## Explanation

The two `if` branches update `ways` exactly as described. `ways[0] = 1` seeds the count.
