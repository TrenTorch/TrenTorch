---
name: sheet-level-order-traversal
title: 'Level Order Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
theory: level-order-row-by-row
---

## Statement

Return the values **level by level**, from the top, and left to right inside each level. The result is a list of lists, one per level.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `[[3], [9, 20], [15, 7]]`.

### Examples

**Example 1**

Input:

```python
level_order(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
[[3], [9, 20], [15, 7]]
```

**Example 2**

Input:

```python
level_order(root)  # root = [1]
```

Output:

```text
[[1]]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Explanation

`for _ in range(len(queue))` handles exactly one level, because the children pushed meanwhile are added after the original size was read.

### Complexity

- Time: O(n). Each node enters and leaves the queue once.
- Space: O(w). `w` is the widest level, at most `n / 2` (the result is output).
