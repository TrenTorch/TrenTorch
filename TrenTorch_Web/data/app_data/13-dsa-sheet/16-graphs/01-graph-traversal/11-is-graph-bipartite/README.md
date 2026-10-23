---
name: sheet-is-graph-bipartite
title: 'Is the Graph Bipartite?'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
---

## Statement

A graph with `n` nodes and undirected `edges` is **bipartite** if the nodes can be split into **two groups** so that every edge joins a node of one group to a node of the other (no edge inside a group). Return `True` if the graph is bipartite. The graph may have several components.

A triangle is not bipartite; a square is.

### Examples

**Example 1**

Input:

```python
is_bipartite(4, [[0, 1], [1, 2], [2, 3], [3, 0]])
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_bipartite(3, [[0, 1], [1, 2], [2, 0]])
```

Output:

```text
False
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- No node has an edge to itself unless the graph is not bipartite.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Try to **colour the nodes with two colours** so that every edge joins different colours. Start a BFS at an uncoloured node and give it colour 0. Each neighbour must get the **opposite** colour: if it is uncoloured, colour and queue it; if it is already coloured with the **same** colour as the current node, there is a conflict: the graph is not bipartite.

Do this from every uncoloured node, because the graph can have several components. Equivalent view: a graph is bipartite exactly when it has **no cycle of odd length**. `O(n + m)`.

## Explanation

`color[v]` is 0, 1 or -1 (unknown). `1 - color[node]` is the opposite colour. A self-loop `[a, a]` conflicts at once.
