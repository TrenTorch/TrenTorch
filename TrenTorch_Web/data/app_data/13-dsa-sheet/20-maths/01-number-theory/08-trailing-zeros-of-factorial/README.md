---
name: sheet-trailing-zeros-of-factorial
title: 'Trailing Zeros of a Factorial'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
---

## Statement

Return the number of **zeros at the end of `n!`** (`n! = 1 × 2 × ... × n`).

For `n = 25` the answer is `6` (`25! = 15511210043330985984000000`).

The starter code visits every number up to `n`. It is correct but too slow for large `n`.

### Examples

**Example 1**

Input:

```python
trailing_zeros(25)
```

Output:

```text
6
```

**Example 2**

Input:

```python
trailing_zeros(5)
```

Output:

```text
1
```

### Constraints

- `0 <= n <= 9 * 10**15`

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

A trailing zero comes from a factor 10 = 2 × 5. The factorial has far more factors of 2 than of 5, so the number of zeros is the **number of factors of 5** in `1 × 2 × ... × n`.

Count them: `n // 5` numbers are multiples of 5 (one factor each), `n // 25` multiples of 25 give one **more** factor, `n // 125` one more, and so on:

**`zeros = n // 5 + n // 25 + n // 125 + ...`** (Legendre's formula). About `log₅ n` terms.

## Explanation

`n //= 5` in each round gives `n // 5`, then `n // 25`, and so on, and the terms are added up.
