---
name: sheet-largest-bst-subtree
title: 'Largest BST Inside a Tree'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Mastery
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

This tree is **not necessarily a BST**. Return the number of nodes in the **largest subtree** (a node together with all its descendants) that is a valid BST (left values strictly smaller, right values strictly larger).

For `[10, 5, 15, 1, 8, None, 7]` the answer is `3` (the subtree rooted at `5`).

### Examples

**Example 1**

Input:

```python
largest_bst_subtree(root)  # root = [10, 5, 15, 1, 8, None, 7]
```

Output:

```text
3
```

**Example 2**

Input:

```python
largest_bst_subtree(root)  # root = [5, 4, 6, None, 3, 7, 8]
```

Output:

```text
1
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Checking every subtree separately repeats the validation work: `O(n²)` in the worst case. Do it **bottom-up in one pass** (postorder). For each subtree return four facts: whether it is a BST, its **size**, its **minimum** and its **maximum**.

A node is the root of a BST when both children are BSTs, the left maximum is `<` the node's value, and the right minimum is `>` the node's value. Then its size is `left + right + 1`, its minimum is the left minimum (or the node), and its maximum is the right maximum (or the node). If it is not a BST, report an impossible range so no ancestor can use it, and keep the best size found so far.

`O(n)`: each node is looked at once.

## Explanation

`go(node)` returns `(size, low, high)` for a BST subtree, and `(0, +inf, -inf)` style markers (size 0 with an impossible range) when the subtree is not a BST or is empty. `best` records the largest size seen.
