---
name: sheet-find-all-anagrams
title: 'Find All Anagrams in a String'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: windows-of-letter-counts
---

## Statement

Return the **start indices** (in increasing order) of every substring of `s` that is a rearrangement (anagram) of `p`. For `s = "cbaebabacd"` and `p = "abc"` the answer is `[0, 6]`.

### Examples

**Example 1**

Input:

```python
find_anagrams('cbaebabacd', 'abc')
```

Output:

```text
[0, 6]
```

**Example 2**

Input:

```python
find_anagrams('abab', 'ab')
```

Output:

```text
[0, 1, 2]
```

### Constraints

- `0 <= len(p) <= 100000`
- `0 <= len(s) <= 200000`
- Lower-case letters; an empty `p` has no matches.

## Explanation

After processing index `i`, the window is `s[i - m + 1 .. i]`. If its counts equal `p`'s counts, `i - m + 1` is recorded.

### Complexity

- Time: O(n). The window moves one step at a time and comparing two 26-letter counts is O(26).
- Space: O(1). Two arrays of 26 counts (the result list is output).
