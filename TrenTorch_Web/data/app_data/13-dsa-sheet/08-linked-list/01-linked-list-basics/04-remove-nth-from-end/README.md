---
name: sheet-remove-nth-from-end
title: 'Remove the Nth Node From the End'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
---

## Statement

Remove the **`n`-th node from the end** of the list (the last node is `n = 1`) and return the head. Do it in **one pass**.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
remove_nth_from_end(head, 2)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[1, 2, 3, 5]
```

**Explanation:** The 2nd node from the end is 4, so removing it yields 1,2,3,5.

**Example 2**

Input:

```python
remove_nth_from_end(head, 1)  # head = 1
```

Output:

```text
[]
```

**Explanation:** The only node is the 1st from end, so removal leaves an empty list.

### Constraints

- `1 <= number of nodes <= 100000`
- `1 <= n <= number of nodes`
- `-10**9 <= val <= 10**9`

## Theory

The `n`-th from the end is the `(length - n + 1)`-th from the start, but you do not know the length yet. Counting first and walking again works (two passes). One pass needs a trick: keep two pointers **`n` nodes apart**. Send `fast` ahead by `n` steps, then move both together. When `fast` reaches the last node, `slow` is just before the node to delete.

Use a **dummy head** in front of the list. Then removing the first node (when `n` equals the length) is no special case: `slow` simply stays on the dummy, and `dummy.next` is the new head.

## Explanation

`fast` starts `n` steps ahead of `slow`. Both move until `fast.next` is `None`, which leaves `slow` on the node before the one to remove. `slow.next = slow.next.next` unlinks it.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `dummy = ListNode(0, head)` | `dummy = <04-remove-nth-from-end_solution.ListNode object at 0x000...`                                                                     |
| `fast = slow = dummy`       | `fast = <04-remove-nth-from-end_solution.ListNode object at 0x000..., slow = <04-remove-nth-from-end_solution.ListNode object at 0x000...` |
| `for _ in range(n):`        | `_ = 0`                                                                                                                                    |
| `for _ in range(n):`        | `_ = 1`                                                                                                                                    |
| `return`                    | `returned = <04-remove-nth-from-end_solution.ListNode object at 0x000...`                                                                  |

### Complexity

- Time: O(n) where n is the list length.
- Extra space: O(1) extra.
- The brute force takes O(n) where n is the list length.
