---
name: sheet-minimum-window-substring
title: 'Minimum Window Substring'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Mastery
theory: tracking-what-is-still-missing
---

## Statement

Return the **smallest substring** of `s` that contains **every character of `t`** (with multiplicity: `t = "aab"` needs two `a`s and one `b`). If there are several of the same smallest length, return the **leftmost**. If there is none, return `""`.

For `s = "ADOBECODEBANC"` and `t = "ABC"` the answer is `"BANC"`.

The starter code checks windows from every start. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
min_window('ADOBECODEBANC', 'ABC')
```

Output:

```text
'BANC'
```

**Example 2**

Input:

```python
min_window('a', 'aa')
```

Output:

```text
''
```

### Constraints

- `0 <= len(s) <= 200000`
- `0 <= len(t) <= 100000`
- Letters (upper or lower case); an empty `t` gives `""`.

## Explanation

`missing` tracks how many needed characters are still short. The window is valid when it is 0. Shrinking is allowed while it stays valid, which finds the tightest window ending at each `right`.

### Complexity

- Time: O(n + m). Both window ends only move forward; `m` is the length of `t`.
- Space: O(k). The two count maps, `k` = number of distinct characters.
