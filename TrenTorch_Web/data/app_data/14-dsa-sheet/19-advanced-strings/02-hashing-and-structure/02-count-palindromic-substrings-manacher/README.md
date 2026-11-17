---
name: sheet-count-palindromic-substrings-manacher
title: 'Count Palindromic Substrings, Fast'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Mastery
theory: counting-palindromic-substrings-fast
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

## Explanation

`d1[i]` counts the odd palindromes with centre `i` (the radius including the centre itself); `d2[i]` counts the even ones. Each loop keeps the window `[left, right]` of the rightmost palindrome.

### Complexity

- Time: O(n). Manacher's algorithm: the rightmost palindrome only grows, and every centre reuses its mirror's radius inside it.
- Space: O(n). The two radius arrays.
