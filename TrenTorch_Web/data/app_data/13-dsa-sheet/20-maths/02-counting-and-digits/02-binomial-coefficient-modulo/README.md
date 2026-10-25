---
name: sheet-binomial-coefficient-modulo
title: 'Binomial Coefficient Modulo a Prime'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
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

**Explanation:** When n is 5 and k is 2, C(5,2) equals 10, which fits under the modulus 10^9+7, so output stays 10.

**Example 2**

Input:

```python
binomial_mod(4, 5)
```

Output:

```text
0
```

**Explanation:** When n is 4 and k is 5, k exceeds n, so binomial coefficient is defined as 0.

### Constraints

- `0 <= n <= 10**9`
- `-1 <= k <= n` and `min(k, n - k) <= 10**6`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

`C(n, k) = n × (n - 1) × ... × (n - k + 1) / k!`. The numbers are huge, but we only want the remainder modulo a **prime** `p = 10**9 + 7`. Division is not allowed in modular arithmetic; instead multiply by the **modular inverse**. Since `p` is prime, Fermat's little theorem gives the inverse of `x` as `x^(p-2) mod p`, computed with `pow(x, p - 2, p)`.

So: numerator `= Π (n - i) mod p`, denominator `= k! mod p`, answer `= numerator × pow(denominator, p - 2, p) mod p`. Use `k = min(k, n - k)` to keep the loop short. This needs `n < p`, which holds here. `O(k)`.

## Explanation

Both products are reduced modulo `p` at every step so they never grow. One `pow` at the end turns the division into a multiplication.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables          |
| ----------------------------------- | ------------------ |
| `mod = 10**9 + 7`                   | `mod = 1000000007` |
| `num = den = 1`                     | `num = 1, den = 1` |
| `for i in range(k):`                | `i = 0`            |
| `num = num * ((n - i) % mod) % mod` | `num = 5`          |
| `for i in range(k):`                | `i = 1`            |
| `num = num * ((n - i) % mod) % mod` | `num = 20`         |
| `den = den * (i + 1) % mod`         | `den = 2`          |
| `return`                            | `returned = 10`    |

### Complexity

- Time: O(k), where k is min(k, n-k).
- Extra space: O(1).
- The brute force takes O(n) for computing factorials.
