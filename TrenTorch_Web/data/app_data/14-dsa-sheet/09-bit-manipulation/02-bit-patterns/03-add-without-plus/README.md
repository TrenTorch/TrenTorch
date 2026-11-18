---
name: sheet-add-without-plus
title: 'Add Without the Plus Sign'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
theory: adding-without-the-plus-sign
---

## Statement

Return `a + b` **without using `+` or `-`**, only bit operations. The numbers are 32-bit signed integers; if the true sum does not fit in 32 bits, the answer **wraps around** like a 32-bit register: the result is the sum reduced to the range `-2**31 .. 2**31 - 1`.

### Examples

**Example 1**

Input:

```python
bit_add(1, 2)
```

Output:

```text
3
```

**Example 2**

Input:

```python
bit_add(-2, 3)
```

Output:

```text
1
```

### Constraints

- `-2**31 <= a, b < 2**31`

## Explanation

`a ^ b` adds without carry; `(a & b) << 1` is the carry. With the mask, values stay in 0..2**32-1, and the final test restores the sign.

### Complexity

- Time: O(1). The carry loop runs at most 32 times because each round pushes the carry one place left.
- Space: O(1). A few integers.
