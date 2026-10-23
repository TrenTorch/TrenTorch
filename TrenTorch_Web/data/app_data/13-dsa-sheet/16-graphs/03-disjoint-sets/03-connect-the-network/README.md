---
name: sheet-connect-the-network
title: 'Operations to Connect the Network'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Intermediate
---

## Statement

`n` computers (`0` to `n - 1`) are joined by cables `connections` (`[a, b]`). In one operation you can take a cable between two directly connected computers and use it to join any two computers instead. Return the **fewest operations** to make all computers connected, or `-1` if it is impossible.

For `n = 4` and `connections = [[0, 1], [0, 2], [1, 2]]` the answer is `1`.

### Examples

**Example 1**

Input:

```python
make_connected(4, [[0, 1], [0, 2], [1, 2]])
```

Output:

```text
1
```

**Example 2**

Input:

```python
make_connected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]])
```

Output:

```text
2
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(connections) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **disjoint set union (DSU)**, also called **union-find**, keeps track of a partition of items into groups. It supports two operations: `find(x)` returns the representative (the "leader") of the group of `x`, and `union(a, b)` merges the groups of `a` and `b`. Store a `parent` array where each item points toward its leader. Two tricks make it almost `O(1)` per operation: **path compression** (while walking up in `find`, point nodes closer to the root) and **union by size** (attach the smaller group under the larger). Two items are in the same group exactly when `find(a) == find(b)`.

To join `n` computers into one network you need at least `n - 1` cables: if there are fewer, return `-1`. If there are enough, the cables are never the problem: some cables are **redundant** (they close a cycle inside a component) and can be moved freely.

Count the connected components `c` with a union-find. Joining `c` components needs `c - 1` cables, and the redundant ones are enough whenever the total is at least `n - 1`. So the answer is `c - 1`.

## Explanation

`components` starts at `n` and drops by one for every successful union. The cable count test decides when the answer is impossible.
