---
name: sheet-lowest-common-ancestor-of-a-bst
title: 'Lowest Common Ancestor in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **lowest common ancestor** of the values `p` and `q`: the lowest node that has both in its subtree (a node counts as being in its own subtree). Both values are in the tree. The tests check the value of the node you return.

For `[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]`, `p = 2` and `q = 8` the answer is the node `6`; for `p = 2` and `q = 4` it is the node `2`.

### Examples

**Example 1**

Input:

```python
lca_bst(root, 2, 8)  # root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
```

Output:

```text
6
```

**Example 2**

Input:

```python
lca_bst(root, 2, 4)  # root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
```

Output:

```text
2
```

### Constraints

- `2 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `p` and `q` are values in the tree.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

In a general tree the LCA needs a search of both subtrees. A BST tells you where each value is without searching. Stand at the root: if **both** `p` and `q` are smaller than the node's value, the LCA is in the left subtree; if **both** are larger, it is in the right subtree; otherwise the values are on different sides (or one of them is the node itself), and this node is the split point: the answer.

A simple loop, `O(h)` time and `O(1)` memory.

## Explanation

The loop descends while both values are on the same side. The first node where they split (or equal one of them) is returned.
