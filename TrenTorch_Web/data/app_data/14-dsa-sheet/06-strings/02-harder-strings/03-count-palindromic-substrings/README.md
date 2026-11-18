---
name: sheet-count-palindromic-substrings
title: 'Count Palindromic Substrings'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
theory: counting-all-palindromic-substrings
---

## Statement

Return how many **substrings** of `s` are palindromes. Substrings at different positions count separately, even if they hold the same characters (`"aaa"` has 6: three `a`, two `aa` and one `aaa`).

The starter code checks every substring. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
count_palindromic_substrings('abc')
```

Output:

```text
3
```

Only the three single letters.

**Example 2**

Input:

```python
count_palindromic_substrings('aaa')
```

Output:

```text
6
```

`a` three times, `aa` twice, `aaa` once: 6.

### Constraints

- `0 <= len(s) <= 1000`
- `s` contains lower-case letters.

## Explanation

Manacher's algorithm (see the longest palindromic substring) gives, for every centre of the string with separators, the radius `p` of the longest palindrome around it. That centre is the middle of exactly `(p + 1) // 2` palindromic substrings: the radii `1, 3, 5, ...` for a character centre, and `2, 4, ...` for a gap centre. The answer is the sum over all centres.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                                                      |
| ---------------------------------- | -------------------------------------------------------------- |
| `t = "#" + "#".join(s) + "#"`      | `t = '#a#b#c#'`                                                |
| `radius = [0] * n`                 | `n = 7, radius = [0, 0, 0, 0, 0, 0, 0]`                        |
| `for i in range(n):`               | `centre = 0, right = 0, i = 1`                                 |
| `centre, right = i, i + radius[i]` | `radius = [0, 1, 0, 0, 0, 0, 0], centre = 1, right = 2`        |
| `radius[i] += 1`                   | `radius = [0, 1, 0, 1, 0, 0, 0], i = 3`                        |
| `for i in range(n):`               | `centre = 3, right = 4, i = 4`                                 |
| `centre, right = i, i + radius[i]` | `radius = [0, 1, 0, 1, 0, 1, 0], centre = 5, right = 6, i = 5` |
| `return`                           | `returned = 3`                                                 |

### Complexity

- Time: O(n). Manacher's algorithm gives the palindrome radius at every centre in linear time, and the count is the sum of the radii.
- Space: O(n). The radius array over the string with separators.
