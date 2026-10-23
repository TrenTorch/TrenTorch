---
name: sheet-count-overlapping-occurrences
title: 'Count Overlapping Occurrences'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
---

## Statement

Count the **occurrences of `pattern` in `text`**, counting overlapping ones (`"aa"` occurs 3 times in `"aaaa"`). `pattern` is not empty.

For `text = "aaaa"` and `pattern = "aa"` the answer is `3`.

The starter code compares letter by letter at every start. It is correct but too slow on repetitive texts.

### Examples

**Example 1**

Input:

```python
count_overlapping('aaaa', 'aa')
```

Output:

```text
3
```

**Example 2**

Input:

```python
count_overlapping('abababa', 'aba')
```

Output:

```text
3
```

### Constraints

- `0 <= len(text) <= 200000`
- `1 <= len(pattern) <= 2000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

The **prefix function** `pi` of a string `s` gives for each position `i` the length of the **longest proper prefix of `s[:i + 1]` that is also its suffix** (proper means shorter than the whole string). For `"abcabca"` it is `[0, 0, 0, 1, 2, 3, 4]`. It is computed in one pass: keep `k`, the length of the current match; when the next letter does not extend it, fall back with `k = pi[k - 1]` until it does or `k` is 0. Each fall back is paid by an earlier increase, so the total is `O(n)`.

Run the KMP search from the previous questions, but do not stop at the first match: when `k == len(pattern)` count one and then **fall back** with `k = fail[k - 1]` so that the next, possibly overlapping, occurrence can continue from the border of the match. `O(n + m)`.

Python's `str.count` counts only non-overlapping occurrences, so it is not enough here.

## Explanation

After a full match the fall back `k = fail[k - 1]` keeps the longest border, which is where an overlapping match would start.
