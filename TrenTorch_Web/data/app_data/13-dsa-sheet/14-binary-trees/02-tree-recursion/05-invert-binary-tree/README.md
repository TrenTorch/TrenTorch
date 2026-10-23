---
name: sheet-invert-binary-tree
title: 'Invert a Binary Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
---

## Statement

**Invert** the tree: swap the left and right child of **every** node, and return the root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[4, 2, 7, 1, 3, 6, 9]` the answer is `[4, 7, 2, 9, 6, 3, 1]`.

### Examples

**Example 1**

Input:

```python
invert_tree(root)  # root = [4, 2, 7, 1, 3, 6, 9]
```

Output:

```text
[4, 7, 2, 9, 6, 3, 1]
```

**Example 2**

Input:

```python
invert_tree(root)  # root = [2, 1, 3]
```

Output:

```text
[2, 3, 1]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Invert the left subtree, invert the right subtree, then swap them: `root.left, root.right = invert(root.right), invert(root.left)`. The base case is the empty tree. `O(n)`.

(It is also solvable with a queue: visit every node and swap its children, in any order.) This question became a famous interview joke, but it is the cleanest example of a **tree transformation**: change the node, recurse on the children.

## Explanation

The right-hand side is evaluated first, so both recursive calls see the original children before the assignment swaps them.
