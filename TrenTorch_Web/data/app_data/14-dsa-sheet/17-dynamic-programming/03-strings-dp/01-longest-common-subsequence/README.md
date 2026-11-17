---
name: sheet-longest-common-subsequence
title: 'Longest Common Subsequence'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
theory: longest-common-subsequence
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

## Explanation

`prev` is the previous row (`lcs(i - 1, ·)`), `cur` the one being built. A match takes the diagonal value plus one; otherwise the larger of the cell above and the cell to the left. The strings are swapped if needed so that the one laid along a row is the shorter, which keeps the rows short (the answer is the same either way).

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                                               |
| ----------------------------------- | ------------------------------------------------------- |
| `prev = [0] * (len(b) + 1)`         | `prev = [0, 0, 0, 0]`                                   |
| `cur[j] = max(prev[j], cur[j - 1])` | `i = 1, cur = [0, 1, 1, 0], j = 2`                      |
| `cur[j] = max(prev[j], cur[j - 1])` | `prev = [0, 1, 1, 1], i = 2, cur = [0, 1, 0, 0], j = 1` |
| `cur = [0] * (len(b) + 1)`          | `i = 3, cur = [0, 0, 0, 0], j = 3`                      |
| `cur[j] = max(prev[j], cur[j - 1])` | `cur = [0, 1, 2, 2]`                                    |
| `for j in range(1, len(b) + 1):`    | `prev = [0, 1, 2, 2], i = 4, cur = [0, 1, 0, 0], j = 2` |
| `cur[j] = max(prev[j], cur[j - 1])` | `i = 5, j = 1`                                          |
| `return`                            | `returned = 3`                                          |

### Complexity

- Time: O(n * m). Every cell of the `n x m` table is computed once; subquadratic algorithms are not known for the general case.
- Space: O(min(n, m)). Two rows of the table, laid along the shorter string.
