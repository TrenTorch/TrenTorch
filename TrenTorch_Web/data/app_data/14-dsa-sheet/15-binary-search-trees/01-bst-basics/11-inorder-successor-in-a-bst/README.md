---
name: sheet-inorder-successor-in-a-bst
title: 'Inorder Successor'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: inorder-successor
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

The **inorder successor** of the value `p` is the node with the **smallest value larger than `p`**. Return that node, or `None` if there is none. The value `p` is in the tree. The tests check the value of the node you return.

For `[2, 1, 3]` and `p = 1` the answer is the node `2`; for `p = 3` it is `None`.

### Examples

**Example 1**

Input:

```python
inorder_successor(root, 1)  # root = [2, 1, 3]
```

Output:

```text
2
```

**Example 2**

Input:

```python
inorder_successor(root, 3)  # root = [2, 1, 3]
```

Output:

```text
None
```

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `p` is a value in the tree.

## Explanation

`answer` holds the smallest node larger than `p` seen so far. Moving right means the current node is too small, so it is skipped.

### Complexity

- Time: O(h). One root-to-leaf walk remembering the last node that was larger.
- Space: O(1). One pointer; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
