---
name: sheet-detect-cycle-undirected
title: 'Cycle in an Undirected Graph'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
theory: cycles-in-an-undirected-graph
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

## Explanation

The search keeps `(node, edge_id_used_to_arrive)`. Meeting a visited node through a different edge means a cycle.

### Complexity

- Time: O(n + e). Each node and edge is visited once; an edge back to a visited node (other than the one just used) closes a cycle.
- Space: O(n + e). The adjacency lists, the visited array and the stack.
