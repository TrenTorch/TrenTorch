---
name: sheet-is-graph-a-tree
title: 'Is the Graph a Tree?'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Beginner
---

## Statement

A graph has `n` nodes (`0` to `n - 1`) and undirected `edges`. Return `True` if it is a **tree**: connected and without cycles.

For `n = 5` and `edges = [[0, 1], [0, 2], [0, 3], [1, 4]]` the answer is `True`; adding `[2, 3]` makes it `False`.

### Examples

**Example 1**

Input:

```python
valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]])
```

Output:

```text
True
```

**Example 2**

Input:

```python
valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]])
```

Output:

```text
False
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- An empty graph (`n = 0`) is not a tree.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **disjoint set union (DSU)**, also called **union-find**, keeps track of a partition of items into groups. It supports two operations: `find(x)` returns the representative (the "leader") of the group of `x`, and `union(a, b)` merges the groups of `a` and `b`. Store a `parent` array where each item points toward its leader. Two tricks make it almost `O(1)` per operation: **path compression** (while walking up in `find`, point nodes closer to the root) and **union by size** (attach the smaller group under the larger). Two items are in the same group exactly when `find(a) == find(b)`.

A tree with `n` nodes has **exactly `n - 1` edges** and is **connected**. Equivalently: `n - 1` edges and **no cycle**. So: if `len(edges) != n - 1`, answer `False`. Otherwise add the edges to a union-find; if any edge joins two nodes that are already in the same group, there is a cycle (and so the graph cannot be connected): `False`. Else `True`.

The count test is what saves you from checking connectivity separately: with `n - 1` edges and no cycle, the graph is a connected tree. `O(n α(n))`.

## Explanation

With exactly `n - 1` edges, "no cycle" and "connected" are the same condition, so detecting a cycle with union-find is enough.
