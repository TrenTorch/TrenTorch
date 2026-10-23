---
name: sheet-closest-value-in-a-bst
title: 'Closest Value in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the value in the tree that is **closest to `target`**. If two values are equally close, return the **smaller** one.

For `[4, 2, 5, 1, 3]` and `target = 3` the answer is `3`; for `[4, 2, 5, 1, 3]` and `target = 6` it is `5`.

### Examples

**Example 1**

Input:

```python
closest_value(root, 3)  # root = [4, 2, 5, 1, 3]
```

Output:

```text
3
```

**Example 2**

Input:

```python
closest_value(root, 6)  # root = [4, 2, 5, 1, 3]
```

Output:

```text
5
```

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `-10**9 <= target <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Walk down as if searching for `target`. At each node compare its distance to `target` with the best so far (breaking ties toward the smaller value), then go left if `target` is smaller than the node and right otherwise. The closest value is always on this path: values off the path are further away than some node on the path.

`O(h)` time, `O(1)` memory.

## Explanation

The key `(abs(v - target), v)` makes the tie-break automatic: the smaller distance wins, and for equal distances the smaller value.
