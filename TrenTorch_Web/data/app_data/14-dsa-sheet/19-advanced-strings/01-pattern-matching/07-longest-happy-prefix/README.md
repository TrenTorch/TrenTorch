---
name: sheet-longest-happy-prefix
title: 'Longest Happy Prefix'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
theory: the-longest-happy-prefix
---

## Statement

A **happy prefix** is a non-empty prefix of `s` (shorter than `s`) that is also a suffix. Return the **longest happy prefix**, or `""` if there is none.

For `"level"` the answer is `"l"`; for `"ababab"` it is `"abab"`.

The starter code compares every possible length from scratch. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_happy_prefix('level')
```

Output:

```text
'l'
```

**Example 2**

Input:

```python
longest_happy_prefix('ababab')
```

Output:

```text
'abab'
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Explanation

The loop is the standard prefix function; only the last value is used.

### Complexity

- Time: O(n). The last value of the prefix function is the length of the longest border.
- Space: O(n). The prefix function array.
