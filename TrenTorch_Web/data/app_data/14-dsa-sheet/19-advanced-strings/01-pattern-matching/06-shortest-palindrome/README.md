---
name: sheet-shortest-palindrome
title: 'Shortest Palindrome'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Advanced
theory: the-shortest-palindrome
---

## Statement

You may add letters **only in front of `s`**. Return the **shortest palindrome** you can get this way.

For `"aacecaaa"` the answer is `"aaacecaaa"`; for `"abcd"` it is `"dcbabcd"`.

The starter code tests every prefix for being a palindrome letter by letter. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
shortest_palindrome('aacecaaa')
```

Output:

```text
'aaacecaaa'
```

**Example 2**

Input:

```python
shortest_palindrome('abcd')
```

Output:

```text
'dcbabcd'
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Explanation

`border` is the length of the longest palindromic prefix. The part of `s` after it is reversed and placed in front.

### Complexity

- Time: O(n). The prefix function of `s + "#" + reverse(s)` gives the longest palindromic prefix of `s` in one linear pass.
- Space: O(n). The combined string and its prefix function.
