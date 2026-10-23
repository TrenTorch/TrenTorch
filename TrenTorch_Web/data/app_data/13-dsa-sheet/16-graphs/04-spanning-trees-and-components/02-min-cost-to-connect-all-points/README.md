---
name: sheet-min-cost-to-connect-all-points
title: 'Connect All Points'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Advanced
---

## Statement

`points[i] = [x, y]` are points on a plane. The cost to connect two points is their **Manhattan distance** `|x1 - x2| + |y1 - y2|`. Return the **least total cost** to connect all points so that any point can reach any other (cables can be shared).

For `[[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]` the answer is `20`.

### Examples

**Example 1**

Input:

```python
min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]])
```

Output:

```text
20
```

**Example 2**

Input:

```python
min_cost_connect_points([[3, 12], [-2, 5], [-4, 1]])
```

Output:

```text
18
```

### Constraints

- `0 <= len(points) <= 1000`
- `-10**6 <= x, y <= 10**6`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Every pair of points is a possible edge, so the graph is **complete**: `n(n-1)/2` edges. Kruskal would sort about half a million edges. For a dense graph, **Prim's algorithm** with plain arrays is better: grow the tree from one point, always adding the **nearest point not yet in the tree**.

Keep `best[v]`, the cheapest distance from `v` to the current tree. Each round pick the unvisited point with the smallest `best`, add its cost, and update the other points' `best` with their distance to the new point. `O(n²)` with no heap.

## Explanation

`best` starts at infinity except for point 0. Every round adds one point and relaxes the distances to all points still outside the tree.
