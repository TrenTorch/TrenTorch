---
name: sheet-z-function
title: 'The Z-Function'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Advanced
---

## Statement

The **Z-function** of `s` gives, for each position `i`, the length of the **longest common prefix of `s` and `s[i:]`**. By convention `z[0] = 0`.

For `"aabxaab"` the answer is `[0, 1, 0, 0, 3, 1, 0]`.

The starter code extends a match letter by letter at every position. It is correct but too slow on repetitive strings.

### Examples

**Example 1**

Input:

```python
z_function('aabxaab')
```

Output:

```text
[0, 1, 0, 0, 3, 1, 0]
```

**Example 2**

Input:

```python
z_function('aaaa')
```

Output:

```text
[0, 3, 2, 1]
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

Keep the **rightmost match window** `[l, r)` found so far: a stretch `s[l:r]` equal to the start of `s`. For a new position `i` inside the window, `s[i]` corresponds to `s[i - l]`, so `z[i]` starts at `min(r - i, z[i - l])` without comparing anything. Only if the match reaches the edge of the window do you extend it letter by letter, and every extension pushes `r` to the right.

Since `r` only moves right, the total number of letter comparisons is `O(n)`. To find a pattern in a text, compute the Z-function of `pattern + "#" + text`: the positions with `z == len(pattern)` are the matches.

## Explanation

`l` and `r` are the window. The starting value of `z[i]` reuses the already computed `z[i - l]`; the `while` loop extends only beyond `r`.
