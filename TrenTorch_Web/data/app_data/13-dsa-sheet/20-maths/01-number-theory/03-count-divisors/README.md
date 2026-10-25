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

**Explanation:** n = 36 has nine divisors: 1, 2, 3, 4, 6, 9, 12, 18, 36.

**Example 2**

Input:

```python
count_divisors(1)
```

Output:

```text
1
```

**Explanation:** The only divisor of 1 is 1 itself, so the count is 1.

### Constraints

- `1 <= n <= 10**12`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Divisors come in **pairs** `(d, n / d)`: one of the two is at most `sqrt(n)`. So loop `d` from 1 to `sqrt(n)`; each `d` that divides `n` gives two divisors, except when `d * d == n` (a single one). That is `O(sqrt(n))`, 1,000,000 steps for `10^12`.

Better: from the prime factorization `n = p1^e1 × p2^e2 × ...`, a divisor chooses an exponent from `0` to `ei` for each prime independently, so the count is **`(e1 + 1) × (e2 + 1) × ...`**.

## Explanation

The loop counts divisors by pairs: both `d` and `n // d`, unless they are the same number.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                   | Variables          |
| --------------------------------- | ------------------ |
| `count = 0`                       | `count = 0`        |
| `count += 1 if d * d == n else 2` | `count = 2, d = 1` |
| `count += 1 if d * d == n else 2` | `count = 4, d = 2` |
| `count += 1 if d * d == n else 2` | `count = 6, d = 3` |
| `d += 1`                          | `d = 4`            |
| `d += 1`                          | `count = 8, d = 5` |
| `count += 1 if d * d == n else 2` | `count = 9, d = 6` |
| `return`                          | `returned = 9`     |

### Complexity

- Time: O(sqrt(n)) n maximum input.
- Extra space: O(1) constant additional memory.
- The brute force takes O(n) n maximum input.
