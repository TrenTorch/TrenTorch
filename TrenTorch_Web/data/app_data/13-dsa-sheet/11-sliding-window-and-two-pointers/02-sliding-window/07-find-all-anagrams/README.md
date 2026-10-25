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

**Explanation:** The window of three characters slides through s, comparing counts; at positions 0 ('cba') and 6 ('bac') the counts equal p's counts, producing indices 0 and 6.

**Example 2**

Input:

```python
find_anagrams('abab', 'ab')
```

Output:

```text
[0, 1, 2]
```

**Explanation:** For s='abab' and p='ab', each two-character window matches p, so starting indices 0,1,2 are returned.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                   | Variables                                                                                                                                                               |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `m = len(p)`                      | `m = 3`                                                                                                                                                                 |
| `need[ord(ch) - 97] += 1`         | `need = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., window = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., ch = 'b'`                  |
| `window[ord(ch) - 97] += 1`       | `need = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., window = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., ch = 'c', out = [], i = 0` |
| `for i, ch in enumerate(s):`      | `window = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., ch = 'e', out = [0], i = 3`                                                                     |
| `window[ord(s[i - m]) - 97] -= 1` | `window = [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., ch = 'b', i = 4`                                                                                |
| `window[ord(s[i - m]) - 97] -= 1` | `window = [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., i = 6`                                                                                          |
| `window[ord(ch) - 97] += 1`       | `window = [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,..., ch = 'c', i = 8`                                                                                |
| `return`                          | `returned = [0, 6]`                                                                                                                                                     |
