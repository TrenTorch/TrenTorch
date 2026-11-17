---
name: sheet-compress-runs
title: 'Compress Repeated Characters'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: compressing-runs
---

## Statement

Compress `s` by replacing every **run** of the same character with that character followed by the length of the run. A run of length `1` is written as just the character (no `1`).

For example `"aabcccccaaa"` becomes `"a2bc5a3"`.

### Examples

**Example 1**

Input:

```python
compress_runs('aabcccccaaa')
```

Output:

```text
'a2bc5a3'
```

**Example 2**

Input:

```python
compress_runs('abc')
```

Output:

```text
'abc'
```

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains lower-case letters.

## Explanation

`groupby(s)` splits `s` into runs of equal characters. For each run write the character, plus its length when it is more than one. The pieces are joined once at the end.

### Complexity

- Time: O(n). One pass over the runs.
- Space: O(n). The result pieces.
