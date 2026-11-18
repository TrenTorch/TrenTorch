---
name: sheet-longest-palindromic-substring
title: 'Longest Palindromic Substring'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Advanced
theory: the-longest-palindromic-substring
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

`bb`.

### Constraints

- `0 <= len(s) <= 1000`
- `s` contains lower-case letters.

## Explanation

Manacher's algorithm. Put a separator between every pair of characters (and at both ends) so that even and odd palindromes both have a single centre, then compute at each centre the radius of the longest palindrome around it.

The trick: keep the palindrome that reaches furthest right, with its centre `c` and right edge `r`. For a centre `i < r`, its mirror `2c - i` already has a radius, and `i` has at least `min(that radius, r - i)`; only the part beyond `r` has to be checked. The edge `r` only moves right, so the total work is linear.

The answer is the centre with the largest radius (the earliest one on a tie); its start in the original string is `(centre - radius) // 2`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                                                                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `t = "#" + "#".join(s) + "#"`          | `t = '#b#a#b#a#d#'`                                                                                               |
| `for i in range(n):`                   | `n = 11, radius = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], centre = 0, right = 0, best_len = 0, best_centre = 0, i = 0` |
| `best_len, best_centre = radius[i], i` | `radius = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], centre = 1, right = 2, best_len = 1, best_centre = 1, i = 1`         |
| `radius[i] += 1`                       | `radius = [0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0], i = 3`                                                               |
| `for i in range(n):`                   | `centre = 3, right = 6, best_len = 3, best_centre = 3, i = 5`                                                     |
| `for i in range(n):`                   | `radius = [0, 1, 0, 3, 0, 3, 0, 0, 0, 0, 0], centre = 5, right = 8, i = 6`                                        |
| `for i in range(n):`                   | `radius = [0, 1, 0, 3, 0, 3, 0, 1, 0, 0, 0], i = 9`                                                               |
| `return`                               | `returned = 'bab'`                                                                                                |

### Complexity

- Time: O(n). Manacher's algorithm: the right edge of the rightmost palindrome only moves forward, and every centre reuses the mirror centre's answer inside it.
- Space: O(n). The radius array over the string with separators.
