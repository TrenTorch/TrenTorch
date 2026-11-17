---
name: sheet-balance-a-bst
title: 'Balance a BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
theory: rebalancing-a-bst
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

The BST may be badly unbalanced (even a chain). Rebuild it as a **height-balanced BST** with the same values. As in the previous question, use the **lower middle** of each range as its root, so the answer is unique.

For `[1, None, 2, None, 3, None, 4]` the answer is `[2, 1, 3, None, None, None, 4]`.

### Examples

**Example 1**

Input:

```python
balance_bst(root)  # root = [1, None, 2, None, 3, None, 4]
```

Output:

```text
[2, 1, 3, None, None, None, 4]
```

**Example 2**

Input:

```python
balance_bst(root)  # root = [2, 1, 3]
```

Output:

```text
[2, 1, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Explanation

The first loop collects the values in sorted order; `build` makes the balanced tree from index ranges.

### Complexity

- Time: O(n). One in-order walk collects the sorted values and one recursion rebuilds the tree.
- Space: O(n). The list of values (the new tree is the output).
