---
name: sheet-count-primes
title: 'Count Primes'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
theory: counting-primes-with-the-sieve
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

## Explanation

`sieve[i]` is 1 while `i` may be prime. For each prime `i` up to `sqrt(n)`, the whole slice of its multiples is cleared at once. The answer is the sum of the remaining ones.

### Complexity

- Time: O(n log log n). Sieve of Eratosthenes: for each prime `p` up to `sqrt(n)` one slice assignment crosses out its multiples, and the work adds up to `n * (1/2 + 1/3 + 1/5 + ...)`.
- Space: O(n). A byte per number.
