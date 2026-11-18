---
name: sheet-bst-to-greater-tree
title: 'BST to Greater Sum Tree'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
theory: greater-sum-tree-by-reverse-inorder
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Change the tree so that every node's value becomes **the original value plus the sum of all original values greater than it**. Return the root.

For `[4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8]` the answer is `[30, 36, 21, 36, 35, 26, 15, None, None, None, 33, None, None, None, 8]`.

### Examples

**Example 1**

Input:

```python
convert_bst(root)  # root = [4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8]
```

Output:

```text
[30, 36, 21, 36, 35, 26, 15, None, None, None, 33, None, None, None, 8]
```

**Example 2**

Input:

```python
convert_bst(root)  # root = [0, None, 1]
```

Output:

```text
[1, None, 1]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `0 <= val <= 10**4`

## Explanation

The traversal goes right first, so larger values are added to `total` before smaller ones. `node.val = total` after the addition includes the node's own old value.

### Complexity

- Time: O(n). A reverse in-order walk visits each node once while keeping a running sum.
- Space: O(h). The stack holds one path; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
