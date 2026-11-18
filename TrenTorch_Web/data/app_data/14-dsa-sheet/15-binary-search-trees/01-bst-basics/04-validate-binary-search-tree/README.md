---
name: sheet-validate-binary-search-tree
title: 'Validate a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: validating-with-ranges
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

Return `True` if the tree is a **valid BST**: for every node, all values in the left subtree are **strictly smaller** and all values in the right subtree are **strictly larger**. This must hold for the **whole subtree**, not only for the direct children.

For `[2, 1, 3]` the answer is `True`; for `[5, 1, 4, None, None, 3, 6]` it is `False` (the `3` sits to the right of `5`).

### Examples

**Example 1**

Input:

```python
is_valid_bst(root)  # root = [2, 1, 3]
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_valid_bst(root)  # root = [5, 1, 4, None, None, 3, 6]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Explanation

`check(node, low, high)` verifies one node against its allowed interval and passes tighter intervals to the children.

### Complexity

- Time: O(n). Every node is checked once against the open interval its position allows.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
