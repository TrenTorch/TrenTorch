---
name: sheet-is-anagram
title: 'Anagram Check'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: counting-with-counter
---

## Statement

Two strings are **anagrams** if one can be rearranged into the other: they contain the same characters the same number of times. Return `True` if `a` and `b` are anagrams, otherwise `False`.

### Examples

**Example 1**

Input:

```python
is_anagram('listen', 'silent')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_anagram('rat', 'car')
```

Output:

```text
False
```

### Constraints

- `0 <= len(a), len(b) <= 2 * 10**5`
- Both strings contain only lower-case letters.

## Explanation

Strings with different lengths cannot be anagrams, and `Counter` equality already covers that (the counts differ). No extra length check is needed, though adding one skips the work early.

### Complexity

- Time: O(n + m). Each string is counted once, and the lengths are compared first.
- Space: O(k). Two counters with at most `k = 26` letters.
