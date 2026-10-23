---
name: sheet-power-of-four
title: 'Is It a Power of Four?'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
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

## Theory

A power of four is a power of two **whose single set bit is in an even position**: `4` is `100` (bit 2), `16` is `10000` (bit 4). Powers of two like `2` (`10`, bit 1) and `8` (`1000`, bit 3) have the bit in an odd position.

So the test has two parts: (1) it is a power of two: `n > 0 and n & (n - 1) == 0`; (2) the bit sits in an even position, which you check with a **mask** that has 1s in every even position: `0x5555...`, binary `0101 0101 ...`. `n & mask != 0` means the bit is in an even position.

A mask is a number made to select particular bits with `&`. It is the most common tool of bit tricks.

## Explanation

`0x5555555555555555` has a `1` at every even bit position (up to 62). A power of two that shares a bit with the mask has its set bit in an even position, which is exactly the powers of four.
