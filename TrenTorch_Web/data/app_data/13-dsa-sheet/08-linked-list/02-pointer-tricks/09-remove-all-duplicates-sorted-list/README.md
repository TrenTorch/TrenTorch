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

**Explanation:** Values 3 and 4 appear more than once in the input list, so they are removed, leaving only the distinct values 1, 2, and 5.

**Example 2**

Input:

```python
remove_all_duplicates(head)  # head = 1 -> 1 -> 1 -> 2 -> 3
```

Output:

```text
[2, 3]
```

**Explanation:** The value 1 appears three times in the input list, so it is entirely removed, leaving only the distinct values 2 and 3.

### Constraints

- `0 <= number of nodes <= 100000`
- The list is sorted in increasing order.

## Theory

Unlike the earlier version, a whole group of equal values must disappear, including the first node of the group, so the **head can be removed**: use a dummy head.

Keep `prev` (the last node kept) and `cur`. If `cur.val == cur.next.val`, remember that value and skip **all** nodes with it (`while cur and cur.val == value: cur = cur.next`), then link `prev.next = cur`. Otherwise `cur` is unique: `prev = cur`, advance.

Notice that `prev` only moves when a node is confirmed unique, so later duplicates are still cut out correctly.

## Explanation

A repeat triggers an inner loop that skips the whole group. The outer pointers move on only when the node is unique.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                                                                                 |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `dummy = ListNode(0, head)` | `dummy = <09-remove-all-duplicates-sorted-list_solution.ListNode o...`                                                                    |
| `prev, cur = dummy, head`   | `prev = <09-remove-all-duplicates-sorted-list_solution.ListNode o..., cur = <09-remove-all-duplicates-sorted-list_solution.ListNode o...` |
| `value = cur.val`           | `value = 3`                                                                                                                               |
| `value = cur.val`           | `value = 4`                                                                                                                               |
| `cur = cur.next`            | `cur = None`                                                                                                                              |
| `return`                    | `returned = <09-remove-all-duplicates-sorted-list_solution.ListNode o...`                                                                 |

### Complexity

- Time: O(n), where n is the number of nodes in the list.
- Extra space: O(1), using only a dummy node and two pointers.
- The brute force takes O(n), where n is the number of nodes in the list.
