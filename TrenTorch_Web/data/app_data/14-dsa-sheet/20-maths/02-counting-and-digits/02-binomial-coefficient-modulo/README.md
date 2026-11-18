---
name: sheet-binomial-coefficient-modulo
title: 'Binomial Coefficient Modulo a Prime'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
theory: factorials-and-binomial-coefficients
---

## Statement

Return the **binomial coefficient** `C(n, k)` (the number of ways to choose `k` items out of `n`) modulo `10**9 + 7`. It is `0` when `k < 0` or `k > n`.

For `n = 5` and `k = 2` the answer is `10`.

The starter code builds the exact number, which becomes enormous. It is correct but too slow when `k` is large.

### Examples

**Example 1**

Input:

```python
binomial_mod(5, 2)
```

Output:

```text
10
```

**Example 2**

Input:

```python
binomial_mod(4, 5)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 10**9`
- `-1 <= k <= n` and `min(k, n - k) <= 10**6`

## Explanation

Both products are reduced modulo `p` at every step so they never grow. One `pow` at the end turns the division into a multiplication.

### Complexity

- Time: O(k + log mod). With `k = min(k, n - k)`, the product of `k` terms is built in a loop, then one modular inverse by fast exponentiation.
- Space: O(1). A few integers.
