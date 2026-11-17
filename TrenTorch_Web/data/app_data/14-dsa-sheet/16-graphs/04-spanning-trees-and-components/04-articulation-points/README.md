---
name: sheet-articulation-points
title: 'Articulation Points'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Mastery
theory: articulation-points
---

## Statement

The undirected graph has `n` nodes and `edges`, and it is connected. A node is an **articulation point** (cut vertex) if **removing it, together with its edges,** leaves the remaining nodes disconnected. Return the articulation points in increasing order.

For `n = 5` and `edges = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]` the answer is `[1, 3]`.

### Examples

**Example 1**

Input:

```python
articulation_points(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]])
```

Output:

```text
[1, 3]
```

**Example 2**

Input:

```python
articulation_points(3, [[0, 1], [1, 2], [2, 0]])
```

Output:

```text
[]
```

### Constraints

- `1 <= n <= 100000`
- `n - 1 <= len(edges) <= 200000`
- No repeated edges, no self-loops.

## Explanation

`root_children` counts the depth-first-search children of the start node: the start node is a cut vertex only when it has two or more. For any other node `u`, a child `v` whose `low[v] >= disc[u]` cannot reach above `u` without passing through it, so `u` is a cut vertex.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables                                                                                                                                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adj = [[] for _ in range(n)]`  | `adj = [[], [], [], [], []]`                                                                                                                                                                            |
| `adj[b].append(a)`              | `adj = [[1, 2], [0, 2, 3], [1, 0], [1], []], a = 1, b = 3`                                                                                                                                              |
| `root_children = 0`             | `adj = [[1, 2], [0, 2, 3], [1, 0], [1, 4], [3]], a = 3, b = 4, disc = [0, -1, -1, -1, -1], low = [0, 0, 0, 0, 0], is_cut = [False, False, False, False, False], timer = 1, root = 0, root_children = 0` |
| `node, parent, i = stack.pop()` | `disc = [0, 1, -1, -1, -1], low = [0, 1, 0, 0, 0], timer = 2, root_children = 1, stack = [(0, -1, 1)], node = 1, parent = 0, i = 1, nxt = 0`                                                            |
| `nxt = adj[node][i]`            | `disc = [0, 1, 2, -1, -1], low = [0, 1, 2, 0, 0], timer = 3, stack = [(0, -1, 1), (1, 0, 2), (2, 1, 2)], node = 2, parent = 1`                                                                          |
| `nxt = adj[node][i]`            | `disc = [0, 1, 2, 3, -1], low = [0, 0, 0, 3, 0], timer = 4, stack = [(0, -1, 1), (1, 0, 3), (3, 1, 1)], node = 3, i = 0, nxt = 1`                                                                       |
| `is_cut[parent] = True`         | `disc = [0, 1, 2, 3, 4], low = [0, 0, 0, 3, 4], is_cut = [False, False, False, True, False], timer = 5, stack = [(0, -1, 1), (1, 0, 3), (3, 1, 2)], node = 4, parent = 3, i = 1, nxt = 3`               |
| `return`                        | `returned = [1, 3]`                                                                                                                                                                                     |

### Complexity

- Time: O(n + e). One depth-first search computes discovery and low-link times.
- Space: O(n + e). The adjacency lists, the two time arrays and the stack.
