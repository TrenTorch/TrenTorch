---
name: sheet-union-find-operations
title: 'Union-Find Operations'
tags: [dsa-sheet, design, classic-designs]
difficulty: Intermediate
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Build a **disjoint set union**. At the start there are `n` separate items `0..n-1`. Operations: `"union a b"` merges the groups of `a` and `b` (no result), `"connected a b"` returns `1` if `a` and `b` are in the same group and `0` otherwise, and `"size a"` returns the **size of the group of `a`**. Return the results of all `connected` and `size` operations.

For `n = 5` and `["union 0 1", "union 1 2", "connected 0 2", "connected 0 3", "size 2"]` the answer is `[1, 0, 3]`.

The starter code relabels a whole group on each union and counts labels for each size. It is correct but too slow for many items.

### Examples

**Example 1**

Input:

```python
run_union_find(5, ['union 0 1', 'union 1 2', 'connected 0 2', 'connected 0 3', 'size 2'])
```

Output:

```text
[1, 0, 3]
```

**Explanation:** Unioning 0 1 and 1 2 makes elements 0,1,2 together; connected 0 2 returns 1, connected 0 3 returns 0, and size 2 reports the group size 3.

**Example 2**

Input:

```python
run_union_find(1, ['size 0'])
```

Output:

```text
[1]
```

**Explanation:** With only one element, size 0 outputs 1 as its group contains the single element.

### Constraints

- `1 <= n <= 100000`
- `0 <= len(ops) <= 100000`
- `0 <= a, b < n`

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

This is the union-find structure from the graphs topic as a class. Keep `parent[x]` (the leader chain) and `size[leader]`. `find(x)` follows the parents to the leader and **compresses the path** (points nodes closer to the leader). `union(a, b)` links the **smaller** group under the larger (**union by size**) and adds the sizes. Then `connected` is `find(a) == find(b)` and `size(a)` is `size[find(a)]`.

With both tricks every operation is almost `O(1)` (inverse Ackermann time).

## Explanation

`find` uses path halving. `union` swaps so the larger group's leader stays on top, and the size of the new leader grows.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                      | Variables                                                                                               |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `parent = list(range(n))`                                            | `parent = [0, 1, 2, 3, 4]`                                                                              |
| `out = []`                                                           | `size = [1, 1, 1, 1, 1], find = <function run_union_find.<locals>.find at 0x000001F485501..., out = []` |
| `parent[b] = a`                                                      | `parent = [0, 0, 2, 3, 4], op = 'union 0 1', parts = ['union', '0', '1'], a = 0, b = 1`                 |
| `parts = op.split()`                                                 | `size = [2, 1, 1, 1, 1], op = 'union 1 2', parts = ['union', '1', '2']`                                 |
| `size[a] += size[b]`                                                 | `parent = [0, 0, 0, 3, 4], size = [3, 1, 1, 1, 1], b = 2`                                               |
| `out.append(1 if find(int(parts[1])) == find(int(parts[2])) else 0)` | `out = [1], op = 'connected 0 2', parts = ['connected', '0', '2']`                                      |
| `for op in ops:`                                                     | `out = [1, 0], op = 'size 2', parts = ['connected', '0', '3']`                                          |
| `return`                                                             | `returned = [1, 0, 3]`                                                                                  |
