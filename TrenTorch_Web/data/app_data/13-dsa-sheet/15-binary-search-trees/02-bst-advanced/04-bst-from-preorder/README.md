---
name: sheet-bst-from-preorder
title: 'Build a BST from Preorder'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Advanced
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

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Inserting the values one at a time in preorder works, but each insertion walks down from the root: `O(n·h)`. In a thin tree that is `O(n²)`.

Better: build in **one pass with bounds**. The first value is the root. The next values that are smaller than the root form the left subtree, then the larger ones form the right subtree. Recursively: `build(bound)` takes values from the front of the list while they are **smaller than `bound`**; the left subtree is built with the node's value as the new bound, and the right subtree with the old bound. Keep a shared index into the list so that each value is consumed once. `O(n)`.

## Explanation

`index` moves forward through the preorder list. A value larger than the bound belongs to an ancestor's right subtree, so the current call stops and returns.
