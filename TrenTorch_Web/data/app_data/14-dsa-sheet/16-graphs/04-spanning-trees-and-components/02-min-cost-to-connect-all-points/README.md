---
name: sheet-min-cost-to-connect-all-points
title: 'Connect All Points'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Advanced
theory: points-on-a-plane
---

## Statement

`points[i] = [x, y]` are points on a plane. The cost to connect two points is their **Manhattan distance** `|x1 - x2| + |y1 - y2|`. Return the **least total cost** to connect all points so that any point can reach any other (cables can be shared).

For `[[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]` the answer is `20`.

### Examples

**Example 1**

Input:

```python
min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]])
```

Output:

```text
20
```

**Example 2**

Input:

```python
min_cost_connect_points([[3, 12], [-2, 5], [-4, 1]])
```

Output:

```text
18
```

### Constraints

- `0 <= len(points) <= 1000`
- `-10**6 <= x, y <= 10**6`

## Explanation

`best` starts at infinity except for point 0. Every round adds one point and relaxes the distances to all points still outside the tree.

### Complexity

- Time: O(n^2). Prim's algorithm without a heap: `n` rounds, each scanning `n` points; the graph has `n^2 / 2` edges, so this is linear in the number of edges.
- Space: O(n). The distance and visited arrays.
