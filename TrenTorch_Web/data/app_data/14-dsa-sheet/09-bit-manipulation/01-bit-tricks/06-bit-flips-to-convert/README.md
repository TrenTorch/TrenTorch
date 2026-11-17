---
name: sheet-bit-flips-to-convert
title: 'Bit Flips to Convert'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
theory: how-many-bits-differ
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

**Example 2**

Input:

```python
bit_flips_to_convert(5, 5)
```

Output:

```text
0
```

### Constraints

- `0 <= a, b < 2**31`

## Explanation

`a ^ b` marks the differing positions; Kernighan's loop counts them.

### Complexity

- Time: O(s). The XOR has a one exactly where the numbers differ, and the loop clears one set bit per step (`s` = number of differing bits).
- Space: O(1). One counter.
