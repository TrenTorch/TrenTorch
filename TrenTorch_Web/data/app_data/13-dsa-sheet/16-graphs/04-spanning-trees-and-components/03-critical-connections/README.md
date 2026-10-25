---
name: sheet-critical-connections
title: 'Critical Connections (Bridges)'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Mastery
---

## Statement

`n` servers (`0` to `n - 1`) are joined by undirected `connections`. The network is connected. A connection is **critical** (a **bridge**) if removing it makes some servers unable to reach each other. Return all critical connections as `[a, b]` with `a < b`, sorted.

For `n = 4` and `connections = [[0, 1], [1, 2], [2, 0], [1, 3]]` the answer is `[[1, 3]]`.

### Examples

**Example 1**

Input:

```python
critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]])
```

Output:

```text
[[1, 3]]
```

**Explanation:** The connection [1, 3] is critical because removing it disconnects server 3 from the rest of the network.

**Example 2**

Input:

```python
critical_connections(2, [[0, 1]])
```

Output:

```text
[[0, 1]]
```

**Explanation:** The connection [0, 1] is critical because removing it disconnects the two servers.

### Constraints

- `2 <= n <= 100000`
- `n - 1 <= len(connections) <= 200000`
- No repeated connections, no self-loops.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Removing an edge `(u, v)` disconnects the graph exactly when there is **no other route** between `u` and `v`; that is, no cycle contains the edge. Testing every edge by removing it costs `O(m·(n + m))`.

**Tarjan's bridge-finding algorithm** does it in one DFS. For each node record `disc[v]`, the time it was first visited, and `low[v]`, the earliest discovery time reachable from `v`'s subtree using **at most one back edge**. An edge `(parent, child)` of the DFS tree is a **bridge** when `low[child] > disc[parent]`: the child's subtree cannot reach the parent or anything above it without this edge.

Write the DFS with an explicit stack: with 100,000 nodes a recursive DFS would exceed Python's recursion limit. `O(n + m)`.

## Explanation

The stack holds `(node, parent, iterator position)`. When a child finishes, its `low` is folded into the parent's, and the bridge test is applied.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                          | Variables                                                                                                                             |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `adj = [[] for _ in range(n)]`                           | `adj = [[], [], [], []]`                                                                                                              |
| `adj[b].append(a)`                                       | `adj = [[1, 2], [0, 2], [1, 0], []], a = 2, b = 0`                                                                                    |
| `disc[root] = low[root] = timer`                         | `adj = [[1, 2], [0, 2, 3], [1, 0], [1]], a = 1, b = 3, disc = [0, -1, -1, -1], low = [0, 0, 0, 0], bridges = [], timer = 0, root = 0` |
| `node, parent, i = stack.pop()`                          | `disc = [0, 1, -1, -1], low = [0, 1, 0, 0], timer = 2, stack = [(0, -1, 1)], node = 1, parent = 0, i = 0, nxt = 1`                    |
| `stack.append((node, parent, i + 1))`                    | `disc = [0, 1, 2, -1], low = [0, 1, 2, 0], timer = 3, stack = [(0, -1, 1), (1, 0, 2), (2, 1, 1)], node = 2, parent = 1, nxt = 2`      |
| `stack.append((node, parent, i + 1))`                    | `low = [0, 0, 0, 0], stack = [(0, -1, 1), (1, 0, 3)], node = 1, parent = 0, i = 2, nxt = 0`                                           |
| `bridges.append([min(parent, node), max(parent, node)])` | `disc = [0, 1, 2, 3], low = [0, 0, 0, 3], bridges = [[1, 3]], timer = 4, node = 3, parent = 1, i = 1, nxt = 1`                        |
| `return`                                                 | `returned = [[1, 3]]`                                                                                                                 |
