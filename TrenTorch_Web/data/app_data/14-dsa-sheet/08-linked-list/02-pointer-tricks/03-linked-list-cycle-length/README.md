---
name: sheet-linked-list-cycle-length
title: 'Length of the Cycle'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
theory: how-long-is-the-loop
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

## Explanation

After the meeting, `node = slow.next` and `length = 1` start the count; each step moves one node, and the loop ends back at `slow`.

### Complexity

- Time: O(n). Find a node inside the cycle with Floyd, then count one lap.
- Space: O(1). Two pointers and a counter.
