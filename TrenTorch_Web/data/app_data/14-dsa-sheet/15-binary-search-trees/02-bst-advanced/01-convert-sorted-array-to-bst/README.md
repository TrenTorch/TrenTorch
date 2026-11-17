---
name: sheet-convert-sorted-array-to-bst
title: 'Sorted Array to a Balanced BST'
tags: [dsa-sheet, binary-search-trees, bst-advanced]
difficulty: Intermediate
theory: building-a-balanced-bst-from-a-sorted-list
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

`nums` is sorted in increasing order with different values. Build a **height-balanced BST** (the heights of the two subtrees of every node differ by at most 1) containing all the values. To make the answer unique, always take the **middle element, and the lower middle when the count is even** (index `(lo + hi) // 2`) as the root of a range.

For `[-10, -3, 0, 5, 9]` the answer is `[0, -10, 5, None, -3, None, 9]`.

### Examples

**Example 1**

Input:

```python
sorted_array_to_bst(nums)  # nums = [-10, -3, 0, 5, 9]
```

Output:

```text
[0, -10, 5, None, -3, None, 9]
```

**Example 2**

Input:

```python
sorted_array_to_bst(nums)  # nums = [1, 3]
```

Output:

```text
[1, None, 3]
```

### Constraints

- `0 <= len(nums) <= 100000`
- `nums` is strictly increasing.

## Explanation

`build(lo, hi)` makes the node for the middle index and builds the two halves around it. An empty range gives `None`.

### Complexity

- Time: O(n). Each value becomes a node once.
- Space: O(log n). The recursion is `log n` deep (the new tree itself is the output).
