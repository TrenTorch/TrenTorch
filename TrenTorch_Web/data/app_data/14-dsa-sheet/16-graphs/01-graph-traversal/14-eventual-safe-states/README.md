---
name: sheet-eventual-safe-states
title: 'Eventual Safe Nodes'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
theory: eventual-safe-states
---

## Statement

The directed graph has `n` nodes and `edges` `[a, b]` (arrows from `a` to `b`). A node with no outgoing arrows is **terminal**. A node is **safe** if **every** path starting at it eventually reaches a terminal node (it cannot be trapped in a cycle). Return the safe nodes in increasing order.

For `n = 7` and `edges = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 5], [3, 0], [4, 5]]` the answer is `[2, 4, 5, 6]`.

### Examples

**Example 1**

Input:

```python
eventual_safe_nodes(7, [[0, 1], [0, 2], [1, 2], [1, 3], [2, 5], [3, 0], [4, 5]])
```

Output:

```text
[2, 4, 5, 6]
```

**Example 2**

Input:

```python
eventual_safe_nodes(5, [[1, 2], [2, 3], [3, 4], [4, 1]])
```

Output:

```text
[0]
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`

## Explanation

`rev[v]` lists the nodes with an arrow into `v`. The queue starts with the terminal nodes and grows with nodes whose outgoing arrows are all accounted for.

### Complexity

- Time: O(n + e). A topological peel of the reversed graph: a node is safe once all of its out-edges lead to safe nodes.
- Space: O(n + e). The reversed adjacency lists, the out-degrees and the queue.
