---
name: sheet-valid-parentheses
title: 'Valid Brackets'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Beginner
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

**Explanation:** All three pairs match their opening brackets, the stack empties, so the result is true.

**Example 2**

Input:

```python
valid_brackets('(]')
```

Output:

```text
False
```

**Explanation:** The closing ']' expects '[', but the top of the stack is '(', causing a mismatch and false.

### Constraints

- `0 <= len(s) <= 200000`

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Brackets match like nested boxes: the **last** one opened must be the **first** one closed. That is exactly what a stack gives you. Walk through the string: push every opening bracket; for a closing bracket, the top of the stack must be its matching opening bracket (pop it), otherwise the string is invalid. At the end the stack must be empty (no bracket was left open).

Two things to remember: a closing bracket with an **empty stack** is invalid, and leftover openers at the end are invalid. `O(n)` time and `O(n)` memory.

## Explanation

A dictionary maps each closing bracket to its opening bracket. On a closing bracket, the stack must be non-empty and its top must be the matching opener; popping removes it.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                |
| ---------------------------------------- | ---------------------------------------- |
| `match = {")": "(", "]": "[", "}": "{"}` | `match = {')': '(', ']': '[', '}': '{'}` |
| `for ch in s:`                           | `stack = [], ch = '('`                   |
| `for ch in s:`                           | `stack = ['('], ch = ')'`                |
| `for ch in s:`                           | `stack = [], ch = '['`                   |
| `for ch in s:`                           | `stack = ['['], ch = ']'`                |
| `for ch in s:`                           | `stack = [], ch = '{'`                   |
| `for ch in s:`                           | `stack = ['{'], ch = '}'`                |
| `return`                                 | `returned = True`                        |

### Complexity

- Time: O(n) where n is length of s.
- Extra space: O(n) stack up to n characters.
- The brute force takes O(n^2) where n is length of s.
