---
name: sheet-minimum-absolute-difference-in-a-bst
title: 'Minimum Difference in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: smallest-gap-between-values
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **smallest absolute difference** between the values of any two different nodes.

For `[4, 2, 6, 1, 3]` the answer is `1`.

### Examples

**Example 1**

Input:

```python
min_diff_bst(root)  # root = [4, 2, 6, 1, 3]
```

Output:

```text
1
```

**Example 2**

Input:

```python
min_diff_bst(root)  # root = [1, 0, 48, None, None, 12, 49]
```

Output:

```text
1
```

### Constraints

- `2 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Explanation

`prev` is the value visited just before the current node in inorder. Because the order is increasing, the difference is never negative.

### Complexity

- Time: O(n). An in-order walk visits values in increasing order, so the best pair is a neighbour pair.
- Space: O(h). The stack holds one path; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
