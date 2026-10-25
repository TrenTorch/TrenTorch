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

**Explanation:** All single letters, pairs, and the whole string are palindromes.

**Example 2**

Input:

```python
count_palindromes_fast('abc')
```

Output:

```text
3
```

**Explanation:** Only single letters are palindromes; each counts once.

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Expanding around each of the `2n - 1` centres costs `O(n)` per centre on a string like `aaaa...`, so `O(n²)` overall.

**Manacher's algorithm** reuses mirror images. Keep the palindrome `[l, r]` that reaches furthest to the right. For a new centre `i` inside it, its mirror position `j = l + r - i` has already been computed, and `i` has **at least** the same radius (capped at the distance to `r`). Only expand beyond `r` by comparing letters, and every expansion moves `r` to the right, so the total work is `O(n)`.

Do it twice: `d1[i]` = number of odd-length palindromes centred at `i`, `d2[i]` = number of even-length palindromes centred between `i - 1` and `i`. The answer is the sum of both arrays.

## Explanation

`d1[i]` counts the odd palindromes with centre `i` (the radius including the centre itself); `d2[i]` counts the even ones. Each loop keeps the window `[left, right]` of the rightmost palindrome.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                        | Variables                                                       |
| ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| `n = len(s)`                                                           | `n = 3`                                                         |
| `k = 1 if i > right else min(d1[left + right - i], right - i + 1)`     | `total = 0, d1 = [0, 0, 0], left = 0, right = -1, i = 0, k = 1` |
| `for i in range(n):`                                                   | `total = 1, d1 = [1, 0, 0], right = 0, i = 1`                   |
| `for i in range(n):`                                                   | `total = 3, d1 = [1, 2, 0], right = 2, i = 2, k = 2`            |
| `left, right = 0, -1`                                                  | `total = 4, d1 = [1, 2, 1], right = -1, k = 1, d2 = [0, 0, 0]`  |
| `d2[i] = k`                                                            | `i = 1, d2 = [0, 1, 0]`                                         |
| `k = 0 if i > right else min(d2[left + right - i + 1], right - i + 1)` | `total = 5, right = 1, i = 2, k = 0`                            |
| `return`                                                               | `returned = 6`                                                  |

### Complexity

- Time: O(n), n is length of s.
- Extra space: O(n), arrays of size n.
- The brute force takes O(n^2), 2n-1 centers, expand each.
