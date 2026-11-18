---
name: sheet-exact-isqrt
title: 'Exact Square Root'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: maths-helpers-and-big-numbers
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

## Explanation

`math.isqrt` is exact for all sizes. A hand-written alternative is binary search over `r` between `0` and `n`, comparing `r * r` with `n`: about `log₂ n` (roughly 700) steps for a 200-digit number.

### Complexity

- Time: O(M(b)). `math.isqrt` is a Newton-style routine whose cost is about one `b`-bit multiplication, where `b` is the bit length of `n` (at most about 665 here).
- Space: O(b). A few `b`-bit integers.
