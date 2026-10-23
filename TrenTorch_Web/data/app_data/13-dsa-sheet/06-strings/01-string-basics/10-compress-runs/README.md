---
name: sheet-compress-runs
title: 'Compress Repeated Characters'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

## Theory

This is **run-length encoding**. Scan the string and keep the current character and how many times it has repeated. When the next character differs (or the string ends), write out the finished run and start a new one.

`itertools.groupby(s)` does the grouping for you: it yields `(character, run)` pairs for consecutive equal characters, so a run's length is `sum(1 for _ in run)`. Collect the pieces in a list and `join` them once, because `+=` on a long string in a loop is slow.

## Explanation

`groupby(s)` splits `s` into runs of equal characters. For each run write the character, plus its length when it is more than one. The pieces are joined once at the end.
