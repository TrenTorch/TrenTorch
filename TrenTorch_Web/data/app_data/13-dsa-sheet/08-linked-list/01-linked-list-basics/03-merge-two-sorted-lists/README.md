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

**Explanation:** Both lists are sorted; merging compares heads and appends the smaller, producing 1, 1, 2, 3, 4, 4.

**Example 2**

Input:

```python
merge_two_lists(list1, list2)  # list1 = empty, list2 = 0
```

Output:

```text
[0]
```

**Explanation:** list1 is empty, so the merged list equals list2, which is [0].

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line       | Variables                                                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `dummy = ListNode()`  | `dummy = <03-merge-two-sorted-lists_solution.ListNode object at 0x...`                                                               |
| `tail = dummy`        | `tail = <03-merge-two-sorted-lists_solution.ListNode object at 0x...`                                                                |
| `a, b = list1, list2` | `a = <03-merge-two-sorted-lists_solution.ListNode object at 0x..., b = <03-merge-two-sorted-lists_solution.ListNode object at 0x...` |
| `a = a.next`          | `a = None`                                                                                                                           |
| `return`              | `returned = <03-merge-two-sorted-lists_solution.ListNode object at 0x...`                                                            |

### Complexity

- Time: O(n + m) n and m are list lengths.
- Extra space: O(1) constant extra space.
- The brute force takes O((n+m) log(n+m)) n and m are list lengths.
