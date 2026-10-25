---
name: sheet-segment-tree-minimum
title: 'Segment Tree (Range Minimum With Updates)'
tags: [dsa-sheet, design, range-structures]
difficulty: Advanced
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

`nums` is a list of numbers. Operations: `"set i v"` changes `nums[i]` to `v`; `"min l r"` asks for the **smallest value in `nums[l..r]`** (both ends included). Return the results of all `min` operations.

For `nums = [5, 2, 8, 1]` and `["min 0 3", "set 3 9", "min 0 3", "min 2 3"]` the answer is `[1, 2, 8]`.

The starter code scans the range for each query. It is correct but too slow for big lists.

### Examples

**Example 1**

Input:

```python
run_segment_tree([5, 2, 8, 1], ['min 0 3', 'set 3 9', 'min 0 3', 'min 2 3'])
```

Output:

```text
[1, 2, 8]
```

**Explanation:** The minimum in the full array is 1, after setting index 3 to 9 the new minimum is 2, and the range [2,3] contains 8.

**Example 2**

Input:

```python
run_segment_tree([7], ['min 0 0'])
```

Output:

```text
[7]
```

**Explanation:** The array has one element 7, so the minimum over [0,0] is 7.

### Constraints

- `1 <= len(nums) <= 100000`
- `0 <= len(ops) <= 100000`
- `-1000 <= value <= 1000`

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

A minimum cannot be undone like a sum (there is no "subtract a value"), so a Fenwick tree does not fit. A **segment tree** stores the answer for **blocks of the array**: the leaves are the numbers, and every inner node holds the minimum of its two children, which covers the union of their ranges. The tree has height `log n`.

Bottom-up (iterative) version for size `n`: leaves live at `tree[n .. 2n-1]`, node `i` has children `2i` and `2i+1`. **Update** `i`: write the leaf at `n + i`, then go up (`i //= 2`) recomputing `tree[i] = min(tree[2i], tree[2i + 1])`. **Query** `[l, r]`: start with pointers `l += n`, `r += n + 1` and move up while `l < r`: if `l` is a right child take `tree[l]` and `l += 1`; if `r` is a right child, `r -= 1` and take `tree[r]`; then halve both. Each query and update is `O(log n)`.

## Explanation

The array `tree` has `2n` entries; the loops climb one level per step, collecting the blocks that exactly cover the query range.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                               | Variables                                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------- |
| `n = len(nums)`                               | `n = 4`                                                                               |
| `tree[i] = min(tree[2 * i], tree[2 * i + 1])` | `inf = inf, tree = [inf, 1, 2, 1, 5, 2, 8, 1], i = 1`                                 |
| `lo //= 2`                                    | `out = [], op = 'min 0 3', parts = ['min', '0', '3'], lo = 1, hi = 4, best = inf`     |
| `parts = op.split()`                          | `out = [1], op = 'set 3 9', parts = ['set', '3', '9'], hi = 1, best = 1`              |
| `for op in ops:`                              | `tree = [inf, 2, 2, 8, 5, 2, 8, 9], i = 0, op = 'min 0 3'`                            |
| `best = min(best, tree[lo])`                  | `parts = ['min', '0', '3'], hi = 2, best = 2`                                         |
| `best = inf`                                  | `out = [1, 2], op = 'min 2 3', parts = ['min', '2', '3'], lo = 6, hi = 8, best = inf` |
| `return`                                      | `returned = [1, 2, 8]`                                                                |
