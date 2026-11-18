---
name: sheet-minimum-spanning-tree
title: 'Minimum Spanning Tree'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Advanced
theory: kruskal-cheapest-edge-first
---

## Statement

A weighted undirected graph has `n` nodes and `edges` `[a, b, w]`. A **spanning tree** joins all nodes with `n - 1` edges and no cycle. Return the **smallest possible total weight** of a spanning tree, or `-1` if the graph is not connected. For `n = 1` the answer is `0`.

For `n = 4` and `edges = [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 5]]` the answer is `6`.

### Examples

**Example 1**

Input:

```python
mst_weight(4, [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 5]])
```

Output:

```text
6
```

**Example 2**

Input:

```python
mst_weight(3, [[0, 1, 4]])
```

Output:

```text
-1
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- `1 <= w <= 10**4`

## Explanation

`taken` counts the accepted edges; the total weight grows with each accepted edge.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                     | Variables                                                                                                     |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `parent = list(range(n))`                           | `parent = [0, 1, 2, 3]`                                                                                       |
| `taken = 0`                                         | `size = [1, 1, 1, 1], find = <function mst_weight.<locals>.find at 0x000002BDE6AF1360>, total = 0, taken = 0` |
| `parent[rb] = ra`                                   | `parent = [0, 0, 2, 3], a = 0, b = 1, w = 1, ra = 0, rb = 1`                                                  |
| `for a, b, w in sorted(edges, key=lambda e: e[2]):` | `size = [2, 1, 1, 1], total = 1, taken = 1, a = 1, b = 2, w = 2`                                              |
| `total += w`                                        | `parent = [0, 0, 0, 3], size = [3, 1, 1, 1], total = 3, rb = 2`                                               |
| `parent[rb] = ra`                                   | `parent = [0, 0, 0, 0], taken = 2, a = 2, b = 3, w = 3, rb = 3`                                               |
| `taken += 1`                                        | `size = [4, 1, 1, 1], total = 6, taken = 3`                                                                   |
| `return`                                            | `returned = 6`                                                                                                |

### Complexity

- Time: O(e log e). Kruskal's algorithm: sorting the edges dominates, and the `e` union-find operations cost almost nothing extra.
- Space: O(n + e). The union-find arrays and the sorted edges.
