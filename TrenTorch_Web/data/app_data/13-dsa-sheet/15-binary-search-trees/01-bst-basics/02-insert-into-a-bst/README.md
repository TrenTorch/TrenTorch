---
name: sheet-insert-into-a-bst
title: 'Insert into a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Beginner
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Insert the value `val` (it is not in the tree yet) as a **new leaf** so that the tree is still a BST, and return the root. Walk down as in a search, and attach the new node where the search falls off the tree.

For `[4, 2, 7, 1, 3]` and `val = 5` the answer is `[4, 2, 7, 1, 3, 5]`.

### Examples

**Example 1**

Input:

```python
insert_into_bst(root, 5)  # root = [4, 2, 7, 1, 3]
```

Output:

```text
[4, 2, 7, 1, 3, 5]
```

**Explanation:** 5 is larger than 4, so go right to 7. 5 is smaller than 7 and 7 has no left child, so 5 is attached there. In level order the new 5 comes after 3.

**Example 2**

Input:

```python
insert_into_bst(root, 5)  # root = []
```

Output:

```text
[5]
```

**Explanation:** The tree is empty, so the new node becomes the root: [5].

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `val` is not already in the tree.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

Insertion is a search that ends at an empty place: the new node always becomes a **leaf**. Walk down with the same left/right rule, remembering the parent. When you reach `None`, attach the new node to the parent's left or right, depending on which side you came from.

An empty tree is the special case: the new node is the root. A recursive version is shorter: `insert(None, val)` returns a new node, and `insert(node, val)` sets `node.left` or `node.right` to the result of inserting below, then returns `node`.

## Explanation

The loop keeps `parent` one step behind `node`. When `node` is `None` the new leaf is attached to the correct side of `parent`.

### Complexity

- Time: O(n) n nodes.
- Extra space: O(1) constant extra space.
- The brute force takes O(n) conversion and recursion.
