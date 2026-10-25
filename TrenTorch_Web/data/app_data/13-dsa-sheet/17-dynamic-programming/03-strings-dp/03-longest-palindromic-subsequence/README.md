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

**Explanation:** The subsequence bbbb is a palindrome of length 4 found within the input string bbbab.

**Example 2**

Input:

```python
longest_palindrome_subseq('cbbd')
```

Output:

```text
2
```

**Explanation:** The subsequence bb is a palindrome of length 2 found within the input string cbbd.

### Constraints

- `0 <= len(s) <= 1000`
- Lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `best(i, j)`, the longest palindromic subsequence inside `s[i..j]`. **Transition:** if the two ends are equal, they can wrap a palindrome: `best(i, j) = 2 + best(i + 1, j - 1)`. Otherwise drop one end: `best(i, j) = max(best(i + 1, j), best(i, j - 1))`. **Base cases:** one character is a palindrome of length 1; an empty range is 0.

A neat shortcut: the answer equals the **longest common subsequence of `s` and its reverse**. The interval table fills by increasing length (or `i` from the end). `O(n²)`.

## Explanation

`row` holds `best(i + 1, ·)` and `new` the row for `i`, filled from left to right for `j > i`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                                                     |
| -------------------------------- | ------------------------------------------------------------- |
| `n = len(s)`                     | `n = 5`                                                       |
| `for i in range(n - 1, -1, -1):` | `prev = [0, 0, 0, 0, 1], i = 3, cur = [0, 0, 0, 0, 1]`        |
| `for i in range(n - 1, -1, -1):` | `prev = [0, 0, 0, 1, 1], i = 2, cur = [0, 0, 0, 1, 1], j = 4` |
| `cur[j] = 2 + prev[j - 1]`       | `cur = [0, 0, 1, 1, 3]`                                       |
| `cur[j] = 2 + prev[j - 1]`       | `prev = [0, 0, 1, 1, 3], i = 1, cur = [0, 1, 2, 0, 0], j = 2` |
| `for i in range(n - 1, -1, -1):` | `prev = [0, 1, 2, 2, 3], i = 0, cur = [0, 1, 2, 2, 3], j = 4` |
| `cur[j] = 2 + prev[j - 1]`       | `cur = [1, 2, 3, 0, 0], j = 2`                                |
| `return`                         | `returned = 4`                                                |

### Complexity

- Time: O(n^2), where n is the length of string s.
- Extra space: O(n), where n is the length of string s.
- The brute force takes O(2^n * n) n is string length.
