---
name: sheet-floyd-warshall
title: 'Floyd-Warshall: All Pairs'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
theory: floyd-warshall-all-pairs
---

## Statement

A directed graph has `n` nodes and weighted `edges` `[a, b, w]` with `w >= 0`. Return an `n x n` matrix where entry `[i][j]` is the **shortest distance from `i` to `j`**, with `-1` if `j` cannot be reached from `i`. The distance from a node to itself is `0`.

For `n = 3` and `edges = [[0, 1, 4], [1, 2, 1], [0, 2, 7]]` the answer is `[[0, 4, 5], [-1, 0, 1], [-1, -1, 0]]`.

### Examples

**Example 1**

Input:

```python
all_pairs_shortest(3, [[0, 1, 4], [1, 2, 1], [0, 2, 7]])
```

Output:

```text
[[0, 4, 5], [-1, 0, 1], [-1, -1, 0]]
```

**Example 2**

Input:

```python
all_pairs_shortest(2, [])
```

Output:

```text
[[0, -1], [-1, 0]]
```

### Constraints

- `1 <= n <= 120`
- `0 <= len(edges) <= 3000`
- `0 <= w <= 10**4`

## Explanation

The matrix starts with the edge weights (and 0 on the diagonal); `inf` marks missing edges. After the triple loop, `inf` entries become `-1`.

### Complexity

- Time: O(n^3). Three nested loops over the nodes.
- Space: O(n^2). The distance matrix.
