---
name: sheet-decode-ways
title: 'Decode Ways'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: decode-ways
---

## Statement

A message uses the code `A = 1, B = 2, ..., Z = 26`. Given a string `s` of digits, return the **number of ways to decode it** into letters (a digit group like `"06"` or `"0"` alone is not a valid code). The answer is returned modulo `10**9 + 7`.

For `"12"` the answer is `2` (`AB` or `L`); for `"226"` it is `3`; for `"06"` it is `0`.

### Examples

**Example 1**

Input:

```python
num_decodings('12')
```

Output:

```text
2
```

**Example 2**

Input:

```python
num_decodings('226')
```

Output:

```text
3
```

**Example 3**

Input:

```python
num_decodings('06')
```

Output:

```text
0
```

### Constraints

- `0 <= len(s) <= 200000`
- `s` contains only digits.

## Explanation

`a` is `ways(i - 2)` and `b` is `ways(i - 1)`. A zero digit contributes nothing alone but may still pair with the digit before it.

### Complexity

- Time: O(n). One pass; each digit pair is checked in O(1).
- Space: O(1). Two numbers.
