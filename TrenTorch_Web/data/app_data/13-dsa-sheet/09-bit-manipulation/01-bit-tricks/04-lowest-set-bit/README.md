---
name: sheet-lowest-set-bit
title: 'The Lowest Set Bit'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
---

## Statement

Return a number with **only the lowest set bit** of `n` kept. For `n = 12` (binary `1100`) the answer is `4` (binary `100`). For `n = 0` the answer is `0`.

### Examples

**Example 1**

Input:

```python
lowest_set_bit(12)
```

Output:

```text
4
```

**Example 2**

Input:

```python
lowest_set_bit(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n < 2**62`

## Theory

`n & (n - 1)` clears the lowest set bit. The opposite, **isolating** it, is `n & -n`.

Why it works: in two's complement, `-n` is `~n + 1`. Flipping all bits of `n` and adding 1 flips everything above the lowest set bit and keeps that bit and the zeros below it. So `n` and `-n` agree on exactly one set bit, the lowest, and `&` keeps only it.

This trick is the heart of the **Fenwick tree** (binary indexed tree), which uses `i & -i` to jump around a prefix-sum array.

## Explanation

`-n` has the same lowest set bit as `n` and the opposite of every bit above it, so `n & -n` is just that one bit. `0 & 0` is `0`.
