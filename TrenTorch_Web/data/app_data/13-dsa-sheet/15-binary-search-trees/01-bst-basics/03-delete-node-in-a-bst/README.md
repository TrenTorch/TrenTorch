---
name: sheet-delete-node-in-a-bst
title: 'Delete a Node from a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Advanced
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Delete the node with the value `key` (if it exists) and return the root of the BST. When the node has **two children**, replace it by its **inorder successor** (the smallest value of its right subtree), so that the answer is unique.

For `[5, 3, 6, 2, 4, None, 7]` and `key = 3` the answer is `[5, 4, 6, 2, None, None, 7]`.

### Examples

**Example 1**

Input:

```python
delete_node(root, 3)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
[5, 4, 6, 2, None, None, 7]
```

**Example 2**

Input:

```python
delete_node(root, 0)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
[5, 3, 6, 2, 4, None, 7]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Find the node to delete with the usual search. Three cases:

1. **Leaf**: remove it (its parent now points to `None`).
2. **One child**: replace the node by that child.
3. **Two children**: you cannot simply remove it. Take the **inorder successor**: the smallest node in the right subtree (go right once, then left as far as possible). Copy its value into the node being deleted, then delete the successor from the right subtree (it has no left child, so it is case 1 or 2).

The recursive form returns the new root of each subtree: `node.left = delete(node.left, key)` and so on. Time `O(h)`.

## Explanation

The first two cases return the surviving child directly. In case 3 the successor's value replaces the deleted one, and the successor is removed from the right subtree with the same function.
