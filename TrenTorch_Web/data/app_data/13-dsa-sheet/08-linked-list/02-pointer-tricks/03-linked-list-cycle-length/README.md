---
name: sheet-linked-list-cycle-length
title: 'Length of the Cycle'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
---

## Statement

Return the **number of nodes in the cycle**, or `0` if the list has no cycle.

A list can have a **cycle**: the last node's `next` points back at an earlier node. The tests give such a list as `{"values": [...], "cycle": k}`, where the last node points back at node `k` (counting from 0), and `k = -1` means no cycle.

### Examples

**Example 1**

Input:

```python
cycle_length(head)  # head = 3 -> 2 -> 0 -> -4, and -4 points back at 2
```

Output:

```text
3
```

**Example 2**

Input:

```python
cycle_length(head)  # head = 1 -> 2, no cycle
```

Output:

```text
0
```

### Constraints

- `0 <= number of nodes <= 100000`
- The cycle position `k` is `-1` or a valid index.

## Theory

Once slow and fast pointers **meet**, they are both inside the cycle. Leave `fast` where it is and walk another pointer around the cycle until it returns to the meeting node, counting the steps. That count is the cycle length.

If `fast` falls off the end instead, there is no cycle: return `0`.

This is the same tortoise and hare idea, finished with a short counting loop.

## Explanation

After the meeting, `node = slow.next` and `length = 1` start the count; each step moves one node, and the loop ends back at `slow`.
