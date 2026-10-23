---
name: sheet-strongly-connected-components
title: 'Strongly Connected Components'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Mastery
---

## Statement

In a **directed** graph with `n` nodes, two nodes are in the same **strongly connected component (SCC)** if each can reach the other. Return the number of SCCs.

For `n = 5` and `edges = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]` the answer is `3` (`{0, 1, 2}`, `{3}`, `{4}`).

### Examples

**Example 1**

Input:

```python
count_scc(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
count_scc(3, [])
```

Output:

```text
3
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Components of an undirected graph are found by one search, but in a directed graph, reaching `b` from `a` does not mean `a` is reachable from `b`.

**Kosaraju's algorithm** uses two DFS passes:

1. Run a DFS on the graph and record the nodes in the order they **finish** (post-order).
2. Build the **reversed** graph (every arrow flipped). Process the nodes in **decreasing finish time**; each unvisited node starts a DFS on the reversed graph that visits exactly one SCC.

Why it works: the node that finishes last in pass 1 belongs to a "source" component; in the reversed graph you cannot leave that component into another unvisited one. `O(n + m)`; use explicit stacks for deep graphs.

## Explanation

`order` is the post-order of pass 1. The second loop counts how many times a new DFS on the reversed graph is needed.
