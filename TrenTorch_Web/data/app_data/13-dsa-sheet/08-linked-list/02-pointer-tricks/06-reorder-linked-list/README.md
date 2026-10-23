---
name: sheet-reorder-linked-list
title: 'Reorder a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
---

## Statement

Reorder the list `L0 -> L1 -> ... -> Ln` as `L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...`: first, last, second, second to last, and so on. Change the pointers, not the values, and return the head.

For `1 -> 2 -> 3 -> 4` the answer is `1 -> 4 -> 2 -> 3`.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
reorder_list(head)  # head = 1 -> 2 -> 3 -> 4
```

Output:

```text
[1, 4, 2, 3]
```

**Example 2**

Input:

```python
reorder_list(head)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[1, 5, 2, 4, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

The pattern "front, back, front, back" is hard on a singly linked list because you cannot walk backwards. The fix is to **combine three tools**:

1. Find the **middle** with slow and fast pointers and cut the list in two halves.
2. **Reverse** the second half. Now its first node is the old last node.
3. **Weave** the halves: take one node from the first half, then one from the reversed second half, and so on.

Each step is `O(n)` and uses `O(1)` memory. The skill is recognising that a hard-looking problem is a sequence of small tools you already have.

## Explanation

`slow` stops at the end of the first half (the first half is the longer one for odd lengths). The second half is cut off and reversed, and the weave loop links `first -> second -> (first.next)` repeatedly.
