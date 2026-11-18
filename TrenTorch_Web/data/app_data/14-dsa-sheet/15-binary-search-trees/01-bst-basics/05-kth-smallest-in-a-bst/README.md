---
name: sheet-kth-smallest-in-a-bst
title: 'Kth Smallest in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: kth-smallest-by-early-stop
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **`k`-th smallest value** (counting from 1) in the BST.

For `[3, 1, 4, None, 2]` and `k = 1` the answer is `1`; for `[5, 3, 6, 2, 4, None, None, 1]` and `k = 3` it is `3`.

### Examples

**Example 1**

Input:

```python
kth_smallest_bst(root, 1)  # root = [3, 1, 4, None, 2]
```

Output:

```text
1
```

**Example 2**

Input:

```python
kth_smallest_bst(root, 3)  # root = [5, 3, 6, 2, 4, None, None, 1]
```

Output:

```text
3
```

### Constraints

- `1 <= k <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Explanation

The stack-based inorder loop counts nodes as they are visited; the `k`-th one is returned immediately.

### Complexity

- Time: O(h + k). An iterative in-order walk stops after `k` nodes; going down the first path costs `h`.
- Space: O(h). The stack holds one path; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
