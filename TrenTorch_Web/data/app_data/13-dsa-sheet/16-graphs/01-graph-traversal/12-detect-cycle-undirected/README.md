---
name: sheet-detect-cycle-undirected
title: 'Cycle in an Undirected Graph'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
---

## Statement

Return `True` if the undirected graph with `n` nodes and the given `edges` contains a **cycle** (a path that returns to its start without reusing an edge). Two copies of the same edge `[a, b]` and `[b, a]` count as a cycle of length 2, and an edge `[a, a]` from a node to itself is a cycle.

For `n = 4` and `edges = [[0, 1], [1, 2], [2, 0], [3, 3]]` the answer is `True`.

### Examples

**Example 1**

Input:

```python
has_cycle_undirected(4, [[0, 1], [1, 2], [2, 0], [3, 3]])
```

Output:

```text
True
```

**Example 2**

Input:

```python
has_cycle_undirected(4, [[0, 1], [1, 2], [2, 3]])
```

Output:

```text
False
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

In a search of an undirected graph, you reach a node that is **already visited** and that is **not the node you just came from** exactly when there is a cycle. The parent must be excluded because every edge leads back to where you came from.

Edge cases: a **repeated edge** or a **self-loop** is a cycle. If you handle edges as an indexed list, record the **edge** you arrived by (not only the parent node) so that two parallel edges between the same pair are detected.

A simpler method uses a **disjoint set (union-find)**: process the edges; if an edge joins two nodes that are already in the same set, it closes a cycle. `O(n + m)`.

## Explanation

The search keeps `(node, edge_id_used_to_arrive)`. Meeting a visited node through a different edge means a cycle.
