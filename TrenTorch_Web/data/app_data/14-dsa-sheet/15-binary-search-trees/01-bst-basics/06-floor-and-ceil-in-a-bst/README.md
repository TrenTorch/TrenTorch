---
name: sheet-floor-and-ceil-in-a-bst
title: 'Floor and Ceil in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: floor-and-ceil
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

For a number `x`, the **floor** is the largest value in the tree that is `<= x` and the **ceil** is the smallest value that is `>= x`. Return `[floor, ceil]`, using `-1` where there is none. All values in the tree are non-negative.

For `[8, 4, 12, 2, 6, 10, 14]` and `x = 5` the answer is `[4, 6]`.

### Examples

**Example 1**

Input:

```python
floor_and_ceil_bst(root, 5)  # root = [8, 4, 12, 2, 6, 10, 14]
```

Output:

```text
[4, 6]
```

**Example 2**

Input:

```python
floor_and_ceil_bst(root, 1)  # root = [8, 4, 12, 2, 6, 10, 14]
```

Output:

```text
[-1, 2]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `0 <= val, x <= 10**9`

## Explanation

`floor` and `ceil` keep the closest values found so far on each side of `x` while the walk narrows the interval.

### Complexity

- Time: O(h). One root-to-leaf walk remembering the last smaller and the last larger value.
- Space: O(1). Two numbers; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
