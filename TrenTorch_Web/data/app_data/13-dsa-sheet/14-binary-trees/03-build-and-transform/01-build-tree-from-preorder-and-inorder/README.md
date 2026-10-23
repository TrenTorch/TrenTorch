---
name: sheet-build-tree-from-preorder-and-inorder
title: 'Build a Tree From Preorder and Inorder'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
---

## Statement

You are given the **preorder** and the **inorder** traversal of a binary tree with **different values**. Rebuild the tree and return its root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `preorder = [3, 9, 20, 15, 7]` and `inorder = [9, 3, 15, 20, 7]` the answer is `[3, 9, 20, None, None, 15, 7]`.

### Examples

**Example 1**

Input:

```python
build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
```

Output:

```text
[3, 9, 20, None, None, 15, 7]
```

**Example 2**

Input:

```python
build_tree([1], [1])
```

Output:

```text
[1]
```

### Constraints

- `0 <= number of nodes <= 20000`
- The tree is not deeper than 800 levels.
- All values are different.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

**Preorder** starts with the root. **Inorder** puts the root with everything on the left in front of it and everything on the right behind. So:

1. The first value of `preorder` is the root.
2. Find that value in `inorder`; the values **before** it are the left subtree, the values after it are the right subtree. The _number_ of left values tells how many of the next preorder values belong to the left subtree.
3. Recurse on the two parts.

Searching the root in `inorder` each time costs `O(n)`, giving `O(n²)` in total for a thin tree. Precompute a dictionary `value -> index in inorder` for `O(1)` lookups, so the whole build is `O(n)`.

## Explanation

`pos` maps each value to its inorder index. `build(lo, hi)` builds the tree for the inorder range `[lo, hi)` and consumes preorder values left to right with an iterator, because preorder visits the root, then the whole left subtree, then the right.
