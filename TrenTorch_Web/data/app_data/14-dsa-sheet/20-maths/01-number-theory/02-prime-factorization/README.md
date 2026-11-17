---
name: sheet-prime-factorization
title: 'Prime Factorization'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
theory: writing-a-number-as-a-product-of-primes
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

## Explanation

The loop condition `d * d <= n` uses the current (shrinking) `n`. A leftover `n > 1` is the last prime factor.

### Complexity

- Time: O(sqrt(n)). Trial division by 2 and then odd numbers up to `sqrt(n)`; `n` shrinks as factors are removed. (Pollard's rho needs only about `n^(1/4)` steps, but trial division is the standard method and fast enough here).
- Space: O(log n). The factors found (at most about 40 pairs).
