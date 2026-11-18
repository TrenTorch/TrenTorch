---
name: sheet-lowest-set-bit
title: 'The Lowest Set Bit'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
theory: isolating-the-lowest-set-bit
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

## Explanation

`-n` has the same lowest set bit as `n` and the opposite of every bit above it, so `n & -n` is just that one bit. `0 & 0` is `0`.

### Complexity

- Time: O(1). `n & -n` isolates the lowest set bit.
- Space: O(1). Nothing is stored.
