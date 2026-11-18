---
name: sheet-power-of-four
title: 'Is It a Power of Four?'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
theory: is-it-a-power-of-four
---

## Statement

Return `True` if `n` is a power of four (`1, 4, 16, 64, ...`). Do it without a loop.

### Examples

**Example 1**

Input:

```python
is_power_of_four(16)
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_power_of_four(8)
```

Output:

```text
False
```

### Constraints

- `-2**62 <= n < 2**62`

## Explanation

`0x5555555555555555` has a `1` at every even bit position (up to 62). A power of two that shares a bit with the mask has its set bit in an even position, which is exactly the powers of four.

### Complexity

- Time: O(1). One bit test for a power of two and one mask test that the bit is at an even position.
- Space: O(1). Nothing is stored.
