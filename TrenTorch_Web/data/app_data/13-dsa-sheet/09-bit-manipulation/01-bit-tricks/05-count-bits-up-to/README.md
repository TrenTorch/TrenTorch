---
name: sheet-count-bits-up-to
title: 'Count Bits for Every Number'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
---

## Statement

Return a list of length `n + 1` where entry `i` is the number of set bits in `i`, for `i = 0, 1, ..., n`.

For `n = 5` the answer is `[0, 1, 1, 2, 1, 2]`.

### Examples

**Example 1**

Input:

```python
count_bits_up_to(5)
```

Output:

```text
[0, 1, 1, 2, 1, 2]
```

**Example 2**

Input:

```python
count_bits_up_to(0)
```

Output:

```text
[0]
```

### Constraints

- `0 <= n <= 200000`

## Theory

Counting the bits of each number separately costs `O(n log n)`. Dynamic programming gives `O(n)`: the number `i` is the number `i >> 1` (shifted right, dropping the last bit) plus that last bit. So

`bits[i] = bits[i >> 1] + (i & 1)`

and `bits[i >> 1]` is already known because `i >> 1 < i`. Start with `bits[0] = 0` and fill from left to right.

This is a first taste of **DP**: use answers for smaller inputs to build the answer for bigger ones.

## Explanation

`i >> 1` is `i` without its lowest bit, so its count is already stored. Adding `i & 1` puts the dropped bit back.
