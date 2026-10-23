---
name: sheet-kth-smallest-in-a-bst
title: 'Kth Smallest in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **`k`-th smallest value** (counting from 1) in the BST.

For `[3, 1, 4, None, 2]` and `k = 1` the answer is `1`; for `[5, 3, 6, 2, 4, None, None, 1]` and `k = 3` it is `3`.

### Examples

**Example 1**

Input:

```python
kth_smallest_bst(root, 1)  # root = [3, 1, 4, None, 2]
```

Output:

```text
1
```

**Example 2**

Input:

```python
kth_smallest_bst(root, 3)  # root = [5, 3, 6, 2, 4, None, None, 1]
```

Output:

```text
3
```

### Constraints

- `1 <= k <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Since inorder gives the values in increasing order, the `k`-th smallest is simply the `k`-th value visited by an inorder traversal. Do the traversal **iteratively** and **stop after `k` visits**: you never look at the rest of the tree. `O(h + k)`.

(If you will ask this question many times on a tree that changes, store the **size of each subtree** in the nodes; then each query is `O(h)` by comparing `k` with the left subtree's size.)

## Explanation

The stack-based inorder loop counts nodes as they are visited; the `k`-th one is returned immediately.
