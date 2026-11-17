---
name: sheet-trim-a-bst
title: 'Trim a BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
theory: trimming-to-a-range
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Trim the tree so that **all remaining values are between `low` and `high`** (both included). Keep the **relative structure** of the remaining nodes: a kept node stays below the same kept ancestors. Return the (possibly new) root.

For `[3, 0, 4, None, 2, None, None, 1]`, `low = 1` and `high = 3` the answer is `[3, 2, None, 1]`.

### Examples

**Example 1**

Input:

```python
trim_bst(root, 1, 3)  # root = [3, 0, 4, None, 2, None, None, 1]
```

Output:

```text
[3, 2, None, 1]
```

**Example 2**

Input:

```python
trim_bst(root, 1, 2)  # root = [1, 0, 2]
```

Output:

```text
[1, None, 2]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Explanation

Each call returns the root of the trimmed subtree, so the parent just re-attaches whatever comes back.

### Complexity

- Time: O(n). Every node is visited at most once.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
