---
name: sheet-bst-from-preorder
title: 'Build a BST from Preorder'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Advanced
theory: building-from-a-preorder-list
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

You are given the **preorder** traversal of a BST (root, left subtree, right subtree) with different values. Rebuild the tree and return its root.

For `[8, 5, 1, 7, 10, 12]` the answer is `[8, 5, 10, 1, 7, None, 12]`.

### Examples

**Example 1**

Input:

```python
bst_from_preorder(preorder)  # preorder = [8, 5, 1, 7, 10, 12]
```

Output:

```text
[8, 5, 10, 1, 7, None, 12]
```

**Example 2**

Input:

```python
bst_from_preorder(preorder)  # preorder = [1, 3]
```

Output:

```text
[1, None, 3]
```

### Constraints

- `0 <= len(preorder) <= 100000`
- The tree is not deeper than 800 levels.
- All values are different.

## Explanation

`index` moves forward through the preorder list. A value larger than the bound belongs to an ancestor's right subtree, so the current call stops and returns.

### Complexity

- Time: O(n). Each value is consumed once; the upper bound tells where a subtree ends.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
