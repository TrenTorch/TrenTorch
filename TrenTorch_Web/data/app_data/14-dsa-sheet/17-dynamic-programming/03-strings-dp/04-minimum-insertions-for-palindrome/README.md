---
name: sheet-minimum-insertions-for-palindrome
title: 'Insertions to Make a Palindrome'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
theory: palindromes-inside-strings
---

## Statement

You may insert characters **anywhere** in `s`. Return the **fewest insertions** needed to make `s` a palindrome.

For `"mbadm"` the answer is `2` (`"mbdadbm"`); for `"leetcode"` it is `5`.

### Examples

**Example 1**

Input:

```python
min_insertions('mbadm')
```

Output:

```text
2
```

**Example 2**

Input:

```python
min_insertions('leetcode')
```

Output:

```text
5
```

### Constraints

- `0 <= len(s) <= 1000`
- Lower-case letters.

## Explanation

The helper is the longest palindromic subsequence table from the previous question. Characters outside it each cost one insertion.

### Complexity

- Time: O(n^2). The longest palindromic subsequence is found with a table whose cells are each computed once; the answer is `n` minus its length.
- Space: O(n). Two rows of the table.
