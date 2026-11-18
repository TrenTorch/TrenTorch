---
name: sheet-longest-ones-after-flip
title: 'Longest Run of Ones After One Flip'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Intermediate
theory: the-longest-run-of-ones-after-one-flip
---

## Statement

Write `n` as a 32-bit binary number. You may flip **at most one `0` bit to `1`**. Return the length of the **longest run of consecutive 1s** you can get. For `n = 1775` (`11011101111`) the answer is `8`.

### Examples

**Example 1**

Input:

```python
longest_ones_after_flip(1775)
```

Output:

```text
8
```

**Example 2**

Input:

```python
longest_ones_after_flip(7)
```

Output:

```text
4
```

### Constraints

- `0 <= n < 2**32`

## Explanation

`previous + current + 1` is the run left of the last zero, the flipped zero, and the run right of it. The `min(..., 32)` handles numbers with no zero, where the extra `+ 1` would count a bit that does not exist.

### Complexity

- Time: O(1). One pass over the 32 bits keeping the current and the previous run of ones.
- Space: O(1). A few integers.
