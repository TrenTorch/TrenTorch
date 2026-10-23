---
name: sheet-merge-two-sorted-lists
title: 'Merge Two Sorted Lists'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
---

## Statement

`list1` and `list2` are linked lists sorted in increasing order. **Merge** them into one sorted list by re-using their nodes, and return its head.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
merge_two_lists(list1, list2)  # list1 = 1 -> 2 -> 4, list2 = 1 -> 3 -> 4
```

Output:

```text
[1, 1, 2, 3, 4, 4]
```

**Example 2**

Input:

```python
merge_two_lists(list1, list2)  # list1 = empty, list2 = 0
```

Output:

```text
[0]
```

### Constraints

- `0 <= nodes in each list <= 100000`
- `-10**9 <= val <= 10**9`
- Both lists are sorted in increasing order.

## Theory

This is the merge step of merge sort, done with pointers. Keep a `tail` for the merged list and compare the two front nodes: attach the smaller one to `tail`, advance in that list, move `tail` forward. When one list runs out, attach the whole rest of the other (it is already sorted).

A **dummy head** node makes the code simpler: `tail` starts on a throwaway node, so you never have to write "if the merged list is still empty" cases. Return `dummy.next` at the end.

It takes `O(n + m)` time and `O(1)` extra memory because no node is copied, only `next` pointers are changed.

## Explanation

The loop takes the smaller front node each time and links it after `tail`. After the loop at most one list still has nodes; `tail.next = a or b` appends that rest in one step.
