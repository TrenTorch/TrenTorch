---
name: sheet-is-graph-bipartite
title: 'Is the Graph Bipartite?'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
theory: bipartite-graphs-and-two-colours
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

## Explanation

`color[v]` is 0, 1 or -1 (unknown). `1 - color[node]` is the opposite colour. A self-loop `[a, a]` conflicts at once.

### Complexity

- Time: O(n + e). Each node and edge is visited once while the nodes are 2-coloured.
- Space: O(n + e). The adjacency lists, the colours and the queue.
