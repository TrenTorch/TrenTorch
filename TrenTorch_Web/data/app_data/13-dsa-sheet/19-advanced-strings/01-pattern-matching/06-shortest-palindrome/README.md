---
name: sheet-shortest-palindrome
title: 'Shortest Palindrome'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Advanced
---

## Statement

You may add letters **only in front of `s`**. Return the **shortest palindrome** you can get this way.

For `"aacecaaa"` the answer is `"aaacecaaa"`; for `"abcd"` it is `"dcbabcd"`.

The starter code tests every prefix for being a palindrome letter by letter. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
shortest_palindrome('aacecaaa')
```

Output:

```text
'aaacecaaa'
```

**Explanation:** The longest palindromic prefix of "aacecaaa" is "aacecaa", so the remaining "a" reversed and placed in front yields "aaacecaaa".

**Example 2**

Input:

```python
shortest_palindrome('abcd')
```

Output:

```text
'dcbabcd'
```

**Explanation:** For "abcd" the only palindromic prefix is "a", thus the suffix "bcd" reversed as "dcb" is prepended, producing "dcbabcd".

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

The **prefix function** `pi` of a string `s` gives for each position `i` the length of the **longest proper prefix of `s[:i + 1]` that is also its suffix** (proper means shorter than the whole string). For `"abcabca"` it is `[0, 0, 0, 1, 2, 3, 4]`. It is computed in one pass: keep `k`, the length of the current match; when the next letter does not extend it, fall back with `k = pi[k - 1]` until it does or `k` is 0. Each fall back is paid by an earlier increase, so the total is `O(n)`.

To add as few letters as possible, find the **longest prefix of `s` that is already a palindrome**; then put the reverse of the remaining part in front. So the question is: how long is the longest palindromic prefix?

A prefix of length `k` is a palindrome when it equals its own reverse. Build `t = s + "#" + reverse(s)` and compute its prefix function. The last value `pi[-1]` is the longest prefix of `s` that is also a suffix of `reverse(s)`, which is exactly the longest palindromic prefix (the `#` stops the match from crossing the middle). The answer is `reverse(s[pi[-1]:]) + s`. `O(n)`.

## Explanation

`border` is the length of the longest palindromic prefix. The part of `s` after it is reversed and placed in front.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line              | Variables                                                                 |
| ---------------------------- | ------------------------------------------------------------------------- |
| `t = s + "#" + s[::-1]`      | `t = 'aacecaaa#aaacecaa'`                                                 |
| `k = pi[k - 1]`              | `pi = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], k = 0, i = 2`  |
| `k += 1`                     | `pi = [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], k = 2, i = 6`  |
| `k = pi[k - 1]`              | `pi = [0, 1, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], k = 1, i = 8`  |
| `pi[i] = k`                  | `pi = [0, 1, 0, 0, 0, 1, 2, 2, 0, 1, 2, 0, 0, 0, 0, 0, 0], k = 2, i = 10` |
| `pi[i] = k`                  | `pi = [0, 1, 0, 0, 0, 1, 2, 2, 0, 1, 2, 2, 3, 0, 0, 0, 0], k = 3, i = 12` |
| `for i in range(1, len(t)):` | `pi = [0, 1, 0, 0, 0, 1, 2, 2, 0, 1, 2, 2, 3, 4, 5, 0, 0], k = 5, i = 15` |
| `return`                     | `returned = 'aaacecaaa'`                                                  |

### Complexity

- Time: O(n) where n is length of s.
- Extra space: O(n) extra memory for pi and concatenated string.
- The brute force takes O(n^2) where n is length of s.
