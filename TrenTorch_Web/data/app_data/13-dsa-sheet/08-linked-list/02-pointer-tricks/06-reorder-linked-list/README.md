---
name: sheet-reorder-linked-list
title: 'Reorder a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
---

## Statement

Reorder the list `L0 -> L1 -> ... -> Ln` as `L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...`: first, last, second, second to last, and so on. Change the pointers, not the values, and return the head.

For `1 -> 2 -> 3 -> 4` the answer is `1 -> 4 -> 2 -> 3`.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
reorder_list(head)  # head = 1 -> 2 -> 3 -> 4
```

Output:

```text
[1, 4, 2, 3]
```

**Explanation:** The reorder alternates between the start and end of the list: first node 1, then last 4, then second 2, then third 3.

**Example 2**

Input:

```python
reorder_list(head)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[1, 5, 2, 4, 3]
```

**Explanation:** The pattern picks 1, then 5, then 2, then 4, then the middle 3.

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

The pattern "front, back, front, back" is hard on a singly linked list because you cannot walk backwards. The fix is to **combine three tools**:

1. Find the **middle** with slow and fast pointers and cut the list in two halves.
2. **Reverse** the second half. Now its first node is the old last node.
3. **Weave** the halves: take one node from the first half, then one from the reversed second half, and so on.

Each step is `O(n)` and uses `O(1)` memory. The skill is recognising that a hard-looking problem is a sequence of small tools you already have.

## Explanation

`slow` stops at the end of the first half (the first half is the longer one for odd lengths). The second half is cut off and reversed, and the weave loop links `first -> second -> (first.next)` repeatedly.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                                                                                                                                                                                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `slow, fast = head, head.next`   | `slow = <06-reorder-linked-list_solution.ListNode object at 0x000..., fast = <06-reorder-linked-list_solution.ListNode object at 0x000...`                                                                                                                                        |
| `prev = None`                    | `second = <06-reorder-linked-list_solution.ListNode object at 0x000..., prev = None`                                                                                                                                                                                              |
| `after = second.next`            | `after = <06-reorder-linked-list_solution.ListNode object at 0x000...`                                                                                                                                                                                                            |
| `after = second.next`            | `prev = <06-reorder-linked-list_solution.ListNode object at 0x000..., after = None`                                                                                                                                                                                               |
| `second = after`                 | `second = None`                                                                                                                                                                                                                                                                   |
| `a, b = first.next, second.next` | `second = <06-reorder-linked-list_solution.ListNode object at 0x000..., first = <06-reorder-linked-list_solution.ListNode object at 0x000..., a = <06-reorder-linked-list_solution.ListNode object at 0x000..., b = <06-reorder-linked-list_solution.ListNode object at 0x000...` |
| `a, b = first.next, second.next` | `a = None, b = None`                                                                                                                                                                                                                                                              |
| `return`                         | `returned = <06-reorder-linked-list_solution.ListNode object at 0x000...`                                                                                                                                                                                                         |

### Complexity

- Time: O(n) where n is the number of nodes.
- Extra space: O(1) extra space.
- The brute force takes O(n) where n is the number of nodes.
