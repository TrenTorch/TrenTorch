---
name: sheet-linked-list-cycle-start
title: 'Where Does the Cycle Start?'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
theory: where-does-the-loop-begin
---

## Statement

Return the **node where the cycle begins**, or `None` if the list has no cycle. Use `O(1)` extra memory.

A list can have a **cycle**: the last node's `next` points back at an earlier node. The tests give such a list as `{"values": [...], "cycle": k}`, where the last node points back at node `k` (counting from 0), and `k = -1` means no cycle. The tests check which node you returned (its position in the list).

### Examples

**Example 1**

Input:

```python
cycle_start(head)  # head = 3 -> 2 -> 0 -> -4, and -4 points back at 2
```

Output:

```text
1
```

The cycle starts at the node with value 2 (position 1).

**Example 2**

Input:

```python
cycle_start(head)  # head = 1 -> 2, no cycle
```

Output:

```text
-1
```

No cycle: the answer is `None`, shown as `-1`.

### Constraints

- `0 <= number of nodes <= 100000`
- The cycle position `k` is `-1` or a valid index.

## Explanation

After the first meeting, `slow` restarts from `head` while `fast` stays at the meeting point. Both then move one step per round; they meet at the node where the cycle begins.

### Complexity

- Time: O(n). Floyd's algorithm finds a meeting point; restarting one pointer at the head and moving both one step at a time makes them meet at the cycle start.
- Space: O(1). Two pointers.
