---
name: sheet-dijkstra-shortest-paths
title: 'Dijkstra: Shortest Distances'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
theory: dijkstra-the-idea-and-a-worked-example
---

## Statement

A **directed** graph has `n` nodes and weighted `edges` `[a, b, w]` (an arrow from `a` to `b` of length `w >= 0`). Return a list with the **shortest distance from `source` to every node**, using `-1` for nodes that cannot be reached.

For `n = 3`, `edges = [[0, 1, 4], [0, 2, 1], [2, 1, 2]]` and `source = 0` the answer is `[0, 3, 1]`.

The starter code finds the closest unfinished node by scanning all nodes every time. It is correct but too slow for a large graph.

### Examples

**Example 1**

Input:

```python
shortest_distances(3, [[0, 1, 4], [0, 2, 1], [2, 1, 2]], 0)
```

Output:

```text
[0, 3, 1]
```

**Example 2**

Input:

```python
shortest_distances(3, [[1, 2, 5]], 0)
```

Output:

```text
[0, -1, -1]
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- `0 <= w <= 10**4`

## Explanation

Pushing a new `(distance, node)` pair on every improvement leaves old pairs in the heap; `if d > dist[u]: continue` skips them.

### Complexity

- Time: O((n + e) log n). Each edge can push one heap entry (`O(log e)`, which is `O(log n)`), and stale entries are skipped when popped.
- Space: O(n + e). The adjacency lists, the distances and the heap.
