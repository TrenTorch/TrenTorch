---
name: sheet-reverse-bits
title: 'Reverse the Bits'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
---

## Statement

Treat `n` as a **32-bit** unsigned number, reverse the order of its 32 bits and return the new number. For `n = 1` (31 zeros and then a `1`) the answer is `2147483648` (a `1` and then 31 zeros).

### Examples

**Example 1**

Input:

```python
reverse_bits(1)
```

Output:

```text
2147483648
```

`1` becomes `1` followed by 31 zeros.

**Example 2**

Input:

```python
reverse_bits(43261596)
```

Output:

```text
964176192
```

### Constraints

- `0 <= n < 2**32`

## Theory

Build the answer bit by bit: take the lowest bit of `n` (`n & 1`), push it into the **result from the right** (`result = (result << 1) | bit`), then shift `n` right. After 32 rounds the first bit read has moved all the way to the top.

Always do all 32 rounds, even when `n` runs out of bits: leading zeros of `n` become trailing zeros of the answer, and the shifts of `result` make room for them.

## Explanation

Each round moves one bit from the bottom of `n` to the bottom of `result` while shifting the earlier bits of `result` up by one. The first bit read ends in position 31.
