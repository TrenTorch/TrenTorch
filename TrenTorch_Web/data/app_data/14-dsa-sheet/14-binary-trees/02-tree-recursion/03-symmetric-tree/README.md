---
name: sheet-symmetric-tree
title: 'Symmetric Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
theory: same-tree-and-symmetric-tree
---

## Statement

Return `True` if the tree is **symmetric**: its left subtree is the mirror image of its right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 2, 3, 4, 4, 3]` the answer is `True`; for `[1, 2, 2, None, 3, None, 3]` it is `False`.

### Examples

**Example 1**

Input:

```python
is_symmetric(root)  # root = [1, 2, 2, 3, 4, 4, 3]
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_symmetric(root)  # root = [1, 2, 2, None, 3, None, 3]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Explanation

`mirror` returns `True` for two `None`s, `False` if only one is `None` or the values differ, and otherwise checks the crossed children.

### Complexity

- Time: O(n). Every node is compared with its mirror once.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
