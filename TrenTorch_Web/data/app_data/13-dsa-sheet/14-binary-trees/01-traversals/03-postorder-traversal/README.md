---
name: sheet-postorder-traversal
title: 'Postorder Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
---

## Statement

Return the values of the tree in **postorder**: visit the left subtree, then the right subtree, then the node itself.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, None, 2, 3]` the answer is `[3, 2, 1]`.

### Examples

**Example 1**

Input:

```python
postorder_traversal(root)  # root = [1, None, 2, 3]
```

Output:

```text
[3, 2, 1]
```

**Example 2**

Input:

```python
postorder_traversal(root)  # root = [1, 2, 3, 4, 5]
```

Output:

```text
[4, 5, 2, 3, 1]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

**Postorder** visits a node **after** its children. It is the order for deleting a tree, or for computing something that depends on both subtrees (the height, the size, the sum).

A short iterative trick: postorder is the **reverse** of "node, right, left". So run the preorder loop with the children pushed in the opposite order (left, then right), which visits node, right, left, and reverse the result at the end.

## Explanation

The loop produces node, right, left; reversing it gives left, right, node.
