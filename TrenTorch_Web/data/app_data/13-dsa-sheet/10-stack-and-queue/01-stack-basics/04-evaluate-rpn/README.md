---
name: sheet-evaluate-rpn
title: 'Evaluate Reverse Polish Notation'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
---

## Statement

`tokens` is an arithmetic expression in **reverse Polish notation** (the operator comes after its two operands): `["2", "1", "+", "3", "*"]` means `(2 + 1) * 3 = 9`. Operators are `+`, `-`, `*` and `/`. Division **truncates toward zero** (`7 / -2 = -3`). Return the value.

### Examples

**Example 1**

Input:

```python
evaluate_rpn(['2', '1', '+', '3', '*'])
```

Output:

```text
9
```

**Example 2**

Input:

```python
evaluate_rpn(['4', '13', '5', '/', '+'])
```

Output:

```text
6
```

### Constraints

- `1 <= len(tokens) <= 100000`
- The expression is valid and never divides by zero.
- Every intermediate value fits in 64 bits.

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

In postfix notation, no brackets or precedence are needed. Read the tokens left to right: a number is **pushed**; an operator **pops the top two numbers**, applies the operation and **pushes the result**. At the end, one number is left.

Watch the order: the first number popped is the **right** operand. For `-` and `/` this matters: with `a b -` you compute `a - b`, where `b` is popped first.

Python's `//` rounds toward negative infinity, but this question wants truncation toward zero: use `int(a / b)` (safe for the sizes here) or fix the sign by hand.

## Explanation

`b = stack.pop()` comes first, then `a = stack.pop()`. Division uses `int(a / b)` only when both are small enough for float division to be exact; here an integer-only test avoids precision loss: `q = abs(a) // abs(b)`, negated if the signs differ.
