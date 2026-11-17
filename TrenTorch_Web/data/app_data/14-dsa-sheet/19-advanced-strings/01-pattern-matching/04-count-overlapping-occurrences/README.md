---
name: sheet-count-overlapping-occurrences
title: 'Count Overlapping Occurrences'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
theory: counting-overlapping-occurrences
---

## Statement

Count the **occurrences of `pattern` in `text`**, counting overlapping ones (`"aa"` occurs 3 times in `"aaaa"`). `pattern` is not empty.

For `text = "aaaa"` and `pattern = "aa"` the answer is `3`.

The starter code compares letter by letter at every start. It is correct but too slow on repetitive texts.

### Examples

**Example 1**

Input:

```python
count_overlapping('aaaa', 'aa')
```

Output:

```text
3
```

**Example 2**

Input:

```python
count_overlapping('abababa', 'aba')
```

Output:

```text
3
```

### Constraints

- `0 <= len(text) <= 200000`
- `1 <= len(pattern) <= 2000`
- Lower-case letters.

## Explanation

After a full match the fall back `k = fail[k - 1]` keeps the longest border, which is where an overlapping match would start.

### Complexity

- Time: O(n + m). KMP: after a match the pointer falls back to the longest border instead of restarting, so overlaps are counted without rescanning.
- Space: O(m). The failure table of the pattern.
