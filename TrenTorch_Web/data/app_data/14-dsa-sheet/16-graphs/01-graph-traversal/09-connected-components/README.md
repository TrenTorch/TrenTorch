---
name: sheet-connected-components
title: 'Number of Connected Components'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
theory: connected-components
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

## Explanation

`seen` marks visited nodes; each unvisited start node begins a new component.

### Complexity

- Time: O(n + e). Each node and edge is visited once.
- Space: O(n + e). The adjacency lists, the visited array and the stack.
