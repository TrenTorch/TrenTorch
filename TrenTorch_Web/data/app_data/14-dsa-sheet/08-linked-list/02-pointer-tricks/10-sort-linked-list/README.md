---
name: sheet-sort-linked-list
title: 'Sort a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
theory: merge-sort-on-a-list
---

## Statement

Sort the list in **increasing order** and return its head. Aim for `O(n log n)` time.

The starter code is an insertion sort. It is correct but too slow for long lists.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
sort_list(head)  # head = 4 -> 2 -> 1 -> 3
```

Output:

```text
[1, 2, 3, 4]
```

**Example 2**

Input:

```python
sort_list(head)  # head = -1 -> 5 -> 3 -> 4 -> 0
```

Output:

```text
[-1, 0, 3, 4, 5]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Explanation

The helper `merge` joins two sorted lists with a dummy head. `slow` stops at the end of the first half; `slow.next = None` cuts the list there.

### Complexity

- Time: O(n log n). Merge sort halves the list `log n` times and each level merges `n` nodes; no comparison sort can be faster.
- Space: O(log n). The recursion depth; nodes are relinked, not copied.
