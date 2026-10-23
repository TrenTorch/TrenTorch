---
name: sheet-is-subsequence
title: 'Is It a Subsequence?'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Beginner
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

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Use one pointer for each string. Walk through `t`; whenever the current character of `t` equals the **next wanted** character of `s`, advance the pointer in `s`. At the end `s` is a subsequence exactly when the pointer in `s` reached its end.

The pointer in `t` moves every step, the pointer in `s` only on a match: one pass, `O(len(t))`.

## Explanation

`i` counts how many characters of `s` have been matched so far, in order. Each character of `t` can match at most the next unmatched one.
