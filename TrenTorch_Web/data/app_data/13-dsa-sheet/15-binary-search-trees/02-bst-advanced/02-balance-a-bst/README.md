---
name: sheet-balance-a-bst
title: 'Balance a BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

The BST may be badly unbalanced (even a chain). Rebuild it as a **height-balanced BST** with the same values. As in the previous question, use the **lower middle** of each range as its root, so the answer is unique.

For `[1, None, 2, None, 3, None, 4]` the answer is `[2, 1, 3, None, None, None, 4]`.

### Examples

**Example 1**

Input:

```python
balance_bst(root)  # root = [1, None, 2, None, 3, None, 4]
```

Output:

```text
[2, 1, 3, None, None, None, 4]
```

**Example 2**

Input:

```python
balance_bst(root)  # root = [2, 1, 3]
```

Output:

```text
[2, 1, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

A tree is only as fast as it is shallow. To rebalance, do two steps you already know: (1) the **inorder** traversal turns the BST into a **sorted list**; (2) build a balanced BST from a sorted list by taking the **middle** as the root and recursing on the halves.

There are in-place rotations (AVL and red-black trees do small rotations after each insert), but rebuilding is simple and `O(n)`.

## Explanation

The first loop collects the values in sorted order; `build` makes the balanced tree from index ranges.
