---
name: sheet-minimum-spanning-tree
title: 'Minimum Spanning Tree'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Advanced
---

## Statement

A weighted undirected graph has `n` nodes and `edges` `[a, b, w]`. A **spanning tree** joins all nodes with `n - 1` edges and no cycle. Return the **smallest possible total weight** of a spanning tree, or `-1` if the graph is not connected. For `n = 1` the answer is `0`.

For `n = 4` and `edges = [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 5]]` the answer is `6`.

### Examples

**Example 1**

Input:

```python
mst_weight(4, [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 5]])
```

Output:

```text
6
```

**Example 2**

Input:

```python
mst_weight(3, [[0, 1, 4]])
```

Output:

```text
-1
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- `1 <= w <= 10**4`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **disjoint set union (DSU)**, also called **union-find**, keeps track of a partition of items into groups. It supports two operations: `find(x)` returns the representative (the "leader") of the group of `x`, and `union(a, b)` merges the groups of `a` and `b`. Store a `parent` array where each item points toward its leader. Two tricks make it almost `O(1)` per operation: **path compression** (while walking up in `find`, point nodes closer to the root) and **union by size** (attach the smaller group under the larger). Two items are in the same group exactly when `find(a) == find(b)`.

**Kruskal's algorithm** is greedy: sort the edges by weight; take an edge if it joins two **different** groups (use the union-find), skip it if the ends are already connected (it would close a cycle). Stop when you have `n - 1` edges. The greedy choice is safe: the lightest edge that does not close a cycle belongs to some minimum spanning tree (the _cut property_).

If fewer than `n - 1` edges could be taken, the graph is disconnected: `-1`. `O(m log m)` for the sort.

## Explanation

`taken` counts the accepted edges; the total weight grows with each accepted edge.
