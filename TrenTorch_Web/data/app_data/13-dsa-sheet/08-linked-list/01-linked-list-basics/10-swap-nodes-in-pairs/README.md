---
name: sheet-swap-nodes-in-pairs
title: 'Swap Nodes in Pairs'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
---

## Statement

Swap every **two adjacent nodes** and return the new head: `1 -> 2 -> 3 -> 4` becomes `2 -> 1 -> 4 -> 3`. If the length is odd the last node stays. Change the **pointers**, not the values stored in the nodes.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
swap_pairs(head)  # head = 1 -> 2 -> 3 -> 4
```

Output:

```text
[2, 1, 4, 3]
```

**Example 2**

Input:

```python
swap_pairs(head)  # head = 1 -> 2 -> 3
```

Output:

```text
[2, 1, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

Swapping two nodes `a -> b` that sit after a node `prev` means rewiring three pointers: `prev -> b`, `b -> a`, `a -> (what came after b)`. Do it in the right order so you do not lose `b.next`: first `a.next = b.next`, then `b.next = a`, then `prev.next = b`.

After a swap, `a` is the second node of the pair, so it becomes the next `prev`. A **dummy head** makes the very first swap look like all the others, and the loop ends when fewer than two nodes remain.

## Explanation

`prev.next` is the first of the pair (`a`) and `a.next` is the second (`b`). The three assignments turn `prev -> a -> b -> rest` into `prev -> b -> a -> rest`. Then `prev = a` moves to the end of the swapped pair.
