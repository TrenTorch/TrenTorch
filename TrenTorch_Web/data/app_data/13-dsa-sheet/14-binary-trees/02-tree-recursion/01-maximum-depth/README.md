---
name: sheet-maximum-depth
title: 'Maximum Depth'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
---

## Statement

Return the **depth** (number of levels) of the tree: the number of nodes on the longest path from the root down to a leaf. An empty tree has depth `0`.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
max_depth(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_depth(root)  # root = [1, None, 2]
```

Output:

```text
2
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Trust the recursion. The depth of a tree is `1 +` the larger of the depths of its two subtrees, and the depth of an empty tree is `0`. That is the whole algorithm:

`depth(node) = 0 if node is None else 1 + max(depth(node.left), depth(node.right))`

Always ask the three recursion questions for a tree: what is the **base case** (an empty tree), what do I **ask the children**, and how do I **combine** their answers. Time `O(n)`; memory `O(h)` for the recursion stack.

## Explanation

The base case `None` returns 0. Each node adds 1 to the better of its two subtrees.
