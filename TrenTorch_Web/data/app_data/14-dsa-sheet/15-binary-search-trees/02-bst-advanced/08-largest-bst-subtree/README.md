---
name: sheet-largest-bst-subtree
title: 'Largest BST Inside a Tree'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Mastery
theory: largest-bst-inside-a-tree
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

This tree is **not necessarily a BST**. Return the number of nodes in the **largest subtree** (a node together with all its descendants) that is a valid BST (left values strictly smaller, right values strictly larger).

For `[10, 5, 15, 1, 8, None, 7]` the answer is `3` (the subtree rooted at `5`).

### Examples

**Example 1**

Input:

```python
largest_bst_subtree(root)  # root = [10, 5, 15, 1, 8, None, 7]
```

Output:

```text
3
```

**Example 2**

Input:

```python
largest_bst_subtree(root)  # root = [5, 4, 6, None, 3, 7, 8]
```

Output:

```text
1
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Explanation

`go(node)` returns `(size, low, high)` for a BST subtree, and `(0, +inf, -inf)` style markers (size 0 with an impossible range) when the subtree is not a BST or is empty. `best` records the largest size seen.

### Complexity

- Time: O(n). One post-order pass; each node combines the facts of its two subtrees in O(1).
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
