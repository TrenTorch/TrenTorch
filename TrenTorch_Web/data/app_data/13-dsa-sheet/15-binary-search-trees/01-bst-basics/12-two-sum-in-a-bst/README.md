---
name: sheet-two-sum-in-a-bst
title: 'Two Sum in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return `True` if there are **two different nodes** whose values add up to `k`.

For `[5, 3, 6, 2, 4, None, 7]` and `k = 9` the answer is `True` (`3 + 6`); for `k = 28` it is `False`.

### Examples

**Example 1**

Input:

```python
find_target(root, 9)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
True
```

**Example 2**

Input:

```python
find_target(root, 28)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `-10**9 <= k <= 2 * 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Two ways. (1) Use a set while traversing: for each value `v`, check whether `k - v` was seen. `O(n)` memory. (2) Use the BST property: the inorder traversal is a **sorted list**, so you can apply the sorted two-pointer technique to it: one pointer at the smallest, one at the largest, move them toward each other depending on the sum.

Write the inorder list first (simple), then the two pointers. The set approach is shorter, the sorted approach shows why the BST matters.

## Explanation

The inorder list is increasing. If the pair sum is too small the left pointer moves right; if too big the right pointer moves left. The pointers never cross a valid pair.
