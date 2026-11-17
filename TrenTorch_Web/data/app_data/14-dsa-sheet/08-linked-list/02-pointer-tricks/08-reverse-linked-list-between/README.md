---
name: sheet-reverse-linked-list-between
title: 'Reverse Part of a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
theory: reversing-only-a-piece
---

## Statement

Reverse `size` nodes of the list **starting at position `left`** (the head is position 1) and return the head. The rest of the list stays in place.

For `1 -> 2 -> 3 -> 4 -> 5`, `left = 2` and `size = 3` give `1 -> 4 -> 3 -> 2 -> 5`.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
reverse_between(head, 2, 3)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[1, 4, 3, 2, 5]
```

**Example 2**

Input:

```python
reverse_between(head, 1, 1)  # head = 5
```

Output:

```text
[5]
```

### Constraints

- `1 <= number of nodes <= 100000`
- `1 <= left` and `1 <= size`
- `left + size - 1 <= number of nodes`

## Explanation

`cur = prev.next` is the part's first node and stays fixed. In each round `nxt = cur.next` is cut out and put right after `prev`. After `size - 1` rounds the part is reversed and `cur` links to whatever followed it.

### Complexity

- Time: O(n). Walk to the segment, then reverse `size` nodes with front insertion.
- Space: O(1). A few pointers.
