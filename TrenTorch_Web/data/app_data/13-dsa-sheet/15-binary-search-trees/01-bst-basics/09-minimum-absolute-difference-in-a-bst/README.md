---
name: sheet-minimum-absolute-difference-in-a-bst
title: 'Minimum Difference in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **smallest absolute difference** between the values of any two different nodes.

For `[4, 2, 6, 1, 3]` the answer is `1`.

### Examples

**Example 1**

Input:

```python
min_diff_bst(root)  # root = [4, 2, 6, 1, 3]
```

Output:

```text
1
```

**Example 2**

Input:

```python
min_diff_bst(root)  # root = [1, 0, 48, None, None, 12, 49]
```

Output:

```text
1
```

### Constraints

- `2 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

The closest two values are **neighbours in sorted order**. And the inorder traversal of a BST gives the sorted order for free. So walk the tree in inorder, keep the **previous value** visited, and take the minimum of `current - previous`. No sorting and no list of all values are needed. `O(n)` time, `O(h)` memory.

## Explanation

`prev` is the value visited just before the current node in inorder. Because the order is increasing, the difference is never negative.
