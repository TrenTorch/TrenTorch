---
name: sheet-sum-of-divisor-counts
title: 'Sum of the Number of Divisors'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Mastery
theory: grouping-equal-quotients
---

## Statement

Let `d(k)` be the number of positive divisors of `k`. Return `d(1) + d(2) + ... + d(n)`.

For `n = 5` the answer is `10` (`1 + 2 + 2 + 3 + 2`).

The starter code does one step for each number up to `n`. It is correct but too slow for large `n`.

### Examples

**Example 1**

Input:

```python
sum_divisor_counts(5)
```

Output:

```text
10
```

**Example 2**

Input:

```python
sum_divisor_counts(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 10**12`

## Explanation

`r = isqrt(n)`; the sum runs over `j <= r`. Doubling it counts each pair `(j, m)` once from each side, and subtracting `r × r` removes the pairs counted twice.

### Complexity

- Time: O(sqrt(n)). The number of pairs `(i, j)` with `i * j <= n` is counted by the hyperbola trick: sum `n // j` up to `sqrt(n)`, double it and subtract the overlap.
- Space: O(1). A few integers.
