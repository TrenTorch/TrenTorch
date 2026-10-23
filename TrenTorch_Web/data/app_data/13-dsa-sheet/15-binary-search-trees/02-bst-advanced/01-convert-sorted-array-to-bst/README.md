---
name: sheet-convert-sorted-array-to-bst
title: 'Sorted Array to a Balanced BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

`nums` is sorted in increasing order with different values. Build a **height-balanced BST** (the heights of the two subtrees of every node differ by at most 1) containing all the values. To make the answer unique, always take the **middle element, and the lower middle when the count is even** (index `(lo + hi) // 2`) as the root of a range.

For `[-10, -3, 0, 5, 9]` the answer is `[0, -10, 5, None, -3, None, 9]`.

### Examples

**Example 1**

Input:

```python
sorted_array_to_bst(nums)  # nums = [-10, -3, 0, 5, 9]
```

Output:

```text
[0, -10, 5, None, -3, None, 9]
```

**Example 2**

Input:

```python
sorted_array_to_bst(nums)  # nums = [1, 3]
```

Output:

```text
[1, None, 3]
```

### Constraints

- `0 <= len(nums) <= 100000`
- `nums` is strictly increasing.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

To keep the tree balanced, make the **middle** element the root: half of the remaining values are smaller (they go left) and half larger (they go right). Then do the same for each half, recursively. The recursion halves the range each time, so the depth is `log₂ n`.

Pass index ranges `(lo, hi)` instead of slicing the list; slices copy and would make it `O(n log n)`. Total `O(n)`.

## Explanation

`build(lo, hi)` makes the node for the middle index and builds the two halves around it. An empty range gives `None`.
