---
name: sheet-detect-cycle-directed
title: 'Cycle in a Directed Graph'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
---

## Statement

The graph has `n` nodes and **directed** `edges` `[a, b]` meaning an arrow from `a` to `b`. Return `True` if it contains a **directed cycle** (you can follow arrows and return to the start). A self-loop `[a, a]` is a cycle.

For `n = 3` and `edges = [[0, 1], [1, 2], [2, 0]]` the answer is `True`.

### Examples

**Example 1**

Input:

```python
has_cycle_directed(3, [[0, 1], [1, 2], [2, 0]])
```

Output:

```text
True
```

**Example 2**

Input:

```python
has_cycle_directed(3, [[0, 1], [0, 2], [1, 2]])
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

For directed graphs, "visited" is not enough: meeting a visited node does not always mean a cycle (two arrows can lead to the same node). A cycle means you meet a node that is **still on the current path** (an ancestor in the DFS).

Use three states for each node: **unvisited**, **in progress** (on the current DFS path) and **done**. Reaching an in-progress node closes a cycle. A node becomes done once all its descendants are finished. Use an explicit stack to avoid deep recursion.

A second method is **Kahn's algorithm** (topological sort): repeatedly remove nodes with no incoming arrows; if some nodes can never be removed, they lie on or after a cycle. `O(n + m)`.

## Explanation

The iterative DFS keeps an index into each node's adjacency list so it can come back to a node after finishing a child. `state` is 0 (new), 1 (on the path) or 2 (done).
