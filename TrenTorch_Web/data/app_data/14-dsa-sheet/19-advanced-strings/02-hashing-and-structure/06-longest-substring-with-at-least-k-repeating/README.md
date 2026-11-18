---
name: sheet-longest-substring-with-at-least-k-repeating
title: 'Longest Substring With Each Letter at Least K Times'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Advanced
theory: divide-at-the-walls
---

## Statement

Return the length of the **longest substring** of `s` in which **every letter that appears occurs at least `k` times**. Return `0` if there is none.

For `s = "aaabb"` and `k = 3` the answer is `3` (`"aaa"`); for `s = "ababbc"` and `k = 2` it is `5` (`"ababb"`).

The starter code counts the letters of every substring. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_substring_k_repeating('aaabb', 3)
```

Output:

```text
3
```

**Example 2**

Input:

```python
longest_substring_k_repeating('ababbc', 2)
```

Output:

```text
5
```

### Constraints

- `0 <= len(s) <= 100000`
- `1 <= k <= 100000`
- Lower-case letters.

## Explanation

`solve(lo, hi)` works on `s[lo:hi]`. A letter with a count below `k` splits the range, and the best length of the pieces is returned.

### Complexity

- Time: O(26 * n). A letter that appears fewer than `k` times splits the string; each level of recursion removes at least one of the at most 26 letters, and each level scans `n` characters.
- Space: O(n). Recursion depth is at most 26, plus the counts.
