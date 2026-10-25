---
name: sheet-longest-substring-with-k-distinct
title: 'Longest Substring With K Distinct Characters'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

Return the length of the **longest substring** of `s` that has **at most `k` different characters**.

For `s = "eceba"` and `k = 2` the answer is `3` (`"ece"`).

The starter code tries every start. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_k_distinct('eceba', 2)
```

Output:

```text
3
```

**Explanation:** The substring "ece" has length 3 and contains 'e', 'c' (2 distinct characters), which is at most k = 2. This is the longest such substring in "eceba".

**Example 2**

Input:

```python
longest_k_distinct('aa', 1)
```

Output:

```text
2
```

**Explanation:** The substring "aa" has length 2 and contains 'a' (1 distinct character), which is at most k = 1. This is the longest such substring in "aa".

### Constraints

- `0 <= len(s) <= 200000`
- `0 <= k <= 26`
- `s` contains lower-case letters.

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

This window has a **condition**: at most `k` different characters. Keep a dictionary `count` of the characters inside the window. Move `right` forward one character at a time (add it to `count`). If the window now has more than `k` different characters (`len(count) > k`), **shrink from the left** until it is valid again: decrease the count of `s[left]`, delete the key when it reaches 0, and advance `left`.

After every step the window is valid; its length is a candidate answer. Every character enters and leaves once: `O(n)`.

This "expand right, shrink left while invalid" loop is the standard form for the **longest valid window** questions.

## Explanation

`count` maps each character in the window to how many times it appears. A key whose count drops to zero is deleted so `len(count)` stays the number of different characters.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                                                         |
| ---------------------------------- | ----------------------------------------------------------------- |
| `count = {}`                       | `count = {}`                                                      |
| `for right, ch in enumerate(s):`   | `left = 0, best = 0, right = 0, ch = 'e'`                         |
| `count[ch] = count.get(ch, 0) + 1` | `count = {'e': 1, 'c': 1}, best = 1, right = 1, ch = 'c'`         |
| `count[ch] = count.get(ch, 0) + 1` | `count = {'e': 2, 'c': 1}, best = 2, right = 2, ch = 'e'`         |
| `count[s[left]] -= 1`              | `count = {'e': 1, 'c': 1, 'b': 1}, best = 3, right = 3, ch = 'b'` |
| `del count[s[left]]`               | `count = {'e': 1, 'b': 1}, left = 1`                              |
| `count[s[left]] -= 1`              | `count = {'e': 0, 'b': 1, 'a': 1}, left = 2, right = 4, ch = 'a'` |
| `return`                           | `returned = 3`                                                    |

### Complexity

- Time: O(n), where n is the length of s.
- Extra space: O(k), where k is the maximum distinct characters allowed.
- The brute force takes O(n^3), where n is the length of s.
