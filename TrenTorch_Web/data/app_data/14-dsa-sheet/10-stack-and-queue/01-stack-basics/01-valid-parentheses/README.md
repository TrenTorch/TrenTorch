---
name: sheet-valid-parentheses
title: 'Valid Brackets'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Beginner
theory: brackets-that-must-match
---

## Statement

`s` contains only the characters `(`, `)`, `[`, `]`, `{` and `}`. Return `True` if the brackets are **valid**: every opening bracket is closed by the same kind of bracket, and brackets are closed in the correct order (`"([])"` is valid, `"([)]"` is not). The empty string is valid.

### Examples

**Example 1**

Input:

```python
valid_brackets('()[]{}')
```

Output:

```text
True
```

**Example 2**

Input:

```python
valid_brackets('(]')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 200000`

## Explanation

A dictionary maps each closing bracket to its opening bracket. On a closing bracket, the stack must be non-empty and its top must be the matching opener; popping removes it.

### Complexity

- Time: O(n). Each character is pushed or popped at most once.
- Space: O(n). The stack can hold all opening brackets.
