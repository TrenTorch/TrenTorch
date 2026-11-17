---
name: sheet-palindrome-partitions
title: 'Palindrome Partitioning'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
theory: cutting-into-palindromes
---

## Statement

Return every way to **cut `s` into pieces so that every piece is a palindrome** (reads the same both ways). Each way is a list of the pieces from left to right. List the ways sorted as lists of strings (compare the first piece, then the second, and so on).

For `"aab"`: `["a", "a", "b"]` and `["aa", "b"]`.

### Examples

**Example 1**

Input:

```python
palindrome_partitions('aab')
```

Output:

```text
[['a', 'a', 'b'], ['aa', 'b']]
```

**Example 2**

Input:

```python
palindrome_partitions('a')
```

Output:

```text
[['a']]
```

### Constraints

- `0 <= len(s) <= 14`
- `s` contains lower-case letters.

## Explanation

First mark every palindromic piece: `pal[i][j]` is true when `s[i:j + 1]` is a palindrome. A piece is a palindrome when its ends match and the inside `pal[i + 1][j - 1]` is one (or the inside is empty); fill the table from short pieces to long ones.

Then backtrack: from `start`, try each end `j` whose piece `s[start:j + 1]` is marked, add it, recurse from `j + 1`, and undo. Taking shorter pieces first produces the partitions in sorted order, so no sorting is needed.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                   | Variables                                                                               |
| --------------------------------- | --------------------------------------------------------------------------------------- |
| `n = len(s)`                      | `n = 3`                                                                                 |
| `for i in range(n - length + 1):` | `pal = [[False, False, False], [False, False, False], [False, Fa..., length = 1, i = 0` |
| `for i in range(n - length + 1):` | `pal = [[True, False, False], [False, False, False], [False, Fal..., i = 1, j = 0`      |
| `for i in range(n - length + 1):` | `pal = [[True, False, False], [False, True, False], [False, Fals..., i = 2, j = 1`      |
| `j = i + length - 1`              | `length = 2, i = 0`                                                                     |
| `j = i + length - 1`              | `pal = [[True, True, False], [False, True, False], [False, False..., i = 1, j = 2`      |
| `out = []`                        | `length = 3, i = 0, out = []`                                                           |
| `return`                          | `returned = [['a', 'a', 'b'], ['aa', 'b']]`                                             |

### Complexity

- Time: O(n * 2^n). A table of palindromic pieces is built once in `O(n^2)`; the recursion then visits at most `2^(n-1)` partitions and the lists come out already in sorted order.
- Space: O(n^2 + n * 2^n). The table, plus the output.
