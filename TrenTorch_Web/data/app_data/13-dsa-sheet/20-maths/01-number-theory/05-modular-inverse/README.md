---
name: sheet-modular-inverse
title: 'Modular Inverse'
tags: [dsa-sheet, maths, number-theory]
difficulty: Advanced
---

## Statement

Return the number `x` with `0 <= x < m` such that `(a * x) % m == 1`, the **modular inverse** of `a` modulo `m`. If there is no such `x`, return `-1`. For `m = 1` the answer is `0`.

For `a = 3` and `m = 11` the answer is `4` (`3 × 4 = 12 = 1 mod 11`); for `a = 2` and `m = 4` it is `-1`.

### Examples

**Example 1**

Input:

```python
mod_inverse(3, 11)
```

Output:

```text
4
```

**Example 2**

Input:

```python
mod_inverse(2, 4)
```

Output:

```text
-1
```

### Constraints

- `1 <= m <= 10**9 + 7`
- `0 <= a <= 10**18`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

The inverse exists exactly when `gcd(a, m) = 1`. To find it, the **extended Euclidean algorithm** finds integers `x, y` with `a·x + m·y = gcd(a, m)`; when the gcd is 1, `a·x ≡ 1 (mod m)`, so `x mod m` is the inverse.

Iteratively: keep pairs `(old_r, r)` and `(old_x, x)`, start with `(a, m)` and `(1, 0)`; repeat `q = old_r // r` and update both pairs (`old_r, r = r, old_r - q·r`, `old_x, x = x, old_x - q·x`) until `r == 0`. Then `old_r` is the gcd and `old_x` the coefficient. `O(log m)` steps.

(For a prime modulus there is also Fermat's trick `a^(m-2) mod m`, via fast power.)

## Explanation

The invariant is `old_r ≡ old_x × a (mod m)`. When the loop ends, `old_r` is the gcd; a gcd other than 1 means no inverse.
