---
name: sheet-linked-list-cycle
title: 'Does the List Have a Cycle?'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
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

## Theory

A set of visited nodes finds a cycle in `O(n)` time but uses `O(n)` memory (and a _list_ of visited nodes is `O(n²)` time, which is why the starter is slow).

**Floyd's tortoise and hare** uses no memory. Move `slow` one step and `fast` two steps. Without a cycle, `fast` falls off the end. With a cycle, both end up circling inside it, and because `fast` gains one step per round on `slow`, it must eventually land **on the same node**. If they ever meet, there is a cycle.

The comparison must be `slow is fast` (the same node), not equal values: different nodes may hold the same value.

## Explanation

The loop ends when `fast` reaches `None` (no cycle). Inside a cycle `fast` closes the gap by one node each round, so it catches `slow`.
