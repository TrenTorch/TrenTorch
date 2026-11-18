---
name: sheet-swap-odd-even-bits
title: 'Swap Odd and Even Bits'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
theory: masks-that-pick-out-many-bits
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

## Explanation

The two masked parts do not overlap after shifting, because the even bits move to odd positions and the odd bits to even positions. `|` merges them.

### Complexity

- Time: O(1). Two masks and two shifts.
- Space: O(1). Nothing is stored.
