---
name: sheet-merge-sorted-lists
title: 'Merge Sorted Lists'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
theory: heaps-and-merging
---

## Statement

You are given a list of lists, and each inner list is already sorted in increasing order. Return one list with all the numbers, sorted in increasing order.

### Examples

**Example 1**

Input:

```python
merge_sorted_lists([[1, 4, 7], [2, 5], [3, 6, 9]])
```

Output:

```text
[1, 2, 3, 4, 5, 6, 7, 9]
```

**Example 2**

Input:

```python
merge_sorted_lists([[], [1], []])
```

Output:

```text
[1]
```

### Constraints

- `0 <= len(lists) <= 100`
- The total number of values is at most `5 * 10**5`.
- Inner lists can be empty.

## Explanation

`heapq.merge(*lists)` returns an iterator over the merged values in order. Wrap it in `list(...)`.

`*lists` unpacks the list of lists into separate arguments. An empty `lists` gives an empty result.

### Complexity

- Time: O(n log k). A heap of `k` list heads gives the next smallest value in O(log k), done `n` times.
- Space: O(k). The heap holds one head per list (the output is not counted).
