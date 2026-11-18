---
name: sheet-evaluate-rpn
title: 'Evaluate Reverse Polish Notation'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
theory: operators-after-their-numbers
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

## Explanation

`b = stack.pop()` comes first, then `a = stack.pop()`. Division uses `int(a / b)` only when both are small enough for float division to be exact; here an integer-only test avoids precision loss: `q = abs(a) // abs(b)`, negated if the signs differ.

### Complexity

- Time: O(n). Each token is read once and each operator costs O(1).
- Space: O(n). The stack of operands.
