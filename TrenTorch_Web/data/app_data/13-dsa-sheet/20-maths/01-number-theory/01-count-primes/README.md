---
name: sheet-count-primes
title: 'Count Primes'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
---

## Statement

Return the number of **prime numbers strictly less than `n`**. A prime has exactly two divisors, 1 and itself.

For `n = 10` the answer is `4` (`2, 3, 5, 7`).

The starter code tests every number by trial division. It is correct but too slow for large `n`.

### Examples

**Example 1**

Input:

```python
count_primes(10)
```

Output:

```text
4
```

**Example 2**

Input:

```python
count_primes(2)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 2000000`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

The **sieve of Eratosthenes** finds all primes below `n` at once. Make a table of booleans, all true. Walk `i` from 2: if `i` is still marked prime, mark all its multiples `i*i, i*i + i, ...` as not prime (smaller multiples were already marked by smaller primes). You only need `i` up to `sqrt(n)`.

The total work is `O(n log log n)`, almost linear. In Python use a `bytearray` and **slice assignment** (`sieve[i*i::i] = bytes(count)`) so the marking runs in C.

## Explanation

`sieve[i]` is 1 while `i` may be prime. For each prime `i` up to `sqrt(n)`, the whole slice of its multiples is cleared at once. The answer is the sum of the remaining ones.
