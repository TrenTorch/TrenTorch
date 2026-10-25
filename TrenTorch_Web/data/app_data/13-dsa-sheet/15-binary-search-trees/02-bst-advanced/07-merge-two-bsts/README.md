---
name: sheet-merge-two-bsts
title: 'Merge Two BSTs into a Sorted List'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Given two BSTs, return **all their values** in one list sorted in increasing order (a value that is in both trees appears twice).

For `[2, 1, 4]` and `[1, 0, 3]` the answer is `[0, 1, 1, 2, 3, 4]`.

### Examples

**Example 1**

Input:

```python
merge_bsts(root1, root2)  # root1 = [2, 1, 4], root2 = [1, 0, 3]
```

Output:

```text
[0, 1, 1, 2, 3, 4]
```

**Explanation:** Both trees produce values 0,1,2,3,4 with duplicate 1, sorted ascending.

**Example 2**

Input:

```python
merge_bsts(root1, root2)  # root1 = [], root2 = [5]
```

Output:

```text
[5]
```

**Explanation:** First tree empty, second contains 5, result is [5].

### Constraints

- `0 <= number of nodes <= 50000` in each tree
- Both trees are BSTs, not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

The inorder traversal of each tree is already sorted. So take the two sorted lists and **merge** them with two pointers, as in merge sort: `O(n + m)`, instead of collecting everything and sorting in `O((n + m) log(n + m))`.

The previous topics showed how to get the inorder list with an iterative traversal.

## Explanation

`inorder` returns the sorted values of one tree. The merge loop takes the smaller front value each time and appends the leftovers at the end.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line      | Variables                                                                |
| -------------------- | ------------------------------------------------------------------------ |
| `def inorder(root):` | `inorder = <function merge_bsts.<locals>.inorder at 0x000001F48329DFC0>` |
| `out = []`           | `a = [1, 2, 4], b = [0, 1, 3], out = []`                                 |
| `out.append(b[j])`   | `out = [0], i = 0, j = 0`                                                |
| `out.append(a[i])`   | `out = [0, 1], j = 1`                                                    |
| `j += 1`             | `out = [0, 1, 1], i = 1, j = 2`                                          |
| `i += 1`             | `out = [0, 1, 1, 2], i = 2`                                              |
| `j += 1`             | `out = [0, 1, 1, 2, 3], j = 3`                                           |
| `return`             | `returned = [0, 1, 1, 2, 3, 4]`                                          |
