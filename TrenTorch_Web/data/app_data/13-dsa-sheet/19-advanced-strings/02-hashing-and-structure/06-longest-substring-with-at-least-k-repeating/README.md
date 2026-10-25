---
name: sheet-longest-substring-with-at-least-k-repeating
title: 'Longest Substring With Each Letter at Least K Times'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Advanced
---

## Statement

Return the length of the **longest substring** of `s` in which **every letter that appears occurs at least `k` times**. Return `0` if there is none.

For `s = "aaabb"` and `k = 3` the answer is `3` (`"aaa"`); for `s = "ababbc"` and `k = 2` it is `5` (`"ababb"`).

The starter code counts the letters of every substring. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_substring_k_repeating('aaabb', 3)
```

Output:

```text
3
```

**Explanation:** The substring "aaa" contains three a's, satisfying k=3, and no longer substring meets the requirement.

**Example 2**

Input:

```python
longest_substring_k_repeating('ababbc', 2)
```

Output:

```text
5
```

**Explanation:** Removing the trailing c leaves "ababb" where a and b each appear at least twice, giving length 5.

### Constraints

- `0 <= len(s) <= 100000`
- `1 <= k <= 100000`
- Lower-case letters.

## Theory

Any letter that occurs fewer than `k` times in the **whole** string can never be part of a valid substring, so it acts like a **separator**: the answer lies entirely in one of the pieces between such letters. Count the letters; if all letters already occur at least `k` times, the whole string is valid; otherwise split at the rare letters and solve each piece the same way, taking the maximum. That is a **divide and conquer**: at most 26 levels of splitting (each level removes a different letter), so `O(26 × n)`.

An alternative is a sliding window run once for each possible number of distinct letters (1 to 26).

## Explanation

`solve(lo, hi)` works on `s[lo:hi]`. A letter with a count below `k` splits the range, and the best length of the pieces is returned.

### Complexity

- Time: O(n^2), where n is the length of the string. The algorithm uses two nested loops: one to iterate over the start index of the substring (i), and another to iterate over the end index (j), resulting in approximately n^2 substring checks.
- Extra space: O(n) for the recursion stack in the worst case.
- The brute force takes O(n^3) where n is string length, due to O(n^2) substrings each tested in O(n) for the condition.
