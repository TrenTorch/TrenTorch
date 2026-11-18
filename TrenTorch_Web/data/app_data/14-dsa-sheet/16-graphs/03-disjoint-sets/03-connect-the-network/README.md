---
name: sheet-connect-the-network
title: 'Operations to Connect the Network'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Intermediate
theory: spotting-cycles
---

## Statement

`n` computers (`0` to `n - 1`) are joined by cables `connections` (`[a, b]`). In one operation you can take a cable between two directly connected computers and use it to join any two computers instead. Return the **fewest operations** to make all computers connected, or `-1` if it is impossible.

For `n = 4` and `connections = [[0, 1], [0, 2], [1, 2]]` the answer is `1`.

### Examples

**Example 1**

Input:

```python
make_connected(4, [[0, 1], [0, 2], [1, 2]])
```

Output:

```text
1
```

**Example 2**

Input:

```python
make_connected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]])
```

Output:

```text
2
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(connections) <= 200000`

## Explanation

`components` starts at `n` and drops by one for every successful union. The cable count test decides when the answer is impossible.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `parent = list(range(n))`   | `parent = [0, 1, 2, 3]`                                                                    |
| `def find(a):`              | `size = [1, 1, 1, 1], find = <function make_connected.<locals>.find at 0x000002BDE6AF3...` |
| `ra, rb = find(a), find(b)` | `components = 4, a = 0, b = 1, ra = 0, rb = 1`                                             |
| `size[ra] += size[rb]`      | `parent = [0, 0, 2, 3], size = [2, 1, 1, 1]`                                               |
| `for a, b in connections:`  | `components = 3, b = 2`                                                                    |
| `parent[rb] = ra`           | `parent = [0, 0, 0, 3], rb = 2`                                                            |
| `for a, b in connections:`  | `size = [3, 1, 1, 1], components = 2, a = 1`                                               |
| `return`                    | `returned = 1`                                                                             |

### Complexity

- Time: O(n * alpha(n)). One union-find operation per cable; with union by size and path halving each operation is `O(alpha(n))`, which is below 5 for any input that fits in memory.
- Space: O(n). The parent and size arrays.
