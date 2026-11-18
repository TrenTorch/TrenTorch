---
name: sheet-euler-totient
title: 'Euler's Totient Function'
tags: [dsa-sheet, maths, number-theory]
difficulty: Advanced
theory: euler-s-totient-function
---

## Statement

Return `phi(n)`, the **number of integers `k` with `1 <= k <= n` and `gcd(k, n) = 1`** (numbers that share no prime factor with `n`).

For `n = 12` the answer is `4` (`1, 5, 7, 11`).

The starter code computes a gcd for every number up to `n`. It is correct but far too slow for large `n`.

### Examples

**Example 1**

Input:

```python
euler_phi(12)
```

Output:

```text
4
```

**Example 2**

Input:

```python
euler_phi(1)
```

Output:

```text
1
```

### Constraints

- `1 <= n <= 10**12`

## Explanation

`result -= result // p` multiplies the result by `(1 - 1/p)` exactly (the division is exact at that moment).

### Complexity

- Time: O(sqrt(n)). Trial division finds each distinct prime factor `p`, and `result -= result // p` applies `n * (1 - 1/p)` exactly.
- Space: O(1). A few integers.
