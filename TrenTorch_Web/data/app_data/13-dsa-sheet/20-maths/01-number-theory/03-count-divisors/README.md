---
name: sheet-count-divisors
title: 'Count the Divisors'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
---

## Statement

Return the **number of positive divisors** of `n` (including 1 and `n`).

For `n = 36` the answer is `9` (`1, 2, 3, 4, 6, 9, 12, 18, 36`).

The starter code tests every number up to `n`. It is correct but far too slow for large `n`.

### Examples

**Example 1**

Input:

```python
count_divisors(36)
```

Output:

```text
9
```

**Example 2**

Input:

```python
count_divisors(1)
```

Output:

```text
1
```

### Constraints

- `1 <= n <= 10**12`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Divisors come in **pairs** `(d, n / d)`: one of the two is at most `sqrt(n)`. So loop `d` from 1 to `sqrt(n)`; each `d` that divides `n` gives two divisors, except when `d * d == n` (a single one). That is `O(sqrt(n))`, 1,000,000 steps for `10^12`.

Better: from the prime factorization `n = p1^e1 × p2^e2 × ...`, a divisor chooses an exponent from `0` to `ei` for each prime independently, so the count is **`(e1 + 1) × (e2 + 1) × ...`**.

## Explanation

The loop counts divisors by pairs: both `d` and `n // d`, unless they are the same number.
