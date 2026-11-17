---
name: sheet-merge-k-sorted-lists
title: 'Merge K Sorted Lists'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
theory: always-take-the-smallest-front
---

## Statement

`lists` is a list of `k` linked lists, each sorted in increasing order. **Merge them all** into one sorted list and return its head.

The starter code merges the lists into a growing result one after another. It is correct but too slow when there are many lists.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`. Here `lists` is shown as a list of such lists.

### Examples

**Example 1**

Input:

```python
merge_k_lists(lists)  # lists = [1 -> 4 -> 5, 1 -> 3 -> 4, 2 -> 6]
```

Output:

```text
[1, 1, 2, 3, 4, 4, 5, 6]
```

**Example 2**

Input:

```python
merge_k_lists(lists)  # lists = []
```

Output:

```text
[]
```

### Constraints

- `0 <= k <= 10000`
- `0 <= total number of nodes <= 100000`
- `-10**9 <= val <= 10**9`
- Each list is sorted in increasing order (a list may be empty).

## Explanation

The heap always holds at most one node per list: the front of each list that is not yet used. Each pop outputs the globally smallest remaining value.

### Complexity

- Time: O(N log k). A heap of `k` list heads gives the next smallest node in `O(log k)`, done `N` times (`N` = total nodes).
- Space: O(k). The heap holds one node per list.
