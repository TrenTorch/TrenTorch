---
name: sheet-build-tree-from-preorder-and-inorder
title: 'Build a Tree From Preorder and Inorder'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
theory: building-from-preorder-and-inorder
---

## Statement

You are given the **preorder** and the **inorder** traversal of a binary tree with **different values**. Rebuild the tree and return its root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `preorder = [3, 9, 20, 15, 7]` and `inorder = [9, 3, 15, 20, 7]` the answer is `[3, 9, 20, None, None, 15, 7]`.

### Examples

**Example 1**

Input:

```python
build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
```

Output:

```text
[3, 9, 20, None, None, 15, 7]
```

**Example 2**

Input:

```python
build_tree([1], [1])
```

Output:

```text
[1]
```

### Constraints

- `0 <= number of nodes <= 20000`
- The tree is not deeper than 800 levels.
- All values are different.

## Explanation

`pos` maps each value to its inorder index. `build(lo, hi)` builds the tree for the inorder range `[lo, hi)` and consumes preorder values left to right with an iterator, because preorder visits the root, then the whole left subtree, then the right.

### Complexity

- Time: O(n). A table of inorder positions gives each root split in O(1), so every node is created once.
- Space: O(n). The position table (plus `O(h)` recursion).
