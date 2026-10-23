---
name: sheet-miller-rabin-primality
title: 'Is It Prime? (Large Numbers)'
tags: [dsa-sheet, maths, number-theory]
difficulty: Mastery
---

## Statement

Return `True` if `n` is a **prime number**.

For `n = 97` the answer is `True`; for `n = 91` it is `False` (`7 × 13`).

The starter code tries every divisor up to the square root. It is correct but too slow for primes near `10^15`.

### Examples

**Example 1**

Input:

```python
is_prime(97)
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_prime(91)
```

Output:

```text
False
```

### Constraints

- `0 <= n <= 9 * 10**15`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Trial division needs up to `sqrt(n)` steps: 10^7 for `n = 10^14`. The **Miller–Rabin test** answers in about 12 modular exponentiations.

Write `n - 1 = 2^s × d` with `d` odd. For a base `a`, a prime `n` must satisfy: either `a^d ≡ 1 (mod n)`, or `a^(d·2^r) ≡ -1 (mod n)` for some `r` from 0 to `s - 1`. A composite `n` usually fails this for most bases `a`. Testing a fixed set of bases is **deterministic** below a known limit: the first 12 primes (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37) are enough for every `n` below `3 × 10^24`.

Handle small `n` and multiples of the small primes first. Use `pow(a, d, n)` for the fast modular power.

## Explanation

The loop squares `x` up to `s - 1` times looking for `-1 mod n`. If no base finds a witness, `n` is prime.
