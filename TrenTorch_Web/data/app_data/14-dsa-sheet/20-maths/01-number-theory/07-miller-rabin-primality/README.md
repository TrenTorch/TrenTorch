---
name: sheet-miller-rabin-primality
title: 'Is It Prime? (Large Numbers)'
tags: [dsa-sheet, maths, number-theory]
difficulty: Mastery
theory: the-stronger-test
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

## Explanation

The loop squares `x` up to `s - 1` times looking for `-1 mod n`. If no base finds a witness, `n` is prime.

### Complexity

- Time: O(12 log^2 n). Twelve fixed bases are enough to be exact for every `n` below 3.3 * 10^24, and each base needs `log n` modular squarings.
- Space: O(1). A few integers.
