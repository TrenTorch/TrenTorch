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

**Explanation:** z[1] equals 1 because the first character 'a' matches the prefix. z[4] equals 3 since the three characters 'aab' match the prefix; other positions have mismatches at the first differing character.

**Example 2**

Input:

```python
z_function('aaaa')
```

Output:

```text
[0, 3, 2, 1]
```

**Explanation:** The second position contains 'aaa' which matches the prefix, giving z[1] = 3. At position 2 two characters match, so z[2] = 2; at position 3 one character matches, z[3] = 1.

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Searching text for a pattern with a double loop compares the pattern with the text at every start position and can take `O(n × m)` steps when the text is full of near-matches (for example `aaaa...a` against `aaa...b`). The fix is to **never re-read text you already matched**: use what you learned about the pattern itself. Two classic tools do this in `O(n + m)`: the **prefix function** (KMP) and the **Z-function**.

Keep the **rightmost match window** `[l, r)` found so far: a stretch `s[l:r]` equal to the start of `s`. For a new position `i` inside the window, `s[i]` corresponds to `s[i - l]`, so `z[i]` starts at `min(r - i, z[i - l])` without comparing anything. Only if the match reaches the edge of the window do you extend it letter by letter, and every extension pushes `r` to the right.

Since `r` only moves right, the total number of letter comparisons is `O(n)`. To find a pattern in a text, compute the Z-function of `pattern + "#" + text`: the positions with `z == len(pattern)` are the matches.

## Explanation

`l` and `r` are the window. The starting value of `z[i]` reuses the already computed `z[i - l]`; the `while` loop extends only beyond `r`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables                                               |
| ------------------------------------ | ------------------------------------------------------- |
| `n = len(s)`                         | `n = 7`                                                 |
| `left = right = 0`                   | `z = [0, 0, 0, 0, 0, 0, 0], left = 0, right = 0`        |
| `left, right = i, i + z[i]`          | `z = [0, 1, 0, 0, 0, 0, 0], left = 1, right = 2, i = 1` |
| `for i in range(1, n):`              | `i = 3`                                                 |
| `z[i] += 1`                          | `z = [0, 1, 0, 0, 1, 0, 0], left = 3, right = 3, i = 4` |
| `z[i] += 1`                          | `z = [0, 1, 0, 0, 3, 0, 0]`                             |
| `z[i] = min(right - i, z[i - left])` | `z = [0, 1, 0, 0, 3, 1, 0], left = 4, right = 7, i = 5` |
| `return`                             | `returned = [0, 1, 0, 0, 3, 1, 0]`                      |

### Complexity

- Time: O(n) (n is length of s).
- Extra space: O(n) (z array of length n).
- The brute force takes O(n^2) where n is length of s.
