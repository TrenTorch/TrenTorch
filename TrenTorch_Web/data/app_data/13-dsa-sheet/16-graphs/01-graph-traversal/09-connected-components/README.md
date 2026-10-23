---
name: sheet-connected-components
title: 'Number of Connected Components'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
---

## Statement

A graph has `n` nodes numbered `0` to `n - 1` and some undirected `edges`. Return the **number of connected components**: groups of nodes that can reach each other.

For `n = 5` and `edges = [[0, 1], [1, 2], [3, 4]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
count_components(5, [[0, 1], [1, 2], [3, 4]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
count_components(3, [])
```

Output:

```text
3
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- `0 <= a, b < n`; there may be repeated edges.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Build the adjacency list first: for each edge `[a, b]` add `b` to `a`'s list and `a` to `b`'s. Then loop over the nodes: when you meet a node that is not visited, start a search (BFS or DFS) from it and mark everything it reaches; that search covers exactly one component, so add one to the count.

`O(n + m)`. Do not forget isolated nodes (nodes with no edges): each is a component of its own. An explicit stack avoids Python's recursion limit.

## Explanation

`seen` marks visited nodes; each unvisited start node begins a new component.
