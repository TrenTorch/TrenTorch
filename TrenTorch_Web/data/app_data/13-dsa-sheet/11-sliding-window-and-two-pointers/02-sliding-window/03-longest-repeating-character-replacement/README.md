---
name: sheet-longest-repeating-character-replacement
title: 'Longest Repeating Character Replacement'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Advanced
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

**Explanation:** In 'AABABBA' the longest stretch of a single letter is 2, but replacing one differing letter gives a 4-character block of identical letters.

**Example 2**

Input:

```python
character_replacement('ABAB', 2)
```

Output:

```text
4
```

**Explanation:** In 'ABAB' we can change both letters in any 4-character window to the same letter, so the whole string becomes uniform, giving length 4.

### Constraints

- `0 <= len(s) <= 200000`
- `0 <= k <= 200000`
- `s` contains upper-case letters.

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

A window can be turned into one repeated letter with `window_length - (count of its most common letter)` changes. So the window is valid when `length - max_count <= k`.

Keep a count of letters in the window and the largest count seen so far, `max_count`. Expand `right`; if the window is **invalid** (`length - max_count > k`), move `left` by **one** (not a loop!) and decrement the count of the letter that leaves.

Two surprising details: `max_count` is never decreased when the window shrinks. It is fine, because the answer can only grow when a window gets a **new bigger** `max_count`; a stale larger value only keeps the window size from shrinking, which never produces a wrong (too big) answer. This makes it `O(n)` with `O(26)` memory.

## Explanation

The window never gets smaller: when it becomes invalid it slides (right moves, left moves one). The final window size is the answer.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                                                        |
| ---------------------------------- | ---------------------------------------------------------------- |
| `count = {}`                       | `count = {}`                                                     |
| `count[ch] = count.get(ch, 0) + 1` | `count = {'A': 1}, left = 0, max_count = 0, right = 0, ch = 'A'` |
| `count[ch] = count.get(ch, 0) + 1` | `count = {'A': 2}, max_count = 1, right = 1`                     |
| `for right, ch in enumerate(s):`   | `count = {'A': 2, 'B': 1}, max_count = 2, right = 3`             |
| `count[ch] = count.get(ch, 0) + 1` | `count = {'A': 3, 'B': 2}, max_count = 3, right = 4, ch = 'B'`   |
| `count[ch] = count.get(ch, 0) + 1` | `count = {'A': 2, 'B': 3}, left = 1, right = 5`                  |
| `for right, ch in enumerate(s):`   | `count = {'A': 1, 'B': 3}, left = 2, right = 6, ch = 'A'`        |
| `return`                           | `returned = 4`                                                   |

### Complexity

- Time: O(n) where n is the length of s.
- Extra space: O(1) constant extra space for letter counts.
- The brute force takes O(n^3), n is the length of s.
