---
name: sheet-xor-of-range
title: 'XOR of a Range'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Advanced
---

## Statement

Return the XOR of **every number from `left` to `right`** (both included): `left ^ (left + 1) ^ ... ^ right`.

The starter code xors the numbers one by one. It is correct but far too slow for large ranges.

### Examples

**Example 1**

Input:

```python
xor_of_range(3, 9)
```

Output:

```text
2
```

**Example 2**

Input:

```python
xor_of_range(5, 5)
```

Output:

```text
5
```

### Constraints

- `0 <= left <= right <= 10**12`

## Theory

XOR of `0..n` has a **pattern with period 4**:

| `n % 4` | `0 ^ 1 ^ ... ^ n` |
| ------- | ----------------- |
| 0       | `n`               |
| 1       | `1`               |
| 2       | `n + 1`           |
| 3       | `0`               |

(Check `0^1 = 1`, `0^1^2 = 3`, `0^1^2^3 = 0`, `0^1^2^3^4 = 4`.) It repeats because every group of four consecutive numbers starting at a multiple of 4 xors to `0`: their higher bits cancel in pairs and the low two bits are `00, 01, 10, 11`.

A range is a **difference of two prefixes**, and xor undoes itself (`x ^ x = 0`), so `xor(left..right) = prefix(right) ^ prefix(left - 1)`. This is `O(1)`.

## Explanation

`prefix(n)` uses the table above. Xoring the prefix up to `right` with the prefix up to `left - 1` cancels all numbers below `left`.
