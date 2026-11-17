---
name: sheet-regular-expression-matching
title: 'Regular Expression Matching'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Mastery
theory: wildcard-and-regular-expression-matching
---

## Statement

The pattern `p` may contain `.` (matches **any single character**) and `*` (matches **zero or more copies of the character just before it**). Return `True` if `p` matches the **whole** string `s`. A `*` always follows a letter or `.`.

For `s = "aab"` and `p = "c*a*b"` the answer is `True`; for `s = "mississippi"` and `p = "mis*is*p*."` it is `False`.

### Examples

**Example 1**

Input:

```python
is_match_regex('aab', 'c*a*b')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_match_regex('mississippi', 'mis*is*p*.')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 1000`
- `0 <= len(p) <= 1000`
- `s` has lower-case letters; `p` has lower-case letters, `.` and `*`, and every `*` has a letter or `.` before it.

## Explanation

`fits(x, ch)` is `x == "." or x == ch`. In the star case, `cur[j - 2]` is "zero copies" and `prev[j]` is "one more copy".

### Complexity

- Time: O(n * m). Every cell of the table is computed once, in O(1).
- Space: O(m). Two rows of the table (`n` = len(s), `m` = len(p)).
