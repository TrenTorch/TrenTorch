---
name: sheet-is-graph-a-tree
title: 'Is the Graph a Tree?'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Beginner
theory: spotting-cycles
---

## Statement

A graph has `n` nodes (`0` to `n - 1`) and undirected `edges`. Return `True` if it is a **tree**: connected and without cycles.

For `n = 5` and `edges = [[0, 1], [0, 2], [0, 3], [1, 4]]` the answer is `True`; adding `[2, 3]` makes it `False`.

### Examples

**Example 1**

Input:

```python
valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]])
```

Output:

```text
True
```

**Example 2**

Input:

```python
valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]])
```

Output:

```text
False
```

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- An empty graph (`n = 0`) is not a tree.

## Explanation

With exactly `n - 1` edges, "no cycle" and "connected" are the same condition, so detecting a cycle with union-find is enough.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                                                |
| --------------------------- | -------------------------------------------------------------------------------------------------------- |
| `parent = list(range(n))`   | `parent = [0, 1, 2, 3, 4]`                                                                               |
| `for a, b in edges:`        | `size = [1, 1, 1, 1, 1], find = <function valid_tree.<locals>.find at 0x000002BDE70576D0>, a = 0, b = 1` |
| `parent[rb] = ra`           | `parent = [0, 0, 2, 3, 4], ra = 0, rb = 1`                                                               |
| `ra, rb = find(a), find(b)` | `size = [2, 1, 1, 1, 1], b = 2, rb = 2`                                                                  |
| `for a, b in edges:`        | `parent = [0, 0, 0, 3, 4], size = [3, 1, 1, 1, 1], b = 3`                                                |
| `size[ra] += size[rb]`      | `parent = [0, 0, 0, 0, 4], size = [4, 1, 1, 1, 1], rb = 3`                                               |
| `ra, rb = find(a), find(b)` | `a = 1, b = 4, rb = 4`                                                                                   |
| `return`                    | `returned = True`                                                                                        |

### Complexity

- Time: O(n * alpha(n)). One union-find operation per edge; with union by size and path halving each operation is `O(alpha(n))`, which is below 5 for any input that fits in memory.
- Space: O(n). The parent and size arrays.
