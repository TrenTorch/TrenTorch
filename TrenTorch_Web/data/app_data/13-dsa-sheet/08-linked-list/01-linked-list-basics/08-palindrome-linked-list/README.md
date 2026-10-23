---
name: sheet-palindrome-linked-list
title: 'Palindrome Linked List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
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

## Theory

A palindrome list matches its second half read backwards. With pointers: (1) find the **middle** with slow and fast pointers, (2) **reverse** the second half in place, (3) walk from both ends toward the middle comparing values.

This combines two earlier tools: slow/fast pointers and in-place reversal. It uses `O(1)` extra memory. (Real code often reverses the second half back afterwards, so the list is left as it was; here the tests do not look at the list afterwards.)

The easy version, `values = [..]; values == values[::-1]`, is correct and also `O(n)`, but uses `O(n)` memory.

## Explanation

After the first loop, `slow` is on the middle node (for odd lengths the middle belongs to the second half, and it still matches itself). The second half is reversed, and then both halves are compared until the shorter one (the reversed half) ends.
