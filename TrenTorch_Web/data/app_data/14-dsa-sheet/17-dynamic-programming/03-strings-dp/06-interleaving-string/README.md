---
name: sheet-interleaving-string
title: 'Interleaving String'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
theory: counting-subsequences
---

## Statement

`c` is an **interleaving** of `a` and `b` if its characters can be split into two subsequences, one spelling `a` and the other spelling `b`, using every character of `c` exactly once. Return `True` if `c` is an interleaving of `a` and `b`.

For `a = "aabcc"`, `b = "dbbca"` and `c = "aadbbcbcac"` the answer is `True`.

### Examples

**Example 1**

Input:

```python
is_interleave('aabcc', 'dbbca', 'aadbbcbcac')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_interleave('aabcc', 'dbbca', 'aadbbbaccc')
```

Output:

```text
False
```

### Constraints

- `0 <= len(a), len(b) <= 500`
- `0 <= len(c) <= 1000`
- Lower-case letters.

## Explanation

`row[j]` means `ok(i, j)` for the current `i`. The first column and the first row are filled with simple checks.

### Complexity

- Time: O(n * m). Every cell of the table is computed once, in O(1).
- Space: O(m). One row of the table.
