---
name: sheet-find-all-anagrams
title: 'Find All Anagrams in a String'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

Return the **start indices** (in increasing order) of every substring of `s` that is a rearrangement (anagram) of `p`. For `s = "cbaebabacd"` and `p = "abc"` the answer is `[0, 6]`.

### Examples

**Example 1**

Input:

```python
find_anagrams('cbaebabacd', 'abc')
```

Output:

```text
[0, 6]
```

**Example 2**

Input:

```python
find_anagrams('abab', 'ab')
```

Output:

```text
[0, 1, 2]
```

### Constraints

- `0 <= len(p) <= 100000`
- `0 <= len(s) <= 200000`
- Lower-case letters; an empty `p` has no matches.

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

This is the same fixed window as the permutation question, but you collect **all** the positions instead of stopping at the first. Slide a window of size `len(p)`, keep its letter counts, and every time the counts equal those of `p`, the start index `i - len(p) + 1` is an answer.

To avoid comparing 26 counts every step, you can keep a running number `matched` of letters whose counts are equal and update it as counts change. The simple comparison is already fast enough here.

## Explanation

After processing index `i`, the window is `s[i - m + 1 .. i]`. If its counts equal `p`'s counts, `i - m + 1` is recorded.
