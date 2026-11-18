---
name: sheet-segment-tree-minimum
title: 'Segment Tree (Range Minimum With Updates)'
tags: [dsa-sheet, design, range-structures]
difficulty: Advanced
theory: the-array-layout
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

**Example 2**

Input:

```python
run_segment_tree([7], ['min 0 0'])
```

Output:

```text
[7]
```

### Constraints

- `1 <= len(nums) <= 100000`
- `0 <= len(ops) <= 100000`
- `-1000 <= value <= 1000`

## Explanation

The array `tree` has `2n` entries; the loops climb one level per step, collecting the blocks that exactly cover the query range.

### Complexity

- Time: O(n + q log n). Building is one pass over the `n` nodes; each query or update touches `O(log n)` nodes.
- Space: O(n). The tree array of `2n` values.
