---
name: sheet-longest-palindromic-subsequence
title: 'Longest Palindromic Subsequence'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
theory: palindromes-inside-strings
---

## Statement

Return the length of the **longest palindromic subsequence** of `s` (a subsequence that reads the same forwards and backwards; characters may be skipped).

For `"bbbab"` the answer is `4` (`"bbbb"`).

The starter code is a plain recursion. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_palindrome_subseq('bbbab')
```

Output:

```text
4
```

**Example 2**

Input:

```python
longest_palindrome_subseq('cbbd')
```

Output:

```text
2
```

### Constraints

- `0 <= len(s) <= 1000`
- Lower-case letters.

## Explanation

`row` holds `best(i + 1, ·)` and `new` the row for `i`, filled from left to right for `j > i`.

### Complexity

- Time: O(n^2). Every cell of the table is computed once, in O(1).
- Space: O(n). Two rows of the table.
