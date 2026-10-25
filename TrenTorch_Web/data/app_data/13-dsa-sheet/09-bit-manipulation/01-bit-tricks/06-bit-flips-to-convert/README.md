---
name: sheet-bit-flips-to-convert
title: 'Bit Flips to Convert'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
---

## Statement

Return the number of **bits you must flip** to turn `a` into `b`, that is, the number of positions where `a` and `b` differ in binary. For `a = 10` (`1010`) and `b = 7` (`0111`) the answer is `3`.

### Examples

**Example 1**

Input:

```python
bit_flips_to_convert(10, 7)
```

Output:

```text
3
```

**Explanation:** 10 is 1010 in binary, 7 is 0111; they differ in three bit positions, so the answer is 3.

**Example 2**

Input:

```python
bit_flips_to_convert(5, 5)
```

Output:

```text
0
```

**Explanation:** 5 and 5 have identical binary representations, so zero bits differ and the result is 0.

### Constraints

- `0 <= a, b < 2**31`

## Theory

`a ^ b` (xor) has a `1` exactly where the bits of `a` and `b` **differ**. So the answer is the number of set bits of `a ^ b`, which you already know how to count.

This number is called the **Hamming distance**. XOR is the natural "difference" operator for bits: `x ^ x = 0` and `x ^ 0 = x`.

## Explanation

`a ^ b` marks the differing positions; Kernighan's loop counts them.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line    | Variables             |
| ------------------ | --------------------- |
| `diff = a ^ b`     | `diff = 13`           |
| `count = 0`        | `count = 0`           |
| `diff &= diff - 1` | `diff = 12`           |
| `count += 1`       | `count = 1`           |
| `count += 1`       | `diff = 8, count = 2` |
| `diff &= diff - 1` | `diff = 0`            |
| `count += 1`       | `count = 3`           |
| `return`           | `returned = 3`        |

### Complexity

- Time: O(k) where k is number of set bits in a^b.
- Extra space: O(1) constant extra memory.
- The brute force takes O(1) constant 40-bit loop.
