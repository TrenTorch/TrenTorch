---
name: sheet-floor-and-ceil-in-a-bst
title: 'Floor and Ceil in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

For a number `x`, the **floor** is the largest value in the tree that is `<= x` and the **ceil** is the smallest value that is `>= x`. Return `[floor, ceil]`, using `-1` where there is none. All values in the tree are non-negative.

For `[8, 4, 12, 2, 6, 10, 14]` and `x = 5` the answer is `[4, 6]`.

### Examples

**Example 1**

Input:

```python
floor_and_ceil_bst(root, 5)  # root = [8, 4, 12, 2, 6, 10, 14]
```

Output:

```text
[4, 6]
```

**Example 2**

Input:

```python
floor_and_ceil_bst(root, 1)  # root = [8, 4, 12, 2, 6, 10, 14]
```

Output:

```text
[-1, 2]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `0 <= val, x <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Walk down as in a search for `x`, and remember the best candidates seen on the way:

- If `node.val == x`, both the floor and the ceil are `x`.
- If `node.val < x`, this node is a floor candidate (record it), and a bigger floor can only be in the **right** subtree.
- If `node.val > x`, this node is a ceil candidate, and a smaller ceil can only be in the **left** subtree.

The last recorded floor and ceil are the answer. One path, `O(h)`.

## Explanation

`floor` and `ceil` keep the closest values found so far on each side of `x` while the walk narrows the interval.
