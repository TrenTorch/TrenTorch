---
name: sheet-calculator-ii
title: 'Basic Calculator'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
theory: plus-minus-times-and-divide
---

## Statement

`s` is an arithmetic expression with non-negative whole numbers, the operators `+`, `-`, `*`, `/` and optional spaces. There are **no brackets**. Multiplication and division come before addition and subtraction; division of whole numbers **truncates toward zero**. Return the value.

For `"3+2*2"` the answer is `7`; for `" 3/2 "` it is `1`.

### Examples

**Example 1**

Input:

```python
calculate('3+2*2')
```

Output:

```text
7
```

**Example 2**

Input:

```python
calculate(' 3/2 ')
```

Output:

```text
1
```

### Constraints

- `1 <= len(s) <= 100000`
- The expression is valid, never divides by zero, and every intermediate value fits in 64 bits.

## Explanation

Keep `total`, the sum of finished terms, and `last`, the term being built. A `+` or `-` finishes the previous term (adds `last` to `total`) and starts a new one with the sign applied. A `*` or `/` changes `last` straight away, which is why they bind tighter. Division truncates toward zero, which is done on the absolute value. At the end, `total + last` is the answer; a sentinel `+` after the string flushes the last number.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line            | Variables                      |
| -------------------------- | ------------------------------ |
| `total = last = num = 0`   | `total = 0, last = 0, num = 0` |
| `num = num * 10 + int(ch)` | `num = 3, op = '+', ch = '3'`  |
| `num = 0`                  | `last = 3, num = 0, ch = '+'`  |
| `for ch in s + "+":`       | `num = 2, ch = '*'`            |
| `last = num`               | `total = 3, last = 2`          |
| `for ch in s + "+":`       | `num = 0, op = '*', ch = '2'`  |
| `last *= num`              | `last = 4, num = 2, ch = '+'`  |
| `return`                   | `returned = 7`                 |

### Complexity

- Time: O(n). One pass; multiplication and division are folded into the last term, and additions are summed on the fly.
- Space: O(1). A few integers.
