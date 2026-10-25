---
name: sheet-longest-palindromic-substring
title: 'Longest Palindromic Substring'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Advanced
---

## Statement

Return the **longest palindromic substring** of `s`: the longest run of consecutive characters that reads the same forwards and backwards. If several have the same length, return the one that starts **earliest**. An empty string gives `""`.

The starter code checks every substring. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
longest_palindromic_substring('babad')
```

Output:

```text
'bab'
```

**Explanation:** Longest palindromes are "bab" and "aba" (length 3); "bab" starts earlier so it is returned.

`bab` and `aba` both work; `bab` starts first.

**Example 2**

Input:

```python
longest_palindromic_substring('cbbd')
```

Output:

```text
'bb'
```

**Explanation:** The only palindrome of length 2 is "bb", so it is the longest.

`bb`.

### Constraints

- `0 <= len(s) <= 1000`
- `s` contains lower-case letters.

## Theory

Checking every substring is `O(n²)` substrings times `O(n)` for each check: `O(n³)`. Use the structure of a palindrome instead: it is **symmetric around its centre**. So grow outwards from every possible centre and stop at the first mismatch.

A palindrome of odd length has a character as its centre; one of even length has a gap between two characters. That is `2n - 1` centres in total. From each centre, extend `left` and `right` while the characters match. Each expansion costs up to `O(n)`, so the total is `O(n²)`, which is fine for `n = 1000`.

There is an `O(n)` algorithm (Manacher's), but expanding around centres is the one to write first. Visiting centres from left to right and replacing the best only on a **strictly longer** palindrome keeps the leftmost one on ties.

## Explanation

For each of the `2n - 1` centres compute the starting `left` and `right` (equal for odd centres, adjacent for even ones) and expand while the characters match. The palindrome found has length `right - left - 1` and starts at `left + 1`. Only a strictly longer palindrome replaces the best.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                    |
| --------------------------- | ---------------------------------------------------------------------------- |
| `n = len(s)`                | `n = 5`                                                                      |
| `length = right - left - 1` | `best_start = 0, best_len = 0, center = 0, left = -1, right = 1, length = 1` |
| `left -= 1`                 | `best_len = 1, center = 2, left = 0, length = 0`                             |
| `left = center // 2`        | `best_len = 3, center = 3, left = 1, right = 3, length = 3`                  |
| `right += 1`                | `center = 4, length = 0`                                                     |
| `length = right - left - 1` | `center = 5, left = 2`                                                       |
| `left = center // 2`        | `center = 7, left = 3, right = 4, length = 1`                                |
| `return`                    | `returned = 'bab'`                                                           |

### Complexity

- Time: O(n^2) n = length of s.
- Extra space: O(1) extra space.
- The brute force takes O(n^3) n = length of s.
