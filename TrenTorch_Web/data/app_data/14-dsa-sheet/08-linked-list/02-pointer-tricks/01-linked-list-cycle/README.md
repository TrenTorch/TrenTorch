---
name: sheet-linked-list-cycle
title: 'Does the List Have a Cycle?'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
theory: the-tortoise-and-the-hare
---

## Statement

Return `True` if the list has a **cycle**, that is, if following `next` pointers from `head` never reaches `None`.

A list can have a **cycle**: the last node's `next` points back at an earlier node. The tests give such a list as `{"values": [...], "cycle": k}`, where the last node points back at node `k` (counting from 0), and `k = -1` means no cycle.

The starter code remembers every visited node in a list. It is correct but too slow. Use `O(1)` memory.

### Examples

**Example 1**

Input:

```python
has_cycle(head)  # head = 3 -> 2 -> 0 -> -4, and -4 points back at 2
```

Output:

```text
True
```

**Example 2**

Input:

```python
has_cycle(head)  # head = 1 -> 2, no cycle
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The cycle position `k` is `-1` or a valid index.

## Explanation

The loop ends when `fast` reaches `None` (no cycle). Inside a cycle `fast` closes the gap by one node each round, so it catches `slow`.

### Complexity

- Time: O(n). Floyd's tortoise and hare: if there is a cycle, `fast` catches `slow` within one lap of it.
- Space: O(1). Two pointers.
