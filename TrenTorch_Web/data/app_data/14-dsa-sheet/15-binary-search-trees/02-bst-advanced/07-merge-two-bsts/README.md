---
name: sheet-merge-two-bsts
title: 'Merge Two BSTs into a Sorted List'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
theory: merging-two-bsts-into-a-sorted-list
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Given two BSTs, return **all their values** in one list sorted in increasing order (a value that is in both trees appears twice).

For `[2, 1, 4]` and `[1, 0, 3]` the answer is `[0, 1, 1, 2, 3, 4]`.

### Examples

**Example 1**

Input:

```python
merge_bsts(root1, root2)  # root1 = [2, 1, 4], root2 = [1, 0, 3]
```

Output:

```text
[0, 1, 1, 2, 3, 4]
```

**Example 2**

Input:

```python
merge_bsts(root1, root2)  # root1 = [], root2 = [5]
```

Output:

```text
[5]
```

### Constraints

- `0 <= number of nodes <= 50000` in each tree
- Both trees are BSTs, not deeper than 800 levels.

## Explanation

`inorder` returns the sorted values of one tree. The merge loop takes the smaller front value each time and appends the leftovers at the end.

### Complexity

- Time: O(n + m). Two in-order walks and one merge of the sorted lists.
- Space: O(n + m). The two lists and the merged result.
