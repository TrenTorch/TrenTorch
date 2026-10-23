---
name: sheet-minimum-window-substring
title: 'Minimum Window Substring'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Mastery
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

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

This is the classic **shortest valid window**. Keep `need` (the counts required by `t`) and `have` (the counts inside the window), plus `missing`, the number of **different** characters of `t` whose count is not yet satisfied.

1. Expand `right`: add `s[right]`. If this makes some needed character's count reach exactly the required amount, `missing -= 1`.
2. While `missing == 0` the window is valid: **record it if it is shorter**, then shrink from the left (remove `s[left]`; if that drops a needed count below the requirement, `missing += 1`), advance `left`.

Each pointer moves forward only, so the time is `O(len(s) + len(t))`. Recording only when strictly shorter keeps the leftmost window on ties.

## Explanation

`missing` tracks how many needed characters are still short. The window is valid when it is 0. Shrinking is allowed while it stays valid, which finds the tightest window ending at each `right`.
