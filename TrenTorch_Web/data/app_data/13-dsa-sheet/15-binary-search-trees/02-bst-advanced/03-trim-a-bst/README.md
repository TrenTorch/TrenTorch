---
name: sheet-trim-a-bst
title: 'Trim a BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Trim the tree so that **all remaining values are between `low` and `high`** (both included). Keep the **relative structure** of the remaining nodes: a kept node stays below the same kept ancestors. Return the (possibly new) root.

For `[3, 0, 4, None, 2, None, None, 1]`, `low = 1` and `high = 3` the answer is `[3, 2, None, 1]`.

### Examples

**Example 1**

Input:

```python
trim_bst(root, 1, 3)  # root = [3, 0, 4, None, 2, None, None, 1]
```

Output:

```text
[3, 2, None, 1]
```

**Example 2**

Input:

```python
trim_bst(root, 1, 2)  # root = [1, 0, 2]
```

Output:

```text
[1, None, 2]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Use the order again to decide quickly what to drop:

- If `node.val < low`: the node and its **whole left subtree** are too small, so the answer is the trimmed **right** subtree.
- If `node.val > high`: the node and its whole right subtree are too large, so the answer is the trimmed **left** subtree.
- Otherwise keep the node and trim both children.

A recursive function that returns the trimmed subtree for each call does it in `O(n)`.

## Explanation

Each call returns the root of the trimmed subtree, so the parent just re-attaches whatever comes back.
