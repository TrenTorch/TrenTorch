---
name: sheet-validate-binary-search-tree
title: 'Validate a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

Return `True` if the tree is a **valid BST**: for every node, all values in the left subtree are **strictly smaller** and all values in the right subtree are **strictly larger**. This must hold for the **whole subtree**, not only for the direct children.

For `[2, 1, 3]` the answer is `True`; for `[5, 1, 4, None, None, 3, 6]` it is `False` (the `3` sits to the right of `5`).

### Examples

**Example 1**

Input:

```python
is_valid_bst(root)  # root = [2, 1, 3]
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_valid_bst(root)  # root = [5, 1, 4, None, None, 3, 6]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

The tempting check, "left child < node < right child", is **not enough**: in `[5, 1, 4, None, None, 3, 6]` every node satisfies it with its own children, but `3` is in the right subtree of `5` and is smaller than `5`.

Pass **bounds** down the recursion: every value in a subtree must lie in an open interval `(low, high)`. The root has `(-inf, inf)`. Going left, the upper bound becomes the node's value; going right, the lower bound becomes the node's value. A node outside its interval makes the tree invalid.

The alternative is the **inorder** traversal: a tree is a BST exactly when its inorder values are strictly increasing. `O(n)`.

## Explanation

`check(node, low, high)` verifies one node against its allowed interval and passes tighter intervals to the children.
