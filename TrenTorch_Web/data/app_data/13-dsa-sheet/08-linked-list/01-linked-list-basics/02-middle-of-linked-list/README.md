---
name: sheet-middle-of-linked-list
title: 'Middle of a Linked List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
---

## Statement

Return the **middle node** of the list. When the list has an even number of nodes there are two middle nodes: return the **second** one. The answer is the node together with all nodes after it.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
middle_node(head)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[3, 4, 5]
```

**Example 2**

Input:

```python
middle_node(head)  # head = 1 -> 2 -> 3 -> 4
```

Output:

```text
[3, 4]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

You do not know the length in advance, and a linked list cannot jump. Counting the nodes first and walking again works, but there is a neat one-pass trick: **slow and fast pointers**. Move `slow` one step and `fast` two steps each round. When `fast` reaches the end, `slow` has covered half the distance, so it is at the middle.

The loop `while fast and fast.next` stops when `fast` is `None` (even length: `slow` ends on the second middle) or on the last node (odd length: `slow` ends on the exact middle).

The same two-speed idea finds the start of a cycle, the half of a list to reverse, and more.

## Explanation

`fast` moves twice as fast as `slow`. When `fast` can no longer take two steps, `slow` is exactly halfway. For `1 -> 2 -> 3 -> 4` the loop ends with `slow` on `3`, the second middle.
