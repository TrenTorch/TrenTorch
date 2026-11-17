---
name: sheet-count-set-bits
title: 'Count the Set Bits'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
theory: counting-set-bits-faster
---

## Statement

Return how many bits of `n` are `1` when `n` is written in binary. For `n = 13` (binary `1101`) the answer is `3`.

### Examples

**Example 1**

Input:

```python
count_set_bits(13)
```

Output:

```text
3
```

**Example 2**

Input:

```python
count_set_bits(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n < 2**62`

## Explanation

Each loop round removes one `1` bit with `n &= n - 1`, so the loop runs exactly as many times as there are set bits.

### Complexity

- Time: O(s). `n & (n - 1)` clears the lowest set bit, so the loop runs once per set bit (`s` <= the number of bits in `n`).
- Space: O(1). One counter.
