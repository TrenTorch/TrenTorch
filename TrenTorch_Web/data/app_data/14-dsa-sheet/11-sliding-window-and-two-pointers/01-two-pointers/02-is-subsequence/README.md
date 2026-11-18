---
name: sheet-is-subsequence
title: 'Is It a Subsequence?'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Beginner
theory: both-pointers-moving-forward-subsequences
---

## Statement

Return `True` if `s` is a **subsequence** of `t`: you can get `s` by deleting some characters of `t` without changing the order of the others. `"ace"` is a subsequence of `"abcde"`; `"aec"` is not.

### Examples

**Example 1**

Input:

```python
is_subsequence('ace', 'abcde')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_subsequence('aec', 'abcde')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 100000`
- `0 <= len(t) <= 200000`
- Lower-case letters.

## Explanation

`i` counts how many characters of `s` have been matched so far, in order. Each character of `t` can match at most the next unmatched one.

### Complexity

- Time: O(|t|). One pass over `t`, advancing a pointer in `s` on each match.
- Space: O(1). One index.
