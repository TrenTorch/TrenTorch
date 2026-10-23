---
name: sheet-valid-path
title: 'Is There a Path?'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
---

## Statement

A graph has `n` nodes numbered `0` to `n - 1` and undirected `edges`. Return `True` if there is a **path from `source` to `destination`**.

For `n = 3`, `edges = [[0, 1], [1, 2], [2, 0]]`, `source = 0` and `destination = 2` the answer is `True`.

### Examples

**Example 1**

Input:

```python
valid_path(3, [[0, 1], [1, 2], [2, 0]], 0, 2)
```

Output:

```text
True
```

**Example 2**

Input:

```python
valid_path(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5)
```

Output:

```text
False
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- `0 <= source, destination < n`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Build the adjacency list, then run a BFS or DFS from `source`. If you reach `destination` the answer is `True`; if the search ends without it, `False`. A node is its own destination (`source == destination` is `True`). You can stop the search as soon as the destination is seen. `O(n + m)`.

## Explanation

The search marks nodes as seen so each is processed once, and stops early when the destination is found.
