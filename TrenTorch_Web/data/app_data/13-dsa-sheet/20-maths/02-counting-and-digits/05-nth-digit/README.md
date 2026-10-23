---
name: sheet-nth-digit
title: 'The Nth Digit'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
---

## Statement

Write all the positive whole numbers one after another: `123456789101112131415...`. Return the **`n`-th digit** of this endless string (counting from 1).

For `n = 11` the answer is `0` (the digits are `1 2 3 4 5 6 7 8 9 1 0 1 1 ...`).

The starter code writes the numbers until the text is long enough. It is correct but too slow, and uses too much memory, for large `n`.

### Examples

**Example 1**

Input:

```python
nth_digit(11)
```

Output:

```text
0
```

**Example 2**

Input:

```python
nth_digit(3)
```

Output:

```text
3
```

### Constraints

- `1 <= n <= 9 * 10**15`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Group the numbers by how many digits they have: 9 numbers with 1 digit (9 digits in total), 90 with 2 digits (180 digits), 900 with 3 digits (2700 digits), and in general `9 × 10^(L-1)` numbers with `L` digits, `L × 9 × 10^(L-1)` digits in total.

1. **Find the length `L`**: subtract the totals of the groups from `n` while `n` is bigger than the group.
2. **Find the number**: the first number with `L` digits is `10^(L-1)`; the digit lies in the number `10^(L-1) + (n - 1) // L`.
3. **Find the digit** inside it: index `(n - 1) % L`.

About 16 steps for `n` up to `9 × 10^15`.

## Explanation

The loop skips whole groups. Then integer division finds the number and the remainder finds the position inside it.
