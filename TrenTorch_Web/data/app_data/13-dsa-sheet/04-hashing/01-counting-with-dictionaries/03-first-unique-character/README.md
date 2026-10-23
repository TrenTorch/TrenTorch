---
name: sheet-first-unique-character
title: 'First Unique Character'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Beginner
---

## Statement

Return the **index** of the first character in `s` that appears **exactly once** in the whole string, or `-1` if every character repeats (or the string is empty).

### Examples

**Example 1**

Input:

```python
first_unique_character('leetcode')
```

Output:

```text
0
```

`l` at index 0 appears once.

**Example 2**

Input:

```python
first_unique_character('aabb')
```

Output:

```text
-1
```

Every character repeats.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains lower-case letters.

## Theory

Two passes with a counting table. In the first pass count every character. In the second pass walk the string in order and return the index of the first character whose count is `1`.

Why not one pass? You only know a character is unique once you have seen the _whole_ string. Counting first, then scanning in the original order, gives the "first" for free.

Strings are iterable, so `Counter(s)` counts characters directly, and `enumerate(s)` gives the index while scanning.

## Explanation

`counts = Counter(s)` records how often each character occurs. The loop over `enumerate(s)` returns the first index whose character has `counts[ch] == 1`. If the loop ends, no character is unique and the answer is `-1`.
