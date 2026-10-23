---
name: sheet-monotone-increasing-digits
title: 'Largest Number With Non-Decreasing Digits'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
---

## Statement

Return the **largest number that is at most `n`** and whose digits are in **non-decreasing order** from left to right (each digit is at least the one before it).

For `n = 332` the answer is `299`; for `n = 1234` it is `1234`; for `n = 10` it is `9`.

### Examples

**Example 1**

Input:

```python
monotone_increasing_digits(332)
```

Output:

```text
299
```

**Example 2**

Input:

```python
monotone_increasing_digits(10)
```

Output:

```text
9
```

### Constraints

- `0 <= n <= 10**15`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Scan the digits from left to right. If the digits are already non-decreasing, `n` itself is the answer. The first time a digit is **smaller than the one before it** (`3 3 2`: the `2`), the number is too big there. Fix it by lowering the **previous digit by 1** and setting everything after it to `9` (the largest filler, which keeps the number as big as possible): `332` becomes `3 2 9` ... but now the earlier digit may be too big for the one before it (`3 2`), so lower and fill again: `299`.

Practical method: scan **from the right**; whenever `digits[i - 1] > digits[i]`, decrease `digits[i - 1]` by 1 and remember `mark = i`; at the end set all digits from `mark` onwards to `9`. `O(number of digits)`.

## Explanation

`mark` is the position from which the digits become 9. Scanning from the right lets earlier drops cascade correctly (a decreased digit may now be larger than its left neighbour).
