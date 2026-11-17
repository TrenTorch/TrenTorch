---
name: sheet-strongly-connected-components
title: 'Strongly Connected Components'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Mastery
theory: strongly-connected-components
---

## Statement

In a **directed** graph with `n` nodes, two nodes are in the same **strongly connected component (SCC)** if each can reach the other. Return the number of SCCs.

For `n = 5` and `edges = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]` the answer is `3` (`{0, 1, 2}`, `{3}`, `{4}`).

### Examples

**Example 1**

Input:

```python
count_scc(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
count_scc(3, [])
```

Output:

```text
3
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`

## Explanation

`order` is the post-order of pass 1. The second loop counts how many times a new DFS on the reversed graph is needed.

### Complexity

- Time: O(n + e). Kosaraju's algorithm: two depth-first searches, each visiting every node and edge once.
- Space: O(n + e). Both adjacency lists, the finish order and the stack.
