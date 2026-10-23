---
name: sheet-maximum-width-of-binary-tree
title: 'Maximum Width of a Binary Tree'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
---

## Statement

The **width** of a level is the distance between its leftmost and rightmost non-empty nodes, **counting the empty places between them** as if the tree were complete (the number of positions from the first to the last node, both included). Return the **largest width** among all levels.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 3, 2, 5, 3, None, 9]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
width_of_tree(root)  # root = [1, 3, 2, 5, 3, None, 9]
```

Output:

```text
4
```

**Example 2**

Input:

```python
width_of_tree(root)  # root = [1, 3, 2, 5]
```

Output:

```text
2
```

### Constraints

- `0 <= number of nodes <= 3000`
- The tree is not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Number the nodes like in a **heap**: the root is `0`; the children of the node numbered `i` are `2i + 1` and `2i + 2`. A level's width is then `last_index - first_index + 1`, where the indices are those of the leftmost and rightmost nodes of the level. Run a BFS and keep the index with each node.

Indices grow quickly in a thin tree (up to `2^depth`); Python integers do not overflow, so no special care is needed. In other languages you subtract the first index of the level before computing the children.

## Explanation

The queue stores `(node, index)`. At the start of each level the first index is read, and the width is the last index minus it plus 1.
