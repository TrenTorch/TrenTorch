---
name: sheet-inorder-successor-in-a-bst
title: 'Inorder Successor'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
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

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

You do not need parent pointers. Search for `p` from the root, and remember the **last node where you turned left**: that node is bigger than `p` and is a candidate for the successor. Each time `node.val > p`, record it and go left (to look for a smaller value still above `p`); otherwise go right.

When the walk ends, the recorded candidate is the smallest value above `p` that you passed. If you never turned left, `p` is the largest value and there is no successor. `O(h)`.

## Explanation

`answer` holds the smallest node larger than `p` seen so far. Moving right means the current node is too small, so it is skipped.
