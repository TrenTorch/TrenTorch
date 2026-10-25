---
name: sheet-reverse-linked-list
title: 'Reverse a Linked List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
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

**Explanation:** The algorithm iterates through each node, setting its next pointer to the previous node, so the last node 5 becomes the new head and the order becomes 5,4,3,2,1.

**Example 2**

Input:

```python
reverse_list(head)  # head = empty list
```

Output:

```text
[]
```

**Explanation:** An empty input list has no nodes, so the loop never runs and prev remains None, returning an empty list.

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

A **linked list** is a chain of nodes. Each node stores a value and a pointer `next` to the following node; the last node's `next` is `None`. You can only reach a node by walking from the `head`, one `next` at a time. That makes reaching the 5th node `O(5)`, not `O(1)` as in a Python list, but inserting or removing at a known spot costs `O(1)` because only pointers change.

**Reversing** means turning every pointer around. Walk once with two variables: `prev` (the part already reversed, starting as `None`) and `head` (the part not yet visited). For each node, remember its `next` first (otherwise you lose the rest of the list), point the node back at `prev`, then move both variables forward.

This one move, "save next, redirect, advance", is the building block for most linked list questions. It takes `O(n)` time and `O(1)` extra memory.

## Explanation

`after = head.next` saves the rest. `head.next = prev` flips the arrow. Then `prev = head` and `head = after` step forward. When `head` becomes `None`, `prev` is the last node, which is the new head.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line     | Variables                                                                 |
| ------------------- | ------------------------------------------------------------------------- |
| `prev = None`       | `prev = None`                                                             |
| `after = head.next` | `after = <01-reverse-linked-list_solution.ListNode object at 0x000...`    |
| `prev = head`       | `prev = <01-reverse-linked-list_solution.ListNode object at 0x000...`     |
| `after = head.next` | `after = None`                                                            |
| `head = after`      | `head = None`                                                             |
| `return`            | `returned = <01-reverse-linked-list_solution.ListNode object at 0x000...` |

### Complexity

- Time: O(n) where n is the number of nodes in the linked list.
- Extra space: O(1) extra memory, only a few pointers used.
- The brute force takes O(n) where n is the number of nodes, due to list conversion and reconstruction.
