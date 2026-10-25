---
name: sheet-euler-totient
title: 'Euler's Totient Function'
tags: [dsa-sheet, maths, number-theory]
difficulty: Advanced
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

**Explanation:** For n=12 the numbers 1, 5, 7, 11 are coprime, giving 4.

**Example 2**

Input:

```python
euler_phi(1)
```

Output:

```text
1
```

**Explanation:** For n=1 only the number 1 is coprime, so the count is 1.

### Constraints

- `1 <= n <= 10**12`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Take all `n` numbers and remove those divisible by some prime factor `p` of `n`: that is a fraction `1/p` of them. Doing it for all prime factors (they are independent) leaves

**`phi(n) = n × (1 - 1/p1) × (1 - 1/p2) × ...`**

over the distinct primes `p` that divide `n`. In integers: start with `result = n` and, for each prime factor `p`, do `result -= result // p`. Factor `n` by trial division up to the square root as in the factorization question. `O(sqrt(n))`.

`phi` appears in modular arithmetic: Euler's theorem says `a^phi(n) ≡ 1 (mod n)` when `gcd(a, n) = 1`.

## Explanation

`result -= result // p` multiplies the result by `(1 - 1/p)` exactly (the division is exact at that moment).

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line           | Variables      |
| ------------------------- | -------------- |
| `result = n`              | `result = 12`  |
| `d = 2`                   | `d = 2`        |
| `n //= d`                 | `n = 6`        |
| `n //= d`                 | `n = 3`        |
| `result -= result // d`   | `result = 6`   |
| `d += 1 if d == 2 else 2` | `d = 3`        |
| `result -= result // n`   | `result = 4`   |
| `return`                  | `returned = 4` |

### Complexity

- Time: O(sqrt(n)) n is the input number.
- Extra space: O(1) constant extra memory.
- The brute force takes O(n log n) n is the input number.
