---
name: sheet-sum-of-divisor-counts
title: 'Sum of the Number of Divisors'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Mastery
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

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Count **pairs `(k, j)` with `j` dividing `k`**, `k <= n`, from the other side: a number `j` divides exactly `n // j` numbers up to `n` (its multiples). So the answer is `sum of n // j` for `j = 1..n`.

That is still `n` terms. The values `n // j` take only about `2·sqrt(n)` different values, because for `j > sqrt(n)` the quotient is below `sqrt(n)`. Use **symmetry**: the pairs `(j, m)` with `j × m <= n` can be counted by the smaller factor: `answer = 2 × sum of n // j for j <= sqrt(n)  -  floor(sqrt(n))²` (the square of pairs where both factors are at most the root was counted twice). `O(sqrt(n))`.

## Explanation

`r = isqrt(n)`; the sum runs over `j <= r`. Doubling it counts each pair `(j, m)` once from each side, and subtracting `r × r` removes the pairs counted twice.
