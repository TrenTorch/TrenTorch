---
name: sheet-range-add-point-query
title: 'Range Add, Point Query'
tags: [dsa-sheet, design, range-structures]
difficulty: Advanced
theory: range-add-with-a-difference-array
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Start with a list of `n` zeros. Operations: `"add l r v"` adds `v` to every element of `l..r` (both included); `"get i"` asks for the current value at position `i`. Return the results of all `get` operations.

For `n = 5` and `["add 1 3 10", "get 2", "add 0 4 -1", "get 0", "get 3"]` the answer is `[10, -1, 9]`.

The starter code adds `v` to each element of the range. It is correct but too slow for big ranges.

### Examples

**Example 1**

Input:

```python
run_range_add(5, ['add 1 3 10', 'get 2', 'add 0 4 -1', 'get 0', 'get 3'])
```

Output:

```text
[10, -1, 9]
```

**Example 2**

Input:

```python
run_range_add(1, ['get 0'])
```

Output:

```text
[0]
```

### Constraints

- `1 <= n <= 100000`
- `0 <= len(ops) <= 50000`
- `-10 <= v <= 10`

## Explanation

The Fenwick tree stores the difference array. Two point updates mark the ends of the range; a prefix sum recovers the value.

### Complexity

- Time: O((n + q) log n). A range add is two updates of a Fenwick tree over differences, and a point query is one prefix sum.
- Space: O(n). The tree.
