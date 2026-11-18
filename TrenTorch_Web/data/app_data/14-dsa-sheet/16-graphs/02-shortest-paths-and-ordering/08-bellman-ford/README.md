---
name: sheet-bellman-ford
title: 'Bellman-Ford With Negative Edges'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
theory: bellman-ford-and-negative-weights
---

## Statement

A directed graph has `n` nodes and weighted `edges` `[a, b, w]`, where **`w` can be negative**. Return the list of **shortest distances from `source`**, using `None` for unreachable nodes. If a **negative cycle** (a cycle whose total weight is negative) can be reached from `source`, shortest distances do not exist: return an **empty list**.

For `n = 3`, `edges = [[0, 1, 4], [1, 2, -2], [0, 2, 3]]` and `source = 0` the answer is `[0, 4, 2]`.

### Examples

**Example 1**

Input:

```python
bellman_ford(3, [[0, 1, 4], [1, 2, -2], [0, 2, 3]], 0)
```

Output:

```text
[0, 4, 2]
```

**Example 2**

Input:

```python
bellman_ford(3, [[0, 1, 1], [1, 2, -3], [2, 1, 1]], 0)
```

Output:

```text
[]
```

### Constraints

- `1 <= n <= 1000`
- `0 <= len(edges) <= 5000`
- `-100 <= w <= 100`

## Explanation

The first `n - 1` rounds compute the distances; the last round is the cycle test. Edges out of unreachable nodes are skipped.

### Complexity

- Time: O(n * e). `n - 1` rounds, each relaxing every edge once, plus one round to detect a negative cycle.
- Space: O(n). The distance array.
