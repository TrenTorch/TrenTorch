---
name: sheet-recover-binary-search-tree
title: 'Recover a BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Advanced
theory: two-values-swapped-by-mistake
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Exactly **two nodes** of a BST had their values **swapped by mistake**. Put the values back so that the tree is a valid BST again, without changing the shape, and return the root.

For `[3, 1, 4, None, None, 2]` the answer is `[2, 1, 4, None, None, 3]`.

### Examples

**Example 1**

Input:

```python
recover_tree(root)  # root = [1, 3, None, None, 2]
```

Output:

```text
[3, 1, None, None, 2]
```

**Example 2**

Input:

```python
recover_tree(root)  # root = [3, 1, 4, None, None, 2]
```

Output:

```text
[2, 1, 4, None, None, 3]
```

### Constraints

- `2 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- Exactly two values were swapped.

## Explanation

`first` is set only the first time a descent is found; `second` is updated at every descent, so the second descent overrides the first descent's partner.

### Complexity

- Time: O(n). One in-order walk finds the two out-of-order nodes.
- Space: O(h). The stack holds one path; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
