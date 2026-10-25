---
name: sheet-basic-calculator-brackets
title: 'Calculator With Brackets'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Advanced
---

## Statement

`s` is an expression with whole numbers, `+`, `-`, **round brackets** and optional spaces. `-` can also be a **minus sign in front of a bracket or a number** (`"-(2+3)"`, `"1-(-2)"`). Return the value.

For `"(1+(4+5+2)-3)+(6+8)"` the answer is `23`.

### Examples

**Example 1**

Input:

```python
calculate_brackets('(1+(4+5+2)-3)+(6+8)')
```

Output:

```text
23
```

**Explanation:** The expression is evaluated from left to right, respecting parentheses, resulting in 1+4+5+2-3+6+8 = 23.

**Example 2**

Input:

```python
calculate_brackets('1 - (-2)')
```

Output:

```text
3
```

**Explanation:** Subtracting a negative number turns into addition: 1 - (-2) equals 1 + 2 = 3.

### Constraints

- `1 <= len(s) <= 100000`
- The expression is valid.
- Every number and intermediate value fits in 64 bits.

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Only `+` and `-` are involved, so no precedence is needed; brackets are the only difficulty. The key idea: **a minus in front of a bracket flips the sign of everything inside it.**

Keep a running `result`, the `sign` of the next number (`+1` or `-1`), and a stack. At `(`: push the `result` so far and the `sign` in front of the bracket, then restart with `result = 0` and `sign = +1`. At `)`: the bracket is finished, so `result = saved_result + saved_sign * result` (pop both).

A `-` before a number or a bracket just sets `sign = -1`, which also covers unary minus.

## Explanation

`result += sign * num` is done when a number ends. The stack remembers the outside value and the sign that applies to the whole bracket.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables                                                                              |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| `stack = []`                    | `stack = []`                                                                           |
| `for ch in s:`                  | `stack = [(0, 1)], result = 0, num = 1, sign = 1, ch = '+'`                            |
| `for ch in s:`                  | `stack = [(0, 1), (1, 1)], num = 4`                                                    |
| `for ch in s:`                  | `result = 9, num = 0, ch = '2'`                                                        |
| `sign = 1 if ch == "+" else -1` | `stack = [(0, 1)], result = 12, sign = -1, ch = '-', saved_result = 1, saved_sign = 1` |
| `sign = 1 if ch == "+" else -1` | `stack = [], result = 9, sign = 1, ch = '+', saved_result = 0`                         |
| `num = 0`                       | `stack = [(9, 1)], result = 6`                                                         |
| `return`                        | `returned = 23`                                                                        |

### Complexity

- Time: O(n) where n is input length.
- Extra space: O(n) extra stack memory for nested brackets.
- The brute force takes O(n) length of s.
