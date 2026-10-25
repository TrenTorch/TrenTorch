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

**Explanation:** The input 4, 2, 1, 3 is split into two halves and recursively sorted using merge sort, resulting in 1, 2, 3, 4.

**Example 2**

Input:

```python
sort_list(head)  # head = -1 -> 5 -> 3 -> 4 -> 0
```

Output:

```text
[-1, 0, 3, 4, 5]
```

**Explanation:** The input -1, 5, 3, 4, 0 is recursively partitioned and merged until all elements are in non-decreasing order: -1, 0, 3, 4, 5.

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

Sorting a Python list is a one-liner, but a linked list has no random access: quick sort and heap sort need indexing. **Merge sort** only needs sequential access and merging, which linked lists do well (and in place).

The recursion: (1) base case: a list of 0 or 1 nodes is sorted; (2) find the middle with slow/fast pointers and **cut** the list into two halves; (3) sort each half recursively; (4) **merge** the two sorted halves (exactly the "merge two sorted lists" question).

There are `log n` levels, each costing `O(n)` for splitting and merging: `O(n log n)` time, and `O(log n)` memory for the recursion.

## Explanation

The helper `merge` joins two sorted lists with a dummy head. `slow` stops at the end of the first half; `slow.next = None` cuts the list there.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line      | Variables                                                                                                                                                                                                         |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `def merge(a, b):`   | `merge = <function sort_list.<locals>.merge at 0x000001F48323B2E0>`                                                                                                                                               |
| `def merge(a, b):`   | `merge = <function sort_list.<locals>.merge at 0x000001F4832395A0>`                                                                                                                                               |
| `second = slow.next` | `slow = <10-sort-linked-list_solution.ListNode object at 0x000001..., fast = <10-sort-linked-list_solution.ListNode object at 0x000001..., second = <10-sort-linked-list_solution.ListNode object at 0x000001...` |
| `def merge(a, b):`   | `merge = <function sort_list.<locals>.merge at 0x000001F4855005E0>`                                                                                                                                               |
| `def merge(a, b):`   | `merge = <function sort_list.<locals>.merge at 0x000001F4832395A0>`                                                                                                                                               |
| `def merge(a, b):`   | `merge = <function sort_list.<locals>.merge at 0x000001F4855005E0>`                                                                                                                                               |
| `def merge(a, b):`   | `(no change)`                                                                                                                                                                                                     |
| `return`             | `returned = <10-sort-linked-list_solution.ListNode object at 0x000001...`                                                                                                                                         |

### Complexity

- Time: O(n log n) where n is the number of nodes.
- Extra space: O(log n) for the recursive call stack.
- The brute force takes O(n log n) where n is the number of nodes.
