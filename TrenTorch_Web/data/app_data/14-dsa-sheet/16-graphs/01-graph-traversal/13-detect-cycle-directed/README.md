---
name: sheet-detect-cycle-directed
title: 'Cycle in a Directed Graph'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
theory: cycles-in-a-directed-graph
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

## Explanation

The iterative DFS keeps an index into each node's adjacency list so it can come back to a node after finishing a child. `state` is 0 (new), 1 (on the path) or 2 (done).

### Complexity

- Time: O(n + e). Depth-first search with three colours; an edge into a node still on the current path closes a cycle.
- Space: O(n + e). The adjacency lists, the states and the stack.
