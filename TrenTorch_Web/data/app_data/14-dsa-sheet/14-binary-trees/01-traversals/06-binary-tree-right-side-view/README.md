---
name: sheet-binary-tree-right-side-view
title: 'Right Side View'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
theory: the-right-side-view
---

## Statement

Imagine standing on the **right side** of the tree. Return the value of the node you can see at each level, from top to bottom (the rightmost node of each level).

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 3, None, 5, None, 4]` the answer is `[1, 3, 4]`.

### Examples

**Example 1**

Input:

```python
right_side_view(root)  # root = [1, 2, 3, None, 5, None, 4]
```

Output:

```text
[1, 3, 4]
```

**Example 2**

Input:

```python
right_side_view(root)  # root = [1, None, 3]
```

Output:

```text
[1, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Explanation

The inner loop processes one level; `level_last` ends up holding the value of the last node popped from that level.

### Complexity

- Time: O(n). Each node enters and leaves the queue once.
- Space: O(w). `w` is the widest level, at most `n / 2`.
