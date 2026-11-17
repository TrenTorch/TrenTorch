---
name: sheet-repeated-substring-pattern
title: 'Repeated Substring Pattern'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
theory: repeated-substring-pattern
---

## Statement

Return `True` if `s` can be written as a **block repeated two or more times** (`"abab"` is `"ab"` twice; `"aaa"` is `"a"` three times; `"abcab"` is not).

A string with fewer than 2 letters gives `False`.

### Examples

**Example 1**

Input:

```python
repeated_substring_pattern('abab')
```

Output:

```text
True
```

**Example 2**

Input:

```python
repeated_substring_pattern('abcab')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Explanation

`period = n - pi[-1]` is the smallest candidate block length; it works if it divides the length and the border is non-zero.

### Complexity

- Time: O(n). The prefix function is computed once; the string is a repetition exactly when its length is a multiple of the smallest period `n - pi[n-1]` and the string has a border.
- Space: O(n). The prefix function array.
