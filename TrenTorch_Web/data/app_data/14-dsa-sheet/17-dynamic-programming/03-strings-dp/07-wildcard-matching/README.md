---
name: sheet-wildcard-matching
title: 'Wildcard Matching'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
theory: wildcard-and-regular-expression-matching
---

## Statement

The pattern `p` may contain `?` (matches **any single character**) and `*` (matches **any sequence of characters**, including an empty one). Return `True` if `p` matches the **whole** string `s`.

For `s = "aa"` and `p = "*"` the answer is `True`; for `s = "cb"` and `p = "?a"` it is `False`.

The starter code tries every length for every star. It is correct but too slow with many stars.

### Examples

**Example 1**

Input:

```python
is_match_wildcard('aa', '*')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_match_wildcard('cb', '?a')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s), len(p) <= 1000`
- `s` has lower-case letters; `p` has lower-case letters, `?` and `*`.

## Explanation

`prev` is the row for `i - 1` and `cur` for `i`. The star case combines "empty match" (`cur[j - 1]`) and "one more character" (`prev[j]`).

### Complexity

- Time: O(n * m). Every cell of the table is computed once, in O(1).
- Space: O(m). Two rows of the table (`n` = len(s), `m` = len(p)).
