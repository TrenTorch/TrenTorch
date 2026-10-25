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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                                                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `need = {}`                      | `need = {}`                                                                                                                |
| `for right, ch in enumerate(s):` | `need = {'A': 1, 'B': 1, 'C': 1}, ch = 'A', have = {}, missing = 3, best_start = 0, best_len = 14, left = 0, right = 0`    |
| `have[ch] = have.get(ch, 0) + 1` | `ch = 'E', have = {'A': 1, 'D': 1, 'O': 1, 'B': 1, 'E': 1}, missing = 1, right = 4`                                        |
| `for right, ch in enumerate(s):` | `ch = 'D', have = {'A': 0, 'D': 1, 'O': 2, 'B': 1, 'E': 1, 'C': 1}, best_len = 6, left = 1, right = 7, gone = 'A'`         |
| `gone = s[left]`                 | `ch = 'A', have = {'A': 1, 'D': 1, 'O': 2, 'B': 2, 'E': 2, 'C': 1}, missing = 0, left = 2, right = 10, gone = 'O'`         |
| `missing += 1`                   | `have = {'A': 1, 'D': 1, 'O': 1, 'B': 1, 'E': 1, 'C': 0}, missing = 1, left = 5, gone = 'C'`                               |
| `have[gone] -= 1`                | `ch = 'C', have = {'A': 1, 'D': 0, 'O': 0, 'B': 1, 'E': 1, 'C': 1, 'N': 1}, missing = 0, left = 7, right = 12, gone = 'D'` |
| `return`                         | `returned = 'BANC'`                                                                                                        |
