---
name: sheet-find-the-needle
title: 'Find the Needle'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
theory: find-the-first-occurrence
---

## Statement

Return the **index of the first occurrence** of `needle` in `haystack`, or `-1` if it does not occur. An empty `needle` occurs at index `0`.

For `haystack = "sadbutsad"` and `needle = "sad"` the answer is `0`; for `needle = "leeto"` in `"leetcode"` it is `-1`.

The starter code compares letter by letter at every start. It is correct but too slow on repetitive texts.

### Examples

**Example 1**

Input:

```python
find_needle('sadbutsad', 'sad')
```

Output:

```text
0
```

**Example 2**

Input:

```python
find_needle('leetcode', 'leeto')
```

Output:

```text
-1
```

### Constraints

- `0 <= len(haystack) <= 200000`
- `0 <= len(needle) <= 2000`
- Lower-case letters.

## Explanation

`fail` is the prefix function of the needle. `k` is the length of the current match; the fall back reuses the part of the needle that is still valid.

### Complexity

- Time: O(n + m). KMP: the failure table of the needle takes O(m) and the scan of the haystack never moves back, so it takes O(n).
- Space: O(m). The failure table (`n` = len(haystack), `m` = len(needle)).
