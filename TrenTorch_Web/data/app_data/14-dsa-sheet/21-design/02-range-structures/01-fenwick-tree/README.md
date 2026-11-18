---
name: sheet-fenwick-tree
title: 'Fenwick Tree (Prefix Sums With Updates)'
tags: [dsa-sheet, design, range-structures]
difficulty: Advanced
theory: query-update-and-set
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

`nums` is a list of numbers. Operations: `"set i v"` changes `nums[i]` to `v`; `"sum l r"` asks for the **sum of `nums[l..r]`** (both ends included). Return the results of all `sum` operations.

For `nums = [1, 2, 3, 4]` and `["sum 0 3", "set 1 10", "sum 0 2", "sum 1 1"]` the answer is `[10, 14, 10]`.

The starter code adds up the range for each query. It is correct but too slow for big lists.

### Examples

**Example 1**

Input:

```python
run_fenwick([1, 2, 3, 4], ['sum 0 3', 'set 1 10', 'sum 0 2', 'sum 1 1'])
```

Output:

```text
[10, 14, 10]
```

**Example 2**

Input:

```python
run_fenwick([5], ['sum 0 0', 'set 0 -5', 'sum 0 0'])
```

Output:

```text
[5, -5]
```

### Constraints

- `1 <= len(nums) <= 100000`
- `0 <= len(ops) <= 100000`
- `-1000 <= value <= 1000`

## Explanation

`add` and `prefix` walk the blocks with `i & -i`. `values` remembers the current numbers so `set` can compute the difference.

### Complexity

- Time: O(n + q log n). Building takes `n` updates of `log n`; each of the `q` operations touches `log n` cells.
- Space: O(n). The tree and the copy of the values.
