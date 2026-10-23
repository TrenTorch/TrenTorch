---
name: sheet-flatten-binary-tree
title: 'Flatten a Binary Tree'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
---

## Statement

Rewire the tree **in place** so that it becomes a chain that only uses `right` pointers (`left` is `None` everywhere) and lists the nodes in **preorder**. Return the root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 5, 3, 4, None, 6]` the answer is `[1, None, 2, None, 3, None, 4, None, 5, None, 6]`.

### Examples

**Example 1**

Input:

```python
flatten_tree(root)  # root = [1, 2, 5, 3, 4, None, 6]
```

Output:

```text
[1, None, 2, None, 3, None, 4, None, 5, None, 6]
```

**Example 2**

Input:

```python
flatten_tree(root)  # root = []
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Flattening in preorder means: node, then the flattened left subtree, then the flattened right subtree. Do it in place by **connecting the end of the left subtree to the start of the right subtree**:

1. For a node with a left child, find the **rightmost node of the left subtree** (follow `right` pointers: it is the last node of the left chain in preorder).
2. Point that node's `right` at the node's current right child.
3. Move the left subtree to the right (`node.right = node.left`, `node.left = None`).
4. Continue with `node.right`.

This is the **Morris**-style idea of threading a tree using the rightmost node. It is `O(n)` time and `O(1)` extra memory.

## Explanation

The inner loop finds the tail of the left subtree. Linking it to the old right child keeps all nodes reachable after the left subtree is moved.
