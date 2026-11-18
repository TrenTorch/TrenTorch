---
name: sheet-partition-linked-list
title: 'Partition a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
theory: two-dummy-lists-partition
---

## Statement

Rearrange the list so that **all nodes with a value less than `x` come before** nodes with a value greater than or equal to `x`. Keep the **original relative order** inside each of the two groups.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
partition_list(head, 3)  # head = 1 -> 4 -> 3 -> 2 -> 5 -> 2
```

Output:

```text
[1, 2, 2, 4, 3, 5]
```

**Example 2**

Input:

```python
partition_list(head, 2)  # head = 2 -> 1
```

Output:

```text
[1, 2]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-1000 <= val, x <= 1000`

## Explanation

`small_tail` and `large_tail` grow two chains. `large_tail.next = None` cuts any stale pointer; `small_tail.next = large_dummy.next` joins them.

### Complexity

- Time: O(n). One pass appends each node to a smaller or a larger chain, then the chains are joined.
- Space: O(1). Two dummy nodes and tail pointers.
