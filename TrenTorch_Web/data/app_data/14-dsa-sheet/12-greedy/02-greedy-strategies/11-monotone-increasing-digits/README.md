---
name: sheet-monotone-increasing-digits
title: 'Largest Number With Non-Decreasing Digits'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
theory: largest-number-with-rising-digits
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

## Explanation

`mark` is the position from which the digits become 9. Scanning from the right lets earlier drops cascade correctly (a decreased digit may now be larger than its left neighbour).

### Complexity

- Time: O(d). `d` is the number of digits of `n`: two passes over the digits.
- Space: O(d). The list of digits.
