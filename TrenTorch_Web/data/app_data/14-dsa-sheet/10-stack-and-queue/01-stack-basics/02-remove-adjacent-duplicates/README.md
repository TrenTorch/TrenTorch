---
name: sheet-remove-adjacent-duplicates
title: 'Remove Adjacent Duplicates'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Beginner
theory: neighbours-that-cancel
---

## Statement

Repeatedly **delete two equal neighbouring characters** until none are left to delete, and return the remaining string. For `"abbaca"`: delete `bb` to get `"aaca"`, delete `aa` to get `"ca"`.

### Examples

**Example 1**

Input:

```python
remove_adjacent_duplicates('abbaca')
```

Output:

```text
'ca'
```

**Example 2**

Input:

```python
remove_adjacent_duplicates('azxxzy')
```

Output:

```text
'ay'
```

### Constraints

- `0 <= len(s) <= 200000`
- `s` contains lower-case letters.

## Explanation

The top of the stack is the last character that survived. A new character that matches it cancels it; otherwise it is kept.

### Complexity

- Time: O(n). Each character is pushed or popped at most once.
- Space: O(n). The stack.
