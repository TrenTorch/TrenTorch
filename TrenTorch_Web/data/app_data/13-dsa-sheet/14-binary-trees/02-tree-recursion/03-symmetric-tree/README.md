---
name: sheet-symmetric-tree
title: 'Symmetric Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
---

## Statement

Return `True` if the tree is **symmetric**: its left subtree is the mirror image of its right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 2, 3, 4, 4, 3]` the answer is `True`; for `[1, 2, 2, None, 3, None, 3]` it is `False`.

### Examples

**Example 1**

Input:

```python
is_symmetric(root)  # root = [1, 2, 2, 3, 4, 4, 3]
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_symmetric(root)  # root = [1, 2, 2, None, 3, None, 3]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Compare **two trees at once**. Two trees `a` and `b` are mirror images when: both are empty, or both exist with equal values and **`a.left` mirrors `b.right`** and **`a.right` mirrors `b.left`** (the cross comparison is the mirror).

So write a helper `mirror(a, b)` and call it on the left and right subtrees of the root. Recursion handles the rest. `O(n)`. Comparing two trees node by node, in lockstep, is a pattern you will reuse (same tree, subtree of another tree, merge two trees).

## Explanation

`mirror` returns `True` for two `None`s, `False` if only one is `None` or the values differ, and otherwise checks the crossed children.
