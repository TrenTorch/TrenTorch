---
name: sheet-ransom-note
title: 'Ransom Note'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Beginner
---

## Statement

Return `True` if you can build the string `note` using letters cut from `magazine`, where each letter of the magazine can be used **at most once**. Otherwise return `False`.

### Examples

**Example 1**

Input:

```python
ransom_note('aab', 'baa')
```

Output:

```text
True
```

**Example 2**

Input:

```python
ransom_note('aa', 'ab')
```

Output:

```text
False
```

### Constraints

- `0 <= len(note), len(magazine) <= 3 * 10**5`
- Both strings contain lower-case letters.

## Theory

The note can be built exactly when, for **every letter**, the magazine has at least as many copies as the note needs. So compare counts.

`Counter` supports subtraction: `Counter(note) - Counter(magazine)` keeps only the letters the note needs **more** of than the magazine has. If that result is empty, nothing is missing. An empty `Counter` is falsy, so `not (need - have)` is the whole test.

Counting both strings is `O(len(note) + len(magazine))`.

## Explanation

`Counter(note) - Counter(magazine)` drops every letter whose magazine count covers the note's count, and keeps the shortfall of the others. Empty means everything is covered.
