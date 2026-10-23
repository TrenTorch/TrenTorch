---
name: sheet-chinese-remainder-theorem
title: 'Chinese Remainder Theorem'
tags: [dsa-sheet, maths, number-theory]
difficulty: Mastery
---

## Statement

You are given conditions `x ≡ remainders[i] (mod moduli[i])`, that is, `x % moduli[i] == remainders[i] % moduli[i]`. The moduli do **not** have to be coprime. Return the **smallest non-negative `x`** that satisfies all of them, or `-1` if there is none. With no conditions the answer is `0`.

For `remainders = [2, 3, 2]` and `moduli = [3, 5, 7]` the answer is `23`.

The starter code tries the numbers one by one up to the least common multiple. It is correct but too slow when the moduli are large.

### Examples

**Example 1**

Input:

```python
solve_congruences([2, 3, 2], [3, 5, 7])
```

Output:

```text
23
```

**Example 2**

Input:

```python
solve_congruences([1, 2], [4, 6])
```

Output:

```text
-1
```

### Constraints

- `0 <= len(moduli) == len(remainders) <= 20`
- `1 <= moduli[i] <= 10000`, `0 <= remainders[i] <= 10**9`
- The least common multiple of the moduli is at most `10**12`.

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Combine the conditions **two at a time**. Suppose you know `x ≡ x0 (mod m0)` and add `x ≡ r (mod m)`. Write `x = x0 + m0·t` and solve `m0·t ≡ r - x0 (mod m)`. Let `g = gcd(m0, m)`.

- If `g` does not divide `r - x0`, the two conditions contradict each other: the answer is `-1`.
- Otherwise divide everything by `g`: `t ≡ ((r - x0) / g) × inverse(m0 / g) (mod m / g)`. The inverse exists because `m0/g` and `m/g` are coprime.

Then `x ≡ x0 + m0·t` modulo `lcm(m0, m)`, which is the new pair `(x0, m0)`. Fold over all conditions. Python's `pow(a, -1, m)` computes the inverse.

## Explanation

`x` and `modulus` always describe the solutions found so far as `x mod modulus`. Each step either detects a contradiction or merges one more condition.
