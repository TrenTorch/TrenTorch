---
name: sheet-longest-repeating-character-replacement
title: 'Longest Repeating Character Replacement'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Advanced
theory: replacing-letters
---

## Statement

You may change **at most `k` characters** of `s` to any letters. Return the length of the **longest substring** that can be made of one repeated letter.

For `s = "AABABBA"` and `k = 1` the answer is `4` (change one `A` or `B` to get `"AAAA"` or `"BBBB"` within a window).

The starter code counts the letters of every substring from scratch. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
character_replacement('AABABBA', 1)
```

Output:

```text
4
```

**Example 2**

Input:

```python
character_replacement('ABAB', 2)
```

Output:

```text
4
```

### Constraints

- `0 <= len(s) <= 200000`
- `0 <= k <= 200000`
- `s` contains upper-case letters.

## Explanation

The window never gets smaller: when it becomes invalid it slides (right moves, left moves one). The final window size is the answer.

### Complexity

- Time: O(n). One pass; the window never shrinks, it only slides.
- Space: O(26). The counts of at most 26 letters.
