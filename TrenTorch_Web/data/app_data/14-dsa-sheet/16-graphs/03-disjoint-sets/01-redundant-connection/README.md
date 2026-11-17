---
name: sheet-redundant-connection
title: 'Redundant Connection'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Intermediate
theory: spotting-cycles
---

## Statement

The nodes are numbered `1` to `n`. The `edges` list a tree with **one extra edge added**, so exactly one cycle exists. Return an edge that can be removed so that the rest is a tree. If several edges can be removed, return the one that appears **last** in `edges`.

For `[[1, 2], [1, 3], [2, 3]]` the answer is `[2, 3]`.

### Examples

**Example 1**

Input:

```python
find_redundant_connection([[1, 2], [1, 3], [2, 3]])
```

Output:

```text
[2, 3]
```

**Example 2**

Input:

```python
find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]])
```

Output:

```text
[1, 4]
```

### Constraints

- `2 <= number of nodes <= 100000`
- `len(edges)` equals the number of nodes
- No other cycle exists apart from the one made by the extra edge.

## Explanation

`find` uses path halving, and `union` attaches the smaller group under the larger one (union by size), so every operation is almost constant time. When `find(a) == find(b)` the edge closes a cycle and is the redundant one; otherwise the two groups are merged.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                                                                                     |
| -------------------------------------- | --------------------------------------------------------------------------------------------- |
| `parent = list(range(len(edges) + 2))` | `parent = [0, 1, 2, 3, 4]`                                                                    |
| `def find(a):`                         | `size = [1, 1, 1, 1, 1], find = <function find_redundant_connection.<locals>.find at 0x00...` |
| `ra, rb = find(a), find(b)`            | `a = 1, b = 2, ra = 1, rb = 2`                                                                |
| `size[ra] += size[rb]`                 | `parent = [0, 1, 1, 3, 4], size = [1, 2, 1, 1, 1]`                                            |
| `for a, b in edges:`                   | `b = 3`                                                                                       |
| `parent[rb] = ra`                      | `parent = [0, 1, 1, 1, 4], rb = 3`                                                            |
| `for a, b in edges:`                   | `size = [1, 3, 1, 1, 1], a = 2`                                                               |
| `return`                               | `returned = [2, 3]`                                                                           |

### Complexity

- Time: O(n * alpha(n)). One union-find operation per edge; with union by size and path halving each operation is `O(alpha(n))`, which is below 5 for any input that fits in memory.
- Space: O(n). The parent and size arrays.
