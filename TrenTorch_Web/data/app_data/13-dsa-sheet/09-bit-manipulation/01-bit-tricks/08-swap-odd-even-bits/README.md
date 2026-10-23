---
name: sheet-swap-odd-even-bits
title: 'Swap Odd and Even Bits'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
---

## Statement

Treat `n` as a 32-bit number and **swap every pair of neighbouring bits**: bit 0 with bit 1, bit 2 with bit 3, and so on. For `n = 10` (`1010`) the answer is `5` (`0101`).

### Examples

**Example 1**

Input:

```python
swap_odd_even_bits(10)
```

Output:

```text
5
```

**Example 2**

Input:

```python
swap_odd_even_bits(23)
```

Output:

```text
43
```

### Constraints

- `0 <= n < 2**32`

## Theory

Use two masks: `0x55555555` (`0101...`) selects the bits at **even** positions and `0xAAAAAAAA` (`1010...`) the bits at **odd** positions.

Shift the even bits **left** by one (into the odd slots) and the odd bits **right** by one (into the even slots), then combine with `|`:

`((n & 0x55555555) << 1) | ((n & 0xAAAAAAAA) >> 1)`

Masks plus shifts let you move groups of bits in one step, without a loop.

## Explanation

The two masked parts do not overlap after shifting, because the even bits move to odd positions and the odd bits to even positions. `|` merges them.
