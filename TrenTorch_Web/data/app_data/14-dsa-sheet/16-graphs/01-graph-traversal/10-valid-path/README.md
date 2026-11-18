---
name: sheet-valid-path
title: 'Is There a Path?'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
theory: connected-components
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

## Explanation

The search marks nodes as seen so each is processed once, and stops early when the destination is found.

### Complexity

- Time: O(n + e). Each node and edge is visited at most once.
- Space: O(n + e). The adjacency lists, the visited array and the stack.
