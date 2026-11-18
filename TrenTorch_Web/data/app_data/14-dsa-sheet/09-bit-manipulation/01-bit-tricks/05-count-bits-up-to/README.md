---
name: sheet-count-bits-up-to
title: 'Count Bits for Every Number'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
theory: counting-bits-for-every-number
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

## Explanation

`i >> 1` is `i` without its lowest bit, so its count is already stored. Adding `i & 1` puts the dropped bit back.

### Complexity

- Time: O(n). Each answer reuses the one for `i >> 1` plus the last bit.
- Space: O(n). The output list.
