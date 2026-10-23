---
name: sheet-longest-palindromic-subsequence
title: 'Longest Palindromic Subsequence'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
---

## Statement

Return the length of the **longest palindromic subsequence** of `s` (a subsequence that reads the same forwards and backwards; characters may be skipped).

For `"bbbab"` the answer is `4` (`"bbbb"`).

The starter code is a plain recursion. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_palindrome_subseq('bbbab')
```

Output:

```text
4
```

**Example 2**

Input:

```python
longest_palindrome_subseq('cbbd')
```

Output:

```text
2
```

### Constraints

- `0 <= len(s) <= 1000`
- Lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `best(i, j)`, the longest palindromic subsequence inside `s[i..j]`. **Transition:** if the two ends are equal, they can wrap a palindrome: `best(i, j) = 2 + best(i + 1, j - 1)`. Otherwise drop one end: `best(i, j) = max(best(i + 1, j), best(i, j - 1))`. **Base cases:** one character is a palindrome of length 1; an empty range is 0.

A neat shortcut: the answer equals the **longest common subsequence of `s` and its reverse**. The interval table fills by increasing length (or `i` from the end). `O(n²)`.

## Explanation

`row` holds `best(i + 1, ·)` and `new` the row for `i`, filled from left to right for `j > i`.
