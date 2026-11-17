---
name: sheet-number-of-shortest-paths
title: 'Number of Shortest Paths'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Mastery
theory: counting-shortest-paths
---

## Statement

There are `n` intersections `0` to `n - 1` and two-way `roads` `[a, b, time]` with `time >= 1`. Return the **number of different shortest paths** (by total time) from `0` to `n - 1`, modulo `10**9 + 7`. If there is no path the answer is `0`; for `n = 1` the answer is `1`.

For `n = 4` and `roads = [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
count_shortest_paths(4, [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
count_shortest_paths(2, [])
```

Output:

```text
0
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(roads) <= 200000`
- `1 <= time <= 10**4`

## Explanation

The two `if` branches update `ways` exactly as described. `ways[0] = 1` seeds the count.

### Complexity

- Time: O((n + e) log n). Dijkstra that also adds up the number of shortest paths into each node.
- Space: O(n + e). The adjacency lists, the distances, the counts and the heap.
