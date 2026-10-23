---
name: sheet-bst-to-greater-tree
title: 'BST to Greater Sum Tree'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
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

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

The new value of a node is a **suffix sum** of the sorted values: the sum of itself and everything larger. So visit the nodes from the **largest to the smallest**, keeping a running total: that is a **reverse inorder** traversal (right, node, left). At each node, add its value to the total and write the total back into the node.

A single pass, `O(n)` time and `O(h)` memory.

## Explanation

The traversal goes right first, so larger values are added to `total` before smaller ones. `node.val = total` after the addition includes the node's own old value.
