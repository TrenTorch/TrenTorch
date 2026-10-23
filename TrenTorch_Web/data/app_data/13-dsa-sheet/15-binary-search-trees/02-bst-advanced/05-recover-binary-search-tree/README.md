---
name: sheet-recover-binary-search-tree
title: 'Recover a BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Advanced
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Exactly **two nodes** of a BST had their values **swapped by mistake**. Put the values back so that the tree is a valid BST again, without changing the shape, and return the root.

For `[3, 1, 4, None, None, 2]` the answer is `[2, 1, 4, None, None, 3]`.

### Examples

**Example 1**

Input:

```python
recover_tree(root)  # root = [1, 3, None, None, 2]
```

Output:

```text
[3, 1, None, None, 2]
```

**Example 2**

Input:

```python
recover_tree(root)  # root = [3, 1, 4, None, None, 2]
```

Output:

```text
[2, 1, 4, None, None, 3]
```

### Constraints

- `2 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- Exactly two values were swapped.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

The inorder list of a correct BST is increasing. After swapping two values, the inorder list has one or two **descents** (places where a value is bigger than the next one):

- If the swapped nodes are neighbours in inorder, there is **one** descent `(a, b)`; swap those two.
- Otherwise there are **two** descents `(a, b)` and `(c, d)`; the wrong nodes are the **first** of the first descent (`a`) and the **second** of the last descent (`d`).

Walk the tree inorder, remember the previous node, and record `first` (the earliest `prev` that is bigger than its successor) and `second` (the latest successor of a descent). Swap their values at the end. `O(n)` time.

## Explanation

`first` is set only the first time a descent is found; `second` is updated at every descent, so the second descent overrides the first descent's partner.
