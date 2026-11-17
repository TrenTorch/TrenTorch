---
name: sheet-delete-node-in-a-bst
title: 'Delete a Node from a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Advanced
theory: deleting-a-node
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Delete the node with the value `key` (if it exists) and return the root of the BST. When the node has **two children**, replace it by its **inorder successor** (the smallest value of its right subtree), so that the answer is unique.

For `[5, 3, 6, 2, 4, None, 7]` and `key = 3` the answer is `[5, 4, 6, 2, None, None, 7]`.

### Examples

**Example 1**

Input:

```python
delete_node(root, 3)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
[5, 4, 6, 2, None, None, 7]
```

**Example 2**

Input:

```python
delete_node(root, 0)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
[5, 3, 6, 2, 4, None, 7]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Explanation

The first two cases return the surviving child directly. In case 3 the successor's value replaces the deleted one, and the successor is removed from the right subtree with the same function.

### Complexity

- Time: O(h). One search down to the node and at most one more walk down for the successor.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
