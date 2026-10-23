---
name: sheet-repeated-substring-pattern
title: 'Repeated Substring Pattern'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
---

## Statement

Return `True` if `s` can be written as a **block repeated two or more times** (`"abab"` is `"ab"` twice; `"aaa"` is `"a"` three times; `"abcab"` is not).

A string with fewer than 2 letters gives `False`.

### Examples

**Example 1**

Input:

```python
repeated_substring_pattern('abab')
```

Output:

```text
True
```

**Example 2**

Input:

```python
repeated_substring_pattern('abcab')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

The **prefix function** `pi` of a string `s` gives for each position `i` the length of the **longest proper prefix of `s[:i + 1]` that is also its suffix** (proper means shorter than the whole string). For `"abcabca"` it is `[0, 0, 0, 1, 2, 3, 4]`. It is computed in one pass: keep `k`, the length of the current match; when the next letter does not extend it, fall back with `k = pi[k - 1]` until it does or `k` is 0. Each fall back is paid by an earlier increase, so the total is `O(n)`.

The **border** of the whole string, `b = pi[n - 1]`, is the longest prefix that is also a suffix. If `s` is made of a block of length `p` repeated, then removing the first block leaves a border of length `n - p`; and conversely the **smallest period** of `s` is `p = n - b`. The string is a repetition exactly when `b > 0` and `n` is divisible by `p = n - b`.

One pass for the prefix function, then a single test. `O(n)`.

## Explanation

`period = n - pi[-1]` is the smallest candidate block length; it works if it divides the length and the border is non-zero.
