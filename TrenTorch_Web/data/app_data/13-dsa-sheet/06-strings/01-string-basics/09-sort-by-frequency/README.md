---
name: sheet-sort-by-frequency
title: 'Sort Characters by Frequency'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

## Theory

Count the characters with a `Counter`, then sort the **distinct** characters by a key that puts bigger counts first and breaks ties alphabetically: `key=lambda ch: (-count[ch], ch)`.

Finally repeat each character by its count: `ch * count[ch]` builds the whole group in one operation, and `"".join(...)` joins the groups. There are at most about 62 different characters here, so the sort is tiny and counting dominates: `O(n)`.

## Explanation

`counts` holds each character's frequency. The distinct characters are sorted by `(-count, char)`. Each group is `char * count`, and the groups are joined.
