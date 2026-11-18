---
name: sheet-range-sum-of-a-bst
title: 'Range Sum of a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Beginner
theory: range-sum-with-pruning
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **sum of the values** in the tree that are between `low` and `high` (both included).

For `[10, 5, 15, 3, 7, None, 18]`, `low = 7` and `high = 15` the answer is `32` (`7 + 10 + 15`).

### Examples

**Example 1**

Input:

```python
range_sum_bst(root, 7, 15)  # root = [10, 5, 15, 3, 7, None, 18]
```

Output:

```text
32
```

**Example 2**

Input:

```python
range_sum_bst(root, 6, 10)  # root = [10, 5, 15, 3, 7, 13, 18, 1, None, 6]
```

Output:

```text
23
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `0 <= low <= high <= 10**9`

## Explanation

The two `if` branches prune; the last line adds the node and explores both sides.

### Complexity

- Time: O(h + m). `m` is the number of nodes inside the range: subtrees that cannot hold a value in range are skipped.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
