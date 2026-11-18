---
name: sheet-factorial-digit-sum
title: 'Digit Sum of a Factorial'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
theory: maths-helpers-and-big-numbers
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

## Explanation

Compute `math.factorial(n)`, lift the string limit with `sys.set_int_max_str_digits(0)`, then add the digits of `str(value)`.

Without that line, any `n` above about 1,800 fails, because `1800!` already has more than 4,300 digits.

### Complexity

- Time: O(n log n + d^2). `math.factorial` multiplies in a balanced way; turning the `d`-digit number (`d` is about `n log10(n)`) into a decimal string is quadratic in CPython.
- Space: O(d). The `d`-digit number and its string.
