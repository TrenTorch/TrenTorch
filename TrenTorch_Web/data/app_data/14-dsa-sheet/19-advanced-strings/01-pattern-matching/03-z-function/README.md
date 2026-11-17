---
name: sheet-z-function
title: 'The Z-Function'
tags: [dsa-sheet, advanced-strings, pattern-matching]
difficulty: Advanced
theory: the-window-trick
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

## Explanation

`l` and `r` are the window. The starting value of `z[i]` reuses the already computed `z[i - l]`; the `while` loop extends only beyond `r`.

### Complexity

- Time: O(n). The window `[left, right)` only moves right, and letters inside it are never compared again.
- Space: O(n). The result array.
