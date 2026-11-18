---
name: sheet-critical-connections
title: 'Critical Connections (Bridges)'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Mastery
theory: critical-connections
---

## Statement

`n` servers (`0` to `n - 1`) are joined by undirected `connections`. The network is connected. A connection is **critical** (a **bridge**) if removing it makes some servers unable to reach each other. Return all critical connections as `[a, b]` with `a < b`, sorted.

For `n = 4` and `connections = [[0, 1], [1, 2], [2, 0], [1, 3]]` the answer is `[[1, 3]]`.

### Examples

**Example 1**

Input:

```python
critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]])
```

Output:

```text
[[1, 3]]
```

**Example 2**

Input:

```python
critical_connections(2, [[0, 1]])
```

Output:

```text
[[0, 1]]
```

### Constraints

- `2 <= n <= 100000`
- `n - 1 <= len(connections) <= 200000`
- No repeated connections, no self-loops.

## Explanation

The stack holds `(node, parent, iterator position)`. When a child finishes, its `low` is folded into the parent's, and the bridge test is applied.

### Complexity

- Time: O(n + e + b log b). One depth-first search computes discovery and low-link times; `b` bridges are sorted for the output.
- Space: O(n + e). The adjacency lists, the two time arrays and the stack.
