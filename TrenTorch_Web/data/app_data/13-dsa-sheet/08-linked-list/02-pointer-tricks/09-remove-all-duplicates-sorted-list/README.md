---
name: sheet-remove-all-duplicates-sorted-list
title: 'Remove Every Repeated Value'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
---

## Statement

`head` is sorted in increasing order. Delete **every node whose value appears more than once**, so only values that were already distinct remain. For `1 -> 2 -> 3 -> 3 -> 4 -> 4 -> 5` the answer is `1 -> 2 -> 5`.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
remove_all_duplicates(head)  # head = 1 -> 2 -> 3 -> 3 -> 4 -> 4 -> 5
```

Output:

```text
[1, 2, 5]
```

**Example 2**

Input:

```python
remove_all_duplicates(head)  # head = 1 -> 1 -> 1 -> 2 -> 3
```

Output:

```text
[2, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The list is sorted in increasing order.

## Theory

Unlike the earlier version, a whole group of equal values must disappear, including the first node of the group, so the **head can be removed**: use a dummy head.

Keep `prev` (the last node kept) and `cur`. If `cur.val == cur.next.val`, remember that value and skip **all** nodes with it (`while cur and cur.val == value: cur = cur.next`), then link `prev.next = cur`. Otherwise `cur` is unique: `prev = cur`, advance.

Notice that `prev` only moves when a node is confirmed unique, so later duplicates are still cut out correctly.

## Explanation

A repeat triggers an inner loop that skips the whole group. The outer pointers move on only when the node is unique.
