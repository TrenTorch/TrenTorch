---
name: sheet-count-palindromic-substrings-manacher
title: 'Count Palindromic Substrings, Fast'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Mastery
---

## Statement

Count the **substrings of `s` that are palindromes** (substrings at different positions count separately, even if they look the same).

For `"aaa"` the answer is `6`.

The starter code expands around every centre separately. It is correct but too slow on long repetitive strings.

### Examples

**Example 1**

Input:

```python
count_palindromes_fast('aaa')
```

Output:

```text
6
```

**Example 2**

Input:

```python
count_palindromes_fast('abc')
```

Output:

```text
3
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Expanding around each of the `2n - 1` centres costs `O(n)` per centre on a string like `aaaa...`, so `O(n²)` overall.

**Manacher's algorithm** reuses mirror images. Keep the palindrome `[l, r]` that reaches furthest to the right. For a new centre `i` inside it, its mirror position `j = l + r - i` has already been computed, and `i` has **at least** the same radius (capped at the distance to `r`). Only expand beyond `r` by comparing letters, and every expansion moves `r` to the right, so the total work is `O(n)`.

Do it twice: `d1[i]` = number of odd-length palindromes centred at `i`, `d2[i]` = number of even-length palindromes centred between `i - 1` and `i`. The answer is the sum of both arrays.

## Explanation

`d1[i]` counts the odd palindromes with centre `i` (the radius including the centre itself); `d2[i]` counts the even ones. Each loop keeps the window `[left, right]` of the rightmost palindrome.
