---
name: sheet-ransom-note
title: 'Ransom Note'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Beginner
theory: counting-up-and-counting-down
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

## Explanation

`Counter(note) - Counter(magazine)` drops every letter whose magazine count covers the note's count, and keeps the shortfall of the others. Empty means everything is covered.

### Complexity

- Time: O(n + m). Each string is counted once and the two counters (at most 26 letters) are subtracted.
- Space: O(1). Two counters with at most 26 letters.
