---
name: sheet-factorial-digit-sum
title: 'Digit Sum of a Factorial'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
---

## Statement

Return the sum of the decimal digits of `n!` (`n` factorial: `1 * 2 * ... * n`, with `0! = 1`).

For example `10! = 3628800`, and its digit sum is `3 + 6 + 2 + 8 + 8 + 0 + 0 = 27`.

### Examples

**Example 1**

Input:

```python
factorial_digit_sum(10)
```

Output:

```text
27
```

`10! = 3628800`.

**Example 2**

Input:

```python
factorial_digit_sum(0)
```

Output:

```text
1
```

`0! = 1`.

### Constraints

- `0 <= n <= 10000`
- `10000!` has about 35,000 digits.

## Theory

`math.factorial(n)` computes the exact value, even when it is huge, because Python integers are unlimited. The digits are a different story: since Python 3.11, converting an integer with more than **4300 digits** to a string raises `ValueError: Exceeds the limit (4300 digits) for integer string conversion`. This is a protection against slow, attacker-controlled conversions.

You have two ways around it. You can lift the limit for your program with `sys.set_int_max_str_digits(0)`. Or you can avoid strings completely and peel off digits with `divmod(x, 10)`, which is slower per digit but never hits the limit. Competitive programmers on Python 3.11+ meet this limit sooner or later, so it is worth knowing.

## Explanation

Compute `math.factorial(n)`, lift the string limit with `sys.set_int_max_str_digits(0)`, then add the digits of `str(value)`.

Without that line, any `n` above about 1,800 fails, because `1800!` already has more than 4,300 digits.
