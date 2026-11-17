---
name: sheet-multiply-strings
title: 'Multiply Big Numbers'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Advanced
theory: schoolbook-multiplication
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

## Explanation

`sys.set_int_max_str_digits(0)` removes the 4300-digit limit, then `str(int(a) * int(b))` multiplies and converts back. CPython uses Karatsuba multiplication for big numbers, so even 20,000 digits is fast.

### Complexity

- Time: O(n^1.585 + n^2). Converting `n`-digit strings to and from integers is quadratic in CPython, and the multiplication itself uses Karatsuba, `O(n^1.585)`.
- Space: O(n). The two integers and the result string.
