---
name: sheet-reverse-linked-list
title: 'Reverse a Linked List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
theory: reversing-in-place
---

## Statement

Reverse a singly linked list and return the new head. Each node has a `val` and a `next` (the next node, or `None` at the end).

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
reverse_list(head)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[5, 4, 3, 2, 1]
```

**Example 2**

Input:

```python
reverse_list(head)  # head = empty list
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Explanation

`after = head.next` saves the rest. `head.next = prev` flips the arrow. Then `prev = head` and `head = after` step forward. When `head` becomes `None`, `prev` is the last node, which is the new head.

### Complexity

- Time: O(n). Each node is visited once and its pointer is flipped.
- Space: O(1). Three pointers.
