---
name: sheet-search-in-a-bst
title: 'Search in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Beginner
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **subtree** whose root has the value `val` (the node with all its descendants), or an empty tree if there is no such node.

For `[4, 2, 7, 1, 3]` and `val = 2` the answer is `[2, 1, 3]`.

### Examples

**Example 1**

Input:

```python
search_bst(root, 2)  # root = [4, 2, 7, 1, 3]
```

Output:

```text
[2, 1, 3]
```

**Example 2**

Input:

```python
search_bst(root, 5)  # root = [4, 2, 7, 1, 3]
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Searching follows one path from the root: if `val` is smaller than the current value go left, if larger go right, if equal you found it, and if you fall off the tree (`None`) it is not there. No recursion is needed: a simple loop with the current node is enough, with `O(h)` time and `O(1)` memory.

## Explanation

Each step discards one whole subtree. The loop ends at the matching node, or at `None`.
