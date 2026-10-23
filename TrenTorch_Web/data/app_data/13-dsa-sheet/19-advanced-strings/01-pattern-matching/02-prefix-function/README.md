---
name: sheet-prefix-function
title: 'The Prefix Function'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
---

## Statement

For each position `i` of `s`, return the length of the **longest proper prefix of `s[:i + 1]` that is also a suffix of it** (proper: shorter than the whole piece).

For `"abcabca"` the answer is `[0, 0, 0, 1, 2, 3, 4]`.

The starter code tries every length at every position. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
prefix_function('abcabca')
```

Output:

```text
[0, 0, 0, 1, 2, 3, 4]
```

**Example 2**

Input:

```python
prefix_function('aaaa')
```

Output:

```text
[0, 1, 2, 3]
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

The **prefix function** `pi` of a string `s` gives for each position `i` the length of the **longest proper prefix of `s[:i + 1]` that is also its suffix** (proper means shorter than the whole string). For `"abcabca"` it is `[0, 0, 0, 1, 2, 3, 4]`. It is computed in one pass: keep `k`, the length of the current match; when the next letter does not extend it, fall back with `k = pi[k - 1]` until it does or `k` is 0. Each fall back is paid by an earlier increase, so the total is `O(n)`.

Why falling back with `pi[k - 1]` is right: if the current match `s[:k]` cannot be extended, the next best candidate is the longest border of `s[:k]` (a prefix that is also a suffix of it), and that is exactly `pi[k - 1]`. The prefix function is the engine of KMP and also answers questions about periods and repetitions.

## Explanation

`k` is the length of the current border. The `while` loop shortens it until the next letter fits, then `k += 1` on a match.
