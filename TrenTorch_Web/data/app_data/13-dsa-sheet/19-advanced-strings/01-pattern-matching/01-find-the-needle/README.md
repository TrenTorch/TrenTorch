---
name: sheet-find-the-needle
title: 'Find the Needle'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
---

## Statement

Return the **index of the first occurrence** of `needle` in `haystack`, or `-1` if it does not occur. An empty `needle` occurs at index `0`.

For `haystack = "sadbutsad"` and `needle = "sad"` the answer is `0`; for `needle = "leeto"` in `"leetcode"` it is `-1`.

The starter code compares letter by letter at every start. It is correct but too slow on repetitive texts.

### Examples

**Example 1**

Input:

```python
find_needle('sadbutsad', 'sad')
```

Output:

```text
0
```

**Explanation:** Because 'sad' appears at the very beginning of 'sadbutsad', the first match is at index 0.

**Example 2**

Input:

```python
find_needle('leetcode', 'leeto')
```

Output:

```text
-1
```

**Explanation:** Because 'leeto' does not occur in 'leetcode', no match is found so result is -1.

### Constraints

- `0 <= len(haystack) <= 200000`
- `0 <= len(needle) <= 2000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

The **prefix function** `pi` of a string `s` gives for each position `i` the length of the **longest proper prefix of `s[:i + 1]` that is also its suffix** (proper means shorter than the whole string). For `"abcabca"` it is `[0, 0, 0, 1, 2, 3, 4]`. It is computed in one pass: keep `k`, the length of the current match; when the next letter does not extend it, fall back with `k = pi[k - 1]` until it does or `k` is 0. Each fall back is paid by an earlier increase, so the total is `O(n)`.

**KMP search:** compute `pi` for the needle. Scan the haystack with a counter `k` = how many letters of the needle are currently matched. For each text letter, while it does not match `needle[k]`, fall back `k = pi[k - 1]`; if it matches, `k += 1`. When `k == len(needle)` the needle ends here: the start is `i - k + 1`. The text pointer never moves back, so the search is `O(n + m)`.

## Explanation

`fail` is the prefix function of the needle. `k` is the length of the current match; the fall back reuses the part of the needle that is still valid.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                |
| ----------------------------------- | ------------------------ |
| `fail = [0] * len(needle)`          | `fail = [0, 0, 0]`       |
| `k = 0`                             | `k = 0`                  |
| `for i in range(1, len(needle)):`   | `i = 2`                  |
| `for i, ch in enumerate(haystack):` | `i = 0, ch = 's'`        |
| `for i, ch in enumerate(haystack):` | `k = 1, i = 1, ch = 'a'` |
| `k += 1`                            | `k = 2`                  |
| `k += 1`                            | `k = 3, i = 2, ch = 'd'` |
| `return`                            | `returned = 0`           |

### Complexity

- Time: O(n + m).
- Extra space: O(m).
- The brute force takes O(n * m).
