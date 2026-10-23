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

## Theory

A **linked list** is a chain of nodes. Each node stores a value and a pointer `next` to the following node; the last node's `next` is `None`. You can only reach a node by walking from the `head`, one `next` at a time. That makes reaching the 5th node `O(5)`, not `O(1)` as in a Python list, but inserting or removing at a known spot costs `O(1)` because only pointers change.

**Reversing** means turning every pointer around. Walk once with two variables: `prev` (the part already reversed, starting as `None`) and `head` (the part not yet visited). For each node, remember its `next` first (otherwise you lose the rest of the list), point the node back at `prev`, then move both variables forward.

This one move, "save next, redirect, advance", is the building block for most linked list questions. It takes `O(n)` time and `O(1)` extra memory.

## Explanation

`after = head.next` saves the rest. `head.next = prev` flips the arrow. Then `prev = head` and `head = after` step forward. When `head` becomes `None`, `prev` is the last node, which is the new head.
