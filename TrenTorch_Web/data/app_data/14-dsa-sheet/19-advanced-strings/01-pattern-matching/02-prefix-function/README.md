---
name: sheet-prefix-function
title: 'The Prefix Function'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Intermediate
theory: computing-it-in-one-pass
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

## Explanation

`k` is the length of the current border. The `while` loop shortens it until the next letter fits, then `k += 1` on a match.

### Complexity

- Time: O(n). The pointer `k` grows by at most one per letter and every failure step shrinks it, so the total number of steps is at most `2n`.
- Space: O(n). The result array.
