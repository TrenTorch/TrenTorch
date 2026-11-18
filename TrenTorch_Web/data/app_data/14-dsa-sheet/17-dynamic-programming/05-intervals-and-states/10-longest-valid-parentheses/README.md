---
name: sheet-longest-valid-parentheses
title: 'Longest Valid Parentheses'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
theory: longest-valid-parentheses
---

## Statement

`s` contains only `(` and `)`. Return the length of the **longest substring** (consecutive characters) that is a **valid** parentheses string (every `(` closed in the right order).

For `")()())"` the answer is `4`.

The starter code checks every substring. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_valid_parentheses(')()())')
```

Output:

```text
4
```

**Example 2**

Input:

```python
longest_valid_parentheses('(()')
```

Output:

```text
2
```

### Constraints

- `0 <= len(s) <= 200000`

## Explanation

Scan left to right counting `(` as `left` and `)` as `right`. When the counts are equal, the stretch so far is balanced: its length is `2 * left`. When `right` exceeds `left`, no valid stretch can include this bracket, so reset both. That finds every valid stretch except those with extra `(` that never get closed, like `(()`. A second scan from right to left with the roles of the brackets swapped finds those. No stack is needed.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line       | Variables                                                                              |
| --------------------- | -------------------------------------------------------------------------------------- |
| `best = 0`            | `best = 0`                                                                             |
| `right += 1`          | `sequence = ')()())', opener = '(', left = 0, right = 1, ch = ')'`                     |
| `for ch in sequence:` | `left = 1, right = 0`                                                                  |
| `left += 1`           | `best = 2, left = 2, right = 1, ch = '('`                                              |
| `left = right = 0`    | `best = 4, left = 0, right = 0, ch = ')'`                                              |
| `for ch in sequence:` | `sequence = <reversed object at 0x000002BDE6B02110>, opener = ')', left = 2, ch = '('` |
| `for ch in sequence:` | `left = 3, right = 1`                                                                  |
| `return`              | `returned = 4`                                                                         |

### Complexity

- Time: O(n). Two scans, one from each end, counting opening and closing brackets.
- Space: O(1). Two counters.
