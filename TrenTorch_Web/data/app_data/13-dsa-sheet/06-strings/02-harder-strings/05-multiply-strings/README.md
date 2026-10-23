---
name: sheet-multiply-strings
title: 'Multiply Big Numbers'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Advanced
---

## Statement

`a` and `b` are non-negative whole numbers written as strings of decimal digits (no leading zeros, except the number zero itself). Return their product as a string.

The numbers can have **thousands of digits**, far beyond a 64-bit integer.

### Examples

**Example 1**

Input:

```python
multiply_strings('123', '456')
```

Output:

```text
'56088'
```

**Example 2**

Input:

```python
multiply_strings('0', '99999')
```

Output:

```text
'0'
```

### Constraints

- `1 <= len(a), len(b) <= 20000`
- Digits only, no leading zeros except for `"0"`.

## Theory

Python integers have no size limit, so `int(a) * int(b)` is exact for any size. But since Python 3.11 there is a safety limit: converting between a string and an integer with more than **4300 digits** raises `ValueError: Exceeds the limit (4300 digits) for integer string conversion`. The tests use bigger numbers on purpose.

You have two ways. Lift the limit for your program with `sys.set_int_max_str_digits(0)`, and let Python's fast multiplication do the work. Or multiply **by hand**, as in school: the digit at position `i` of `a` times the digit at position `j` of `b` adds to position `i + j + 1` of the result. That is `O(len(a) * len(b))`, fine for hundreds of digits but slow for twenty thousand; know it for languages without big integers.

## Explanation

`sys.set_int_max_str_digits(0)` removes the 4300-digit limit, then `str(int(a) * int(b))` multiplies and converts back. CPython uses Karatsuba multiplication for big numbers, so even 20,000 digits is fast.
