---
name: sheet-palindrome-linked-list
title: 'Palindrome Linked List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
theory: halve-reverse-compare
---

## Statement

Return `True` if the list reads the **same forwards and backwards**. Try to use only `O(1)` extra memory (copying the values into a Python list is the easy way, but the challenge is to do it with pointers).

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
is_palindrome_list(head)  # head = 1 -> 2 -> 2 -> 1
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_palindrome_list(head)  # head = 1 -> 2
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- `0 <= val <= 9`

## Explanation

After the first loop, `slow` is on the middle node (for odd lengths the middle belongs to the second half, and it still matches itself). The second half is reversed, and then both halves are compared until the shorter one (the reversed half) ends.

### Complexity

- Time: O(n). Find the middle (`n / 2` steps), reverse the second half, compare the halves.
- Space: O(1). A few pointers; the second half is reversed in place.
