---
name: sheet-fibonacci-modulo
title: 'Huge Fibonacci Number'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
---

## Statement

The Fibonacci numbers are `F(0) = 0`, `F(1) = 1`, `F(k) = F(k - 1) + F(k - 2)`. Return `F(n)` modulo `10**9 + 7`.

For `n = 10` the answer is `55`.

The starter code adds up one number at a time. It is correct but far too slow when `n` is huge.

### Examples

**Example 1**

Input:

```python
fib_mod(10)
```

Output:

```text
55
```

**Example 2**

Input:

```python
fib_mod(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 9 * 10**15`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Looping `n` times is hopeless for `n = 10^15`. The **fast doubling** identities compute `F(2k)` and `F(2k + 1)` from `F(k)` and `F(k + 1)`:

- `F(2k) = F(k) × (2·F(k + 1) - F(k))`
- `F(2k + 1) = F(k)² + F(k + 1)²`

So the pair `(F(n), F(n + 1))` can be computed from the pair for `n // 2`, one doubling step, plus one extra addition if `n` is odd. The recursion has `log₂ n` levels (about 53), each a few multiplications modulo `10**9 + 7`. The same trick is the idea of **matrix exponentiation**: the Fibonacci step is a 2×2 matrix and its power is computed by repeated squaring.

## Explanation

`pair(k)` returns `(F(k), F(k + 1))`. For odd `k` the pair is shifted by one step after doubling.
