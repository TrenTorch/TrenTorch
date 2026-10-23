---
name: sheet-balanced-binary-tree
title: 'Balanced Binary Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Intermediate
---

## Statement

A tree is **height-balanced** if, for **every node**, the heights of its left and right subtrees differ by **at most 1**. Return `True` if the tree is balanced.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `True`; for `[1, 2, 2, 3, 3, None, None, 4, 4]` it is `False`.

### Examples

**Example 1**

Input:

```python
is_balanced(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_balanced(root)  # root = [1, 2, 2, 3, 3, None, None, 4, 4]
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

The natural solution checks each node's balance using a `height` function that walks the whole subtree: that repeats work, `O(n²)` in a thin tree.

Do both in **one pass**: let the recursion return the height, or a **signal value** (`-1`) meaning "this subtree is already unbalanced". For a node: get the left and right results; if either is `-1`, or their difference is above 1, return `-1`; otherwise return `1 + max(left, right)`. The tree is balanced when the root's result is not `-1`.

This "return the answer plus the failure in one number" trick makes it `O(n)`.

## Explanation

`check(node)` returns the height, or `-1` if any node below is unbalanced. The first `-1` bubbles up unchanged.
