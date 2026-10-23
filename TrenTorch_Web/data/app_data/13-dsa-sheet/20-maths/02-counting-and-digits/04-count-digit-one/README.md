---
name: sheet-count-digit-one
title: 'Count the Digit One'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Mastery
---

## Statement

Return the **total number of times the digit `1` appears** when you write all the numbers from `1` to `n`.

For `n = 13` the answer is `6` (`1, 10, 11` (two), `12, 13`).

The starter code looks at the digits of every number. It is correct but too slow for large `n`.

### Examples

**Example 1**

Input:

```python
count_digit_one(13)
```

Output:

```text
6
```

**Example 2**

Input:

```python
count_digit_one(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 9 * 10**15`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Count position by position. Take the digit position with place value `p` (1, 10, 100, ...). Split `n` into `high = n // (10p)`, `cur = (n // p) % 10`, and `low = n % p`. How many numbers up to `n` have a `1` at this position?

- `high × p` numbers from the complete blocks of `10p` numbers before the last (each block has `p` numbers with a 1 here);
- plus a partial last block: if `cur > 1`, another full `p`; if `cur == 1`, `low + 1`; if `cur == 0`, nothing.

Add this up for every position: about 16 positions for `n` up to `9 × 10^15`. This **digit counting** idea is the foundation of "digit DP".

## Explanation

`high * p` counts the full blocks; the `if/elif` adds the partial block depending on the current digit.
