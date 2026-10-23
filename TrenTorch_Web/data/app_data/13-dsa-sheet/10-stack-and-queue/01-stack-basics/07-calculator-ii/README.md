---
name: sheet-calculator-ii
title: 'Basic Calculator'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
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

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Precedence is the difficulty: `2*3` must be done before it is added to something. A stack of **terms** solves it. Read number by number, remembering the operator that came **before** the number:

- `+`: push the number.
- `-`: push the negative of the number.
- `*` or `/`: pop the last term, combine it with the number, push the result.

At the end, the answer is the **sum of the stack**: all the terms of the sum. Multiplication and division were done immediately because they bind tighter and always belong to the term just pushed.

Trick: process the number when you reach the next operator or the end of the string, so add a sentinel `+` at the end.

## Explanation

`op` is the operator before the current number. Digits are collected into `num`; at an operator or at the end the number is applied according to `op`. Division uses an integer-only truncation toward zero.
