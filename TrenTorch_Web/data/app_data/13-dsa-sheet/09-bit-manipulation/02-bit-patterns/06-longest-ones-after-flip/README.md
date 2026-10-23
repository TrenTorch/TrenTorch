---
name: sheet-longest-ones-after-flip
title: 'Longest Run of Ones After One Flip'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Intermediate
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

## Theory

This is a **sliding window** over the bits with at most one zero inside. Walk through the 32 bits keeping `current` (the length of the run of 1s ending here, counting the flipped zero's right side) and `previous` (the run before the last zero).

- On a `1`: `current += 1`.
- On a `0`: `previous = current` (if the next bit is 1 the two runs join through this zero) and `current = 0`.
- After each bit: `best = max(best, previous + current + 1)`, the `+ 1` being the flipped zero.

The answer is capped at 32 (the number of bits). An all-ones number has no zero to flip: the answer is 32.

## Explanation

`previous + current + 1` is the run left of the last zero, the flipped zero, and the run right of it. The `min(..., 32)` handles numbers with no zero, where the extra `+ 1` would count a bit that does not exist.
