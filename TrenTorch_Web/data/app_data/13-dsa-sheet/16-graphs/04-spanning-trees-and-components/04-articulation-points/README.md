---
name: sheet-articulation-points
title: 'Articulation Points'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Mastery
---

## Statement

The undirected graph has `n` nodes and `edges`, and it is connected. A node is an **articulation point** (cut vertex) if **removing it, together with its edges,** leaves the remaining nodes disconnected. Return the articulation points in increasing order.

For `n = 5` and `edges = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]` the answer is `[1, 3]`.

### Examples

**Example 1**

Input:

```python
articulation_points(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]])
```

Output:

```text
[1, 3]
```

**Explanation:** Removing node 1 separates the triangle component from the chain; removing node 3 isolates node 4, so both are cut vertices.

**Example 2**

Input:

```python
articulation_points(3, [[0, 1], [1, 2], [2, 0]])
```

Output:

```text
[]
```

**Explanation:** All nodes are in a cycle, removing any one keeps graph connected, so no cut vertices.

### Constraints

- `1 <= n <= 100000`
- `n - 1 <= len(edges) <= 200000`
- No repeated edges, no self-loops.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

This is the sibling of the bridges question and uses the same DFS with `disc` and `low` values. A node `u` is an articulation point when:

- `u` is **not the root** and it has a DFS child `v` with `low[v] >= disc[u]` (the subtree of `v` cannot get above `u` without passing through `u`), or
- `u` is the **root** of the DFS and has **two or more children** in the DFS tree.

The root needs its own rule because it has no "above". As before, use an explicit stack for deep graphs. `O(n + m)`.

## Explanation

`children[root]` counts the DFS children of the start node. `low[v] >= disc[u]` marks `u` as a cut vertex when `u` is not the root.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables                                                                                                                                                              |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adj = [[] for _ in range(n)]`  | `adj = [[], [], [], [], []]`                                                                                                                                           |
| `adj[b].append(a)`              | `adj = [[1, 2], [0, 2, 3], [1, 0], [1], []], a = 1, b = 3`                                                                                                             |
| `root_children = 0`             | `adj = [[1, 2], [0, 2, 3], [1, 0], [1, 4], [3]], a = 3, b = 4, disc = [0, -1, -1, -1, -1], low = [0, 0, 0, 0, 0], cut = set(), timer = 1, root = 0, root_children = 0` |
| `node, parent, i = stack.pop()` | `disc = [0, 1, -1, -1, -1], low = [0, 1, 0, 0, 0], timer = 2, root_children = 1, stack = [(0, -1, 1)], node = 1, parent = 0, i = 1, nxt = 0`                           |
| `nxt = adj[node][i]`            | `disc = [0, 1, 2, -1, -1], low = [0, 1, 2, 0, 0], timer = 3, stack = [(0, -1, 1), (1, 0, 2), (2, 1, 2)], node = 2, parent = 1`                                         |
| `nxt = adj[node][i]`            | `disc = [0, 1, 2, 3, -1], low = [0, 0, 0, 3, 0], timer = 4, stack = [(0, -1, 1), (1, 0, 3), (3, 1, 1)], node = 3, i = 0, nxt = 1`                                      |
| `cut.add(parent)`               | `disc = [0, 1, 2, 3, 4], low = [0, 0, 0, 3, 4], cut = {3}, timer = 5, stack = [(0, -1, 1), (1, 0, 3), (3, 1, 2)], node = 4, parent = 3, i = 1, nxt = 3`                |
| `return`                        | `returned = [1, 3]`                                                                                                                                                    |
