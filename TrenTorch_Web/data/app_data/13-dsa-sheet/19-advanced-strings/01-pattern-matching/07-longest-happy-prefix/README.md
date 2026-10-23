---
name: sheet-longest-happy-prefix
title: 'Longest Happy Prefix'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
---

## Statement

A **happy prefix** is a non-empty prefix of `s` (shorter than `s`) that is also a suffix. Return the **longest happy prefix**, or `""` if there is none.

For `"level"` the answer is `"l"`; for `"ababab"` it is `"abab"`.

The starter code compares every possible length from scratch. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_happy_prefix('level')
```

Output:

```text
'l'
```

**Example 2**

Input:

```python
longest_happy_prefix('ababab')
```

Output:

```text
'abab'
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

The **prefix function** `pi` of a string `s` gives for each position `i` the length of the **longest proper prefix of `s[:i + 1]` that is also its suffix** (proper means shorter than the whole string). For `"abcabca"` it is `[0, 0, 0, 1, 2, 3, 4]`. It is computed in one pass: keep `k`, the length of the current match; when the next letter does not extend it, fall back with `k = pi[k - 1]` until it does or `k` is 0. Each fall back is paid by an earlier increase, so the total is `O(n)`.

The answer is exactly what the prefix function holds for the last position: `s[:pi[-1]]`. This is the _border_ of the whole string. `O(n)`.

## Explanation

The loop is the standard prefix function; only the last value is used.
