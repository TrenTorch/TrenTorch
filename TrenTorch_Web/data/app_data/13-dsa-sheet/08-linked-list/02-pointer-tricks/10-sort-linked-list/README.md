---
name: sheet-sort-linked-list
title: 'Sort a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
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

## Theory

Sorting a Python list is a one-liner, but a linked list has no random access: quick sort and heap sort need indexing. **Merge sort** only needs sequential access and merging, which linked lists do well (and in place).

The recursion: (1) base case: a list of 0 or 1 nodes is sorted; (2) find the middle with slow/fast pointers and **cut** the list into two halves; (3) sort each half recursively; (4) **merge** the two sorted halves (exactly the "merge two sorted lists" question).

There are `log n` levels, each costing `O(n)` for splitting and merging: `O(n log n)` time, and `O(log n)` memory for the recursion.

## Explanation

The helper `merge` joins two sorted lists with a dummy head. `slow` stops at the end of the first half; `slow.next = None` cuts the list there.
