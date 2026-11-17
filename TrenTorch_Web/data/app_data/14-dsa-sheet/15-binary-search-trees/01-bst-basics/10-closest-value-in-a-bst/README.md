---
name: sheet-closest-value-in-a-bst
title: 'Closest Value in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: closest-value-to-a-target
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the value in the tree that is **closest to `target`**. If two values are equally close, return the **smaller** one.

For `[4, 2, 5, 1, 3]` and `target = 3` the answer is `3`; for `[4, 2, 5, 1, 3]` and `target = 6` it is `5`.

### Examples

**Example 1**

Input:

```python
closest_value(root, 3)  # root = [4, 2, 5, 1, 3]
```

Output:

```text
3
```

**Example 2**

Input:

```python
closest_value(root, 6)  # root = [4, 2, 5, 1, 3]
```

Output:

```text
5
```

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `-10**9 <= target <= 10**9`

## Explanation

The key `(abs(v - target), v)` makes the tie-break automatic: the smaller distance wins, and for equal distances the smaller value.

### Complexity

- Time: O(h). One root-to-leaf walk toward the target.
- Space: O(1). Two numbers; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
