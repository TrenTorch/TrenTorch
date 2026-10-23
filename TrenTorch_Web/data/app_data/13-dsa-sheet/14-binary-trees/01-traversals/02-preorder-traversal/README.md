---
name: sheet-preorder-traversal
title: 'Preorder Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Beginner
---

## Statement

Return the values of the tree in **preorder**: visit the node itself, then the left subtree, then the right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, None, 2, 3]` the answer is `[1, 2, 3]`.

### Examples

**Example 1**

Input:

```python
preorder_traversal(root)  # root = [1, None, 2, 3]
```

Output:

```text
[1, 2, 3]
```

**Example 2**

Input:

```python
preorder_traversal(root)  # root = [1, 2, 3, 4, 5]
```

Output:

```text
[1, 2, 4, 5, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

**Preorder** visits a node **before** its children. It is the order in which you would copy a tree, or print a folder with its contents indented below it.

Iteratively, use a stack that holds the nodes still to be visited. Pop a node, record its value, then push its **right** child first and its **left** child second, so that the left child is popped next. Pushing right before left is the detail that keeps the order correct.

## Explanation

The stack always has the next node on top. Because a stack is last in, first out, pushing right then left makes left come out first.
