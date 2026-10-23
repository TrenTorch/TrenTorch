---
name: sheet-longest-common-subsequence
title: 'Longest Common Subsequence'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
---

## Statement

A **subsequence** keeps the order of the characters but may skip some. Return the **length of the longest string that is a subsequence of both `a` and `b`**.

For `a = "abcde"` and `b = "ace"` the answer is `3` (`"ace"`).

The starter code is a plain recursion. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
lcs_length('abcde', 'ace')
```

Output:

```text
3
```

**Example 2**

Input:

```python
lcs_length('abc', 'def')
```

Output:

```text
0
```

### Constraints

- `0 <= len(a), len(b) <= 900`
- Lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `lcs(i, j)`, the answer for the first `i` characters of `a` and the first `j` of `b`. **Transition:** if the last characters match (`a[i - 1] == b[j - 1]`) they can both end the common subsequence: `lcs(i, j) = 1 + lcs(i - 1, j - 1)`. Otherwise one of them is not used: `lcs(i, j) = max(lcs(i - 1, j), lcs(i, j - 1))`. **Base cases:** `lcs(0, j) = lcs(i, 0) = 0`.

The table has `(len(a) + 1) × (len(b) + 1)` cells; each is filled in `O(1)`. Only the previous row is needed. This **two-string table** is the pattern behind edit distance, interleaving and many other questions.

## Explanation

`prev` is the previous row (`lcs(i - 1, ·)`), `cur` the one being built. A match takes the diagonal value plus one; otherwise the larger of the cell above and the cell to the left.
