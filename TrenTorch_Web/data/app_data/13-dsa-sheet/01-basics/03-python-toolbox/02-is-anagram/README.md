---
name: sheet-is-anagram
title: 'Anagram Check'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
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

- `0 <= len(a), len(b) <= 10**6`
- Both strings contain only lower-case letters.

## Theory

`collections.Counter` turns an iterable into a dictionary of `value -> how many times it appears`. Two `Counter` objects compare equal when every count matches, so `Counter(a) == Counter(b)` is the whole check, in `O(n)`.

Sorting both strings and comparing also works (`O(n log n)`). The counting version is faster for long strings, and the habit of counting with a `Counter` returns in nearly every hashing problem.

## Explanation

Strings with different lengths cannot be anagrams, and `Counter` equality already covers that (the counts differ). No extra length check is needed, though adding one skips the work early.
