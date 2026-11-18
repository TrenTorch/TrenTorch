---
name: sheet-reverse-bits
title: 'Reverse the Bits'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
theory: reversing-the-bits
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

## Explanation

Each round moves one bit from the bottom of `n` to the bottom of `result` while shifting the earlier bits of `result` up by one. The first bit read ends in position 31.

### Complexity

- Time: O(1). A fixed 32 steps, one per bit.
- Space: O(1). Two integers.
