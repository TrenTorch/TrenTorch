---
name: sheet-longest-common-substring
title: 'Longest Common Substring'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
---

## Statement

A **substring** is a block of **consecutive** characters. Return the length of the **longest substring that appears in both `a` and `b`**.

For `a = "abcdxyz"` and `b = "xyzabcd"` the answer is `4` (`"abcd"`).

### Examples

**Example 1**

Input:

```python
longest_common_substring('abcdxyz', 'xyzabcd')
```

Output:

```text
4
```

**Example 2**

Input:

```python
longest_common_substring('zxabcdezy', 'yzabcdezx')
```

Output:

```text
6
```

### Constraints

- `0 <= len(a), len(b) <= 900`
- Lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Unlike the subsequence question, characters must be **consecutive**, so a mismatch resets the run. **State:** `run(i, j)`, the length of the longest common suffix of `a[:i]` and `b[:j]`. **Transition:** if `a[i - 1] == b[j - 1]` then `run(i, j) = 1 + run(i - 1, j - 1)`, otherwise `0`. The answer is the **maximum** over all cells (not the corner). `O(len(a) × len(b))`, one row at a time.

## Explanation

`cur[j]` is the length of the common block ending at `a[i - 1]` and `b[j - 1]`. A mismatch leaves it at 0, and `best` keeps the largest run.
