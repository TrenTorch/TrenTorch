---
name: sheet-exact-isqrt
title: 'Exact Square Root'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
---

## Statement

Return the integer square root of `n`: the largest integer `r` with `r * r <= n`.

`n` can have up to 200 digits.

### Examples

**Example 1**

Input:

```python
exact_isqrt(26)
```

Output:

```text
5
```

`5 * 5 = 25 <= 26 < 36`.

**Example 2**

Input:

```python
exact_isqrt(999999999999999999)
```

Output:

```text
999999999
```

A float gives `1000000000.0`, which is one too many.

### Constraints

- `0 <= n < 10**200`

## Theory

`math.sqrt(n)` and `n ** 0.5` return a **float**, which keeps only about 15-16 significant digits. For a big `n` the result is rounded, and for `n` above about `1.8 * 10³⁰⁸` it fails with an `OverflowError`. Even for `n = 10**18 - 1` the float answer rounds up to the wrong integer.

`math.isqrt(n)` works on exact integers and returns the exact floor of the square root, for any size. If you want to build it yourself, binary search on `r` works and takes `O(log n)` steps.

Rule of thumb: when the answer must be an exact integer, stay in integers.

## Explanation

`math.isqrt` is exact for all sizes. A hand-written alternative is binary search over `r` between `0` and `n`, comparing `r * r` with `n`: about `log₂ n` (roughly 700) steps for a 200-digit number.
