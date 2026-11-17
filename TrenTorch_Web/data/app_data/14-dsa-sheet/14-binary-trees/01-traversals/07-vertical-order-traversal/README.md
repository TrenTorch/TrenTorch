---
name: sheet-vertical-order-traversal
title: 'Vertical Order Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Advanced
theory: vertical-order-with-columns
---

## Statement

Give each node a **column**: the root is column `0`, a left child is one column to the **left** (column − 1) and a right child one column to the **right** (column + 1). Return the values grouped by column, from the leftmost column to the rightmost. Inside a column, go from **top to bottom**; nodes in the same row and column are ordered by **value** (smaller first).

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `[[9], [3, 15], [20], [7]]`.

### Examples

**Example 1**

Input:

```python
vertical_order(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
[[9], [3, 15], [20], [7]]
```

**Example 2**

Input:

```python
vertical_order(root)  # root = [1, 2, 3, 4, 5, 6, 7]
```

Output:

```text
[[4], [2], [1, 5, 6], [3], [7]]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Explanation

The key `(col, row, value)` encodes the whole required order. `groupby`-style grouping then splits by column.

### Complexity

- Time: O(n log n). One pass over the nodes, then each column is sorted by `(row, value)`.
- Space: O(n). The table of columns.
