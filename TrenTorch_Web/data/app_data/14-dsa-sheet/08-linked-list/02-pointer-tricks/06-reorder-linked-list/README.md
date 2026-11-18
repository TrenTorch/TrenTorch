---
name: sheet-reorder-linked-list
title: 'Reorder a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
theory: halve-reverse-weave
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

## Explanation

`slow` stops at the end of the first half (the first half is the longer one for odd lengths). The second half is cut off and reversed, and the weave loop links `first -> second -> (first.next)` repeatedly.

### Complexity

- Time: O(n). Find the middle, reverse the second half, then interleave the two halves; each step is one pass.
- Space: O(1). A few pointers.
