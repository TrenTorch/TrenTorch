---
name: sheet-sort-by-frequency
title: 'Sort Characters by Frequency'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: sorting-the-characters-of-a-string
---

## Statement

Return a string with the characters of `s` **grouped together**, ordered by how often they appear: the most frequent character first, each character repeated as many times as it occurs. If two characters appear equally often, the **smaller character** (in alphabetical order) comes first.

### Examples

**Example 1**

Input:

```python
sort_by_frequency('tree')
```

Output:

```text
'eert'
```

`e` appears twice, `r` and `t` once: `eert`.

**Example 2**

Input:

```python
sort_by_frequency('cccaaa')
```

Output:

```text
'aaaccc'
```

`a` and `c` tie, so `a` comes first.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains letters and digits.

## Explanation

`counts` holds each character's frequency. The distinct characters are sorted by `(-count, char)`. Each group is `char * count`, and the groups are joined.

### Complexity

- Time: O(n + k log k). One counting pass, then a sort of the `k <= 62` distinct characters, then building the result.
- Space: O(n). The result string; the counter has at most 62 entries.
