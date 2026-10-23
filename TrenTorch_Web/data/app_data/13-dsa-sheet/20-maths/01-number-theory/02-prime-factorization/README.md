---
name: sheet-prime-factorization
title: 'Prime Factorization'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
---

## Statement

Write `n` as a product of primes and return the list of `[prime, exponent]` pairs in increasing order of the prime. For `n = 1` return an empty list.

For `n = 360` the answer is `[[2, 3], [3, 2], [5, 1]]` (`360 = 2³ × 3² × 5`).

### Examples

**Example 1**

Input:

```python
prime_factors(360)
```

Output:

```text
[[2, 3], [3, 2], [5, 1]]
```

**Example 2**

Input:

```python
prime_factors(1)
```

Output:

```text
[]
```

### Constraints

- `1 <= n <= 10**12`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

**Trial division up to the square root.** Divide out `2` as many times as possible, then try the odd numbers `3, 5, 7, ...` while `d * d <= n`; every time `d` divides `n`, count how many times and divide it out. After the loop, if `n > 1`, what is left is **one prime factor larger than the square root** (there can be at most one).

Dividing as you go makes `n` smaller, so the stopping point `d * d <= n` comes earlier. The worst case is a large prime: about `sqrt(n) / 2` steps, which is 500,000 for `10^12`.

## Explanation

The loop condition `d * d <= n` uses the current (shrinking) `n`. A leftover `n > 1` is the last prime factor.
