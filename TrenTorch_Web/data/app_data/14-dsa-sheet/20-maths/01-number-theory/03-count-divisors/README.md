---
name: sheet-count-divisors
title: 'Count the Divisors'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
theory: counting-the-divisors-from-the-factors
---

## Statement

Return the **number of positive divisors** of `n` (including 1 and `n`).

For `n = 36` the answer is `9` (`1, 2, 3, 4, 6, 9, 12, 18, 36`).

The starter code tests every number up to `n`. It is correct but far too slow for large `n`.

### Examples

**Example 1**

Input:

```python
count_divisors(36)
```

Output:

```text
9
```

**Example 2**

Input:

```python
count_divisors(1)
```

Output:

```text
1
```

### Constraints

- `1 <= n <= 10**12`

## Explanation

The loop counts divisors by pairs: both `d` and `n // d`, unless they are the same number.

### Complexity

- Time: O(sqrt(n)). Every divisor `d <= sqrt(n)` pairs with `n / d`, so testing the numbers up to `sqrt(n)` finds them all.
- Space: O(1). A counter.
