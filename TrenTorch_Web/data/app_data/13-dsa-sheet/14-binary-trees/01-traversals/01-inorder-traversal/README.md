---
name: sheet-inorder-traversal
title: 'Inorder Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Beginner
---

## Statement

Return the values of the tree in **inorder**: visit the left subtree, then the node itself, then the right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, None, 2, 3]` the answer is `[1, 3, 2]`.

### Examples

**Example 1**

Input:

```python
inorder_traversal(root)  # root = [1, None, 2, 3]
```

Output:

```text
[1, 3, 2]
```

**Example 2**

Input:

```python
inorder_traversal(root)  # root = []
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **traversal** visits every node once. For **inorder**, the recursion is three lines: inorder of the left subtree, the node's value, inorder of the right subtree. (For a binary _search_ tree, inorder gives the values in sorted order.)

The recursive version is the clearest. The **iterative** version replaces the call stack with your own stack: go as far **left** as you can, pushing every node on the way; then pop a node, record its value, and move to its **right** child. Repeat until the stack is empty and there is no current node. It uses `O(h)` memory, where `h` is the tree height.

## Explanation

`stack` holds the ancestors still waiting for their turn. When no more left child exists, the top of the stack is the next node in inorder.
