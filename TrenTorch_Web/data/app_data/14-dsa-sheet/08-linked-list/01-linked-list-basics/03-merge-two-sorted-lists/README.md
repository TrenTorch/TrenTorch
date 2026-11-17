---
name: sheet-merge-two-sorted-lists
title: 'Merge Two Sorted Lists'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
theory: merging-two-sorted-lists
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

## Explanation

The loop takes the smaller front node each time and links it after `tail`. After the loop at most one list still has nodes; `tail.next = a or b` appends that rest in one step.

### Complexity

- Time: O(n + m). Each step attaches one existing node, and each pointer only moves forward.
- Space: O(1). Nodes are relinked, not copied.
