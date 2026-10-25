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

**Explanation:** 1775 is 11011101111 in binary: runs of 2, 3 and 4 ones, separated by single zeros. Flipping the zero between the runs of 3 and 4 joins them into 3 + 1 + 4 = 8.

**Example 2**

Input:

```python
longest_ones_after_flip(7)
```

Output:

```text
4
```

**Explanation:** 7 is 111, and the bits above it are zeros. Flipping the next 0 gives a run of 4.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                            | Variables                                    |
| ------------------------------------------ | -------------------------------------------- |
| `best = current = previous = 0`            | `best = 0, current = 0, previous = 0`        |
| `current += 1`                             | `best = 3, current = 3, i = 2`               |
| `for i in range(32):`                      | `best = 5, current = 0, previous = 4, i = 5` |
| `best = max(best, previous + current + 1)` | `best = 8, current = 3, i = 7`               |
| `for i in range(32):`                      | `current = 2, previous = 3, i = 11`          |
| `for i in range(32):`                      | `current = 0, previous = 0, i = 16`          |
| `for i in range(32):`                      | `i = 24`                                     |
| `return`                                   | `returned = 8`                               |

### Complexity

- Time: O(1) fixed 32 iterations.
- Extra space: O(1) fixed extra variables.
- The brute force takes O(1) fixed 32 times 32 iterations.
